def copier_fichier(source, destination):
    with open(source, 'r') as fichier_source:
        contenu = fichier_source.read()

    with open(destination, 'w') as fichier_destination:
        fichier_destination.write(contenu)


source = input("Numéro run voulu >")
source = f"cern_data_run{source}.txt"
copier_fichier(source, destination=f"copy_{source}")