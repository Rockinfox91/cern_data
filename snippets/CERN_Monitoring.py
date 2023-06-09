from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import time
import numpy as np
import threading
import os.path
import serial
from PyDAQmx import *
import sys
import pyvisa as visa
 
# NI Class to read gauge and temperature
class readNidaq():#QtCore.QObject):
    def __init__(self,*args):
        super().__init__(*args)

    def configure(self):
        print("Configuring Ni DAQ")
        self.analog_input=Task()
        self.data = np.zeros((400,), dtype=np.float64) ### DATA FROM NI MODULES
        self.read=int32()

        self.analog_input.CreateAIRTDChan("cDAQ1Mod3/ai0:3","",-40.0,60.0,DAQmx_Val_DegC,DAQmx_Val_Pt3928,DAQmx_Val_4Wire,DAQmx_Val_Internal,0.001,100)
        self.analog_input.CfgSampClkTiming("",100.0,DAQmx_Val_Rising,DAQmx_Val_ContSamps,100)
        self.analog_input.StartTask()

    def readRTD(self):
        try:
            self.analog_input.ReadAnalogF64(100,10.0,DAQmx_Val_GroupByChannel,self.data,400,(self.read),None)
            self.tA=np.mean(self.data[:99])
            self.tB=np.mean(self.data[100:199])
            self.tC=np.mean(self.data[200:299])
            self.tD=np.mean(self.data[300:])
        except DAQError as err:
            print(err)

    def run(self):
        self.configure()
        while True :
            self.readRTD()

if __name__ == '__main__':
    #### TTi power supply address ####
    resource1='COM7' ## Motor4 : COM7
    resource3='COM8' ## Motor1 : COM8
    rm = visa.ResourceManager()
    
    print('TTi power supply for motor 4: ')
    instrument1 = rm.open_resource(resource1)
    print(instrument1.query("*IDN?"))
    print("The Input voltage: ",instrument1.query("VO?"))

    print('TTi power supply for motor 1: ')
    instrument3 = rm.open_resource(resource3)
    print(instrument3.query("*IDN?"))
    print("The Input voltage: ",instrument3.query("VO?"))
    
    ## Arduino stuff
    ser = serial.Serial('COM9', 9600) # Creating serial object

    # Output file
    n_run = 1
    data_file = "CERN/cern_test_data.txt"
    if os.path.isfile(data_file):
        while os.path.isfile(data_file):
            data_file = "CERN/cern_data_run" + str(n_run) + ".txt"
            n_run += 1
    print("===> Saving data in: ", data_file)
            
    file = open(data_file,'w') # creating the output file
    file.write("Time\tFlowIn\tTout\tHout\tTamb\tHamb\tHin\tCryoL\tTa\tTb\tTc\tTd\tI1\tI3") # column titles
    file.close()

    # Creating the NI object
    lecture=readNidaq()

    # Creating the thread
    t=threading.Thread(group=None, target=lecture.run, name=None)
    t.start()
    time.sleep(2)

    # Creating the QT window + its widgets
    app = QtGui.QApplication([])
    w = QtGui.QWidget()

    plot = pg.PlotWidget(w) # Temp plot
    plot.addLegend()
    plot1 = pg.PlotWidget(w) # Current plot
    plot1.addLegend()
    plot2 = pg.PlotWidget(w) # Humidity plot
    plot2.addLegend()
    plot3 = pg.PlotWidget(w) # Flow plot
    labelGauge=QtGui.QLabel(w)
    newfont=QtGui.QFont("Times",25,QtGui.QFont.Bold)
    labelGauge.setFont(newfont)
    labelGauge.setWordWrap(True)

    ## Create a grid layout to manage the widgets size and position
