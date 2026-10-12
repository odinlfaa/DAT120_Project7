import csv
import os

# Finner CSV-filen
mappe = os.path.dirname(__file__)
filnavn = os.path.join(mappe, "sinnes_2014_2025.csv")

# Spør brukeren om år
aar = input("Hvilket år vil du beregne planteveksten for? ")

total_vekst = 0

with open(filnavn, "r", encoding="utf-8") as fil:
    leser = csv.DictReader(fil, delimiter=";")

    for rad in leser:
        dato = rad["Tid(norsk normaltid)"]

        if dato.endswith(aar):

            temperatur_tekst = rad["Middeltemperatur (døgn)"]

            # Hopper over dager som mangler temperatur
            if temperatur_tekst != "-":

                temperatur = float(
                    temperatur_tekst.replace(",", ".")
                )

                if temperatur > 5:
                    vekst = temperatur - 5
                    total_vekst += vekst

print("Total plantevekst i", aar, "er:", total_vekst)