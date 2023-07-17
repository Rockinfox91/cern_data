from src.process.graph import tension_graph
from src.process.data_analyse import lire_data

if __name__ == "__main__":

    data = lire_data("windows_final_data")

    LN2_data = data[data["Time"]<1687773600]
    LAr_data = data[data["Time"]>1688371200]
    LN2_using_motor_data = LN2_data[(LN2_data["I1"]>0.5 )|(LN2_data["I3"]>0.5)]
    LAr_using_motor_data = LAr_data[(LAr_data["I1"]>0.5 )|(LAr_data["I3"]>0.5)]

    nb_total_data_ln2 = LN2_data.size
    nb_using_motor_data_ln2 = LN2_using_motor_data.size
    nb_total_data_lar = LAr_data.size
    nb_using_motor_data_lar = LAr_using_motor_data.size

    print(f"Total données : {nb_total_data_ln2}\n Moteurs en cours : {nb_using_motor_data_ln2}\n {nb_using_motor_data_ln2 / nb_total_data_ln2 * 100}%")
    print(f"Total données : {nb_total_data_lar}\n Moteurs en cours : {nb_using_motor_data_lar}\n {nb_using_motor_data_lar / nb_total_data_lar * 100}%")

    print(LN2_data["Time"].iloc[-1] - LN2_data["Time"].iloc[0])
    print(LAr_data["Time"].iloc[-1] - LAr_data["Time"].iloc[0])