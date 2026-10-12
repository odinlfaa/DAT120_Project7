import csv

filnavn = "sinnes_2014_2025.csv"

aar = input("Skriv inn år! ")

sommerdager = 0
høysommerdager = 0
tropedager = 0

with open(filnavn, "r", encoding="utf-8-sig") as fil:
    leser = csv.DictReader(fil, delimiter=";")

    for rad in leser:
        dato = rad["Tid(norsk normaltid)"]
        temperatur = rad["Maksimumstemperatur (døgn)"]

        # Teller bare dager fra det valgte året
        if dato.endswith(aar) and temperatur != "" and temperatur != "-":
            temperatur = float(temperatur.replace(",", "."))

            if temperatur > 20:
                sommerdager += 1

            if temperatur > 25:
                høysommerdager += 1

            if temperatur > 30:
                tropedager += 1

print("Antall sommerdager:", sommerdager)
print("Antall høysommerdager:", høysommerdager)
print("Antall tropedager:", tropedager)
