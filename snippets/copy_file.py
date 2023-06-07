def copier_fichier(source, destination):
    try:
        with open(source, 'r') as fichier_source:
            contenu = fichier_source.read()
    except FileNotFoundError:
        print("This file does not exist...")
        return
    except Exception as e:
        print(e)

    with open(destination, 'w') as fichier_destination:
        fichier_destination.write(contenu)
        print("File copied")


while True:
    source = input("Run number wanted to copy >")
    source = "cern_data_run{0}.txt".format(source)
    copier_fichier(source, "copy_{0}".format(source))
    print("----------")