##    layout = QtGui.QVBoxLayout()
    layout = QtGui.QGridLayout()
    w.setLayout(layout)

    ## Add widgets to the layout in their proper positions
    layout.addWidget(plot, 1, 1)#, 0, 0, 1, 3) # creating plot for temperatures
    layout.addWidget(plot1, 1, 2)#,1,0,1,3)    # creating plot for currents
    layout.addWidget(plot2, 2, 1)#,2,0,1,3)    # creating plot for humidity
    layout.addWidget(plot3, 2, 2)#,2,0,1,3)    # creating plot for N2 flow
    layout.addWidget(labelGauge, 0, 0, 1, 3)#,3,1,3,2) # creating the measurement output on screen

    plot.plotItem.setTitle(title="Temperatures (°C)")
    plot1.plotItem.setTitle(title="Currents (A)")
    plot2.plotItem.setTitle(title="humidity (%)")
    plot3.plotItem.setTitle(title="Cryostat filled volume")
    curve_t1=plot.plotItem.plot(pen='y',name = 'Bottom') # defining the curve corresponding to the first temperature
    curve_t2=plot.plotItem.plot(pen='r',name = 'Elbow') # defining the curve corresponding to the second temperature
    curve_t3=plot.plotItem.plot(pen='b',name = 'Intermediate') # defining the curve corresponding to the third temperature
    curve_t4=plot.plotItem.plot(pen='g',name = 'Top') # defining the curve corresponding to the fourth temperature
    curve_t5=plot.plotItem.plot(pen='w',name = 'Out') # defining the curve corresponding to the fifth temperature
    curve_t6=plot.plotItem.plot(pen='c',name = 'Ambient') # defining the curve corresponding to the sixth temperature

    curve_I1=plot1.plotItem.plot(pen='r',name = 'Motor 1')# defining the curve corresponding to the current of motor 1
    curve_I3=plot1.plotItem.plot(pen='g',name = 'Motor 3')# defining the curve corresponding to the current of motor 3

    curve_h1=plot2.plotItem.plot(pen='w',name = 'Out')# defining the curve corresponding to the first humidity measurement
    curve_h2=plot2.plotItem.plot(pen='c',name = 'Ambient')# defining the curve corresponding to the 2nd humidity measurement
    curve_h3=plot2.plotItem.plot(pen='m',name = 'In')# defining the curve corresponding to the 3rd humidity measurement

    curve_f=plot3.plotItem.plot(pen='m')# defining the curve corresponding to the cryostat filled volume
    
    w.show()

    x=[]

    yt1=[]
    yt2=[]
    yt3=[]
    yt4=[]
    yt5=[] #temp Ambient
    yt6=[] #temp Out

    yI1=[] # current motor1
    yI3=[] # current motor3
    
    yh1=[]# humidity Ambient
    yh2=[]# humidity Out
    yh3=[]# humidity In

    yf1=[]# gauge cryo

    j=0

    def update():
        global j,temps0

        n_sample = 1000

        file = open(data_file,'a') # open the output file in "append" mode
        file.seek(0, 2) # To be sure the file's position is at the end (prevent any trouble)
        output_screen = ""
        data_to_save = "\n" + str(time.time()) + "\t" #getting linux time

        try:

# Getting sensor values from ARDUINO ###
            value = ser.readline().decode('utf-8')
            value = value.strip('\n')
            print("From Arduino: ", value)
            loc = value.find("\t")
            out_arduino = []

            while loc != -1:
                temp = float(value[:loc])
                out_arduino.append(temp)
                value = value[(loc+1):]
                loc = value.find("\t")
            out_arduino.append(float(value[(loc+1):]))

            flow_t = out_arduino[0]
