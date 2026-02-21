
# diese Anwendung demonsriert die Verwendung von Python Standard Funktionen.


def main():

    print("Hallo Python Programmierer!")

    name = input("Wie heißt du? ")

    print(f"Schön dich kennenzulernen, {name}!")
    
    alter = int( input("Wie alt bist du? "))
    
    if alter < 18:

        print("Du bist minderjährig.")
    elif alter < 65:
            print("Du bist erwachsen.")
    else:
        print("Du bist senior.")

    

         


# Das Skript wird nur ausgeführt, wenn es direkt aufgerufen wird, 
# nicht wenn es als Modul importiert wird.

if __name__ == "__main__":
    main()