##            yf1.append(flow_t)
            output_screen += "f: {0:1.2f}".format(flow_t)
            data_to_save += "{0:1.3f}\t".format(flow_t)

            t_out = out_arduino[1]
            yt5.append(t_out)
            output_screen += " a.u tout: {0:1.2f}".format(t_out)
            data_to_save += "{0:1.3f}\t".format(t_out)

            h_out = out_arduino[2]
            yh1.append(h_out)
            output_screen += " °C hout: {0:1.2f}".format(h_out)
            data_to_save += "{0:1.3f}\t".format(h_out)

            t_amb = out_arduino[3]
            yt6.append(t_amb)
            output_screen += " % tamb: {0:1.2f}".format(t_amb)
            data_to_save += "{0:1.3f}\t".format(t_amb)

            h_amb = out_arduino[4]
            yh2.append(h_amb)
            output_screen += " °C hamb: {0:1.2f}".format(h_amb)
            data_to_save += "{0:1.3f}\t".format(h_amb)

            h_in = (out_arduino[5]*5/1023) * 38.9 - 41.939 # Calculating humidity for HM1500LF
            yh3.append(h_in)
            output_screen += " %  hin: {0:1.2f}".format(h_in)
            data_to_save += "{0:1.3f}\t".format(h_in)           

            if out_arduino[6]>5: # 
                height = (out_arduino[6]-200) + 57 # Calculating height of LN2 in cryostat
                g_cryostat = height*100/2*57 # filled % of the cryostat
            else: # case when the gauge sensor is not providing signal (turned off)
                g_cryostat = 0
            yf1.append(g_cryostat)
            output_screen += " %\nCryo: {0:1.2f}".format(g_cryostat)
            data_to_save += "{0:1.3f}\t".format(g_cryostat)           

            yt1.append(lecture.tA)
            output_screen += " % t1: {0:1.2f}".format(lecture.tA)
            data_to_save += "{0:1.3f}\t".format(lecture.tA)
            
            yt2.append(lecture.tB)
            output_screen += " °C  t2: {0:1.2f}".format(lecture.tB)
            data_to_save += "{0:1.3f}\t".format(lecture.tB)
            
            yt3.append(lecture.tC)
            output_screen += " °C  t3: {0:1.2f}".format(lecture.tC)
            data_to_save += "{0:1.3f}\t".format(lecture.tC)
           
            yt4.append(lecture.tD)
            output_screen += " °C  t4: {0:1.2f} °C".format(lecture.tD)
            data_to_save += "{0:1.3f}\t".format(lecture.tD)

                ### Getting the currents from the motor power supplies
            cur = instrument1.query("IO?")
            current1 = float(cur[2:])
            cur = instrument3.query("IO?")
            current3 = float(cur[2:])
            print("Currents: ", current1, current3)

            yI1.append(current1)
            yI3.append(current3)
            output_screen += " °C  I1: {0:1.2f}".format(current1)
            data_to_save += "{0:1.3f}\t".format(current1)
            output_screen += " A  I3: {0:1.2f} A".format(current3)
            data_to_save += "{0:1.3f}".format(current3)

            if j==0:
                temps0=time.time()
##                print("Time of start: ", temps0)
                x.append(0)
                j+=1
            else:
                if len(yt1)!=0:
                    x.append(time.time()-temps0)
                j+=1

##                print("Time: ", time.time())
##            print(output_screen)

            if(len(x)<n_sample):
                curve_t1.setData(x,yt1)
                curve_t2.setData(x,yt2)
                curve_t3.setData(x,yt3)
                curve_t4.setData(x,yt4)
                curve_t5.setData(x,yt5)
                curve_t6.setData(x,yt6)
                curve_h1.setData(x,yh1)
                curve_h2.setData(x,yh2)
                curve_h3.setData(x,yh3)
                curve_f.setData(x,yf1)
                curve_I1.setData(x,yI1)
                curve_I3.setData(x,yI3)
            else:
                curve_t1.setData(x[-n_sample:],yt1[-n_sample:])
                curve_t2.setData(x[-n_sample:],yt2[-n_sample:])
                curve_t3.setData(x[-n_sample:],yt3[-n_sample:])
                curve_t4.setData(x[-n_sample:],yt4[-n_sample:])
                curve_t5.setData(x[-n_sample:],yt5[-n_sample:])
                curve_t6.setData(x[-n_sample:],yt6[-n_sample:])
                curve_h1.setData(x[-n_sample:],yh1[-n_sample:])
                curve_h2.setData(x[-n_sample:],yh2[-n_sample:])
                curve_h3.setData(x[-n_sample:],yh3[-n_sample:])
                curve_f.setData(x[-n_sample:],yf1[-n_sample:])
                curve_I1.setData(x[-n_sample:],yI1[-n_sample:])
                curve_I3.setData(x[-n_sample:],yI3[-n_sample:])
                
               
            labelGauge.setText(output_screen)
            file.write(data_to_save) #saving data
            #print(data_to_save)
            file.close()

        except KeyboardInterrupt:
            print("Stopping the monitoring")
            file.close()  # plt.close() was written ? Maybe an error ?
            sys.exit(1)
            
        except:
            if j == 0:
                print("Passing...")
                j+=1
                pass

            
        

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(1000)

    QtGui.QApplication.instance().exec()
