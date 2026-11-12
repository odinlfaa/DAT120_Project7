
import csv
import matplotlib.pyplot as plt

aar = []
sommerdager = []
hoysommerdager = []
tropedager = []

with open("oslo_blindern_1954_2025_med_makstemperatur.csv", encoding="utf-8-sig") as fil:
    leser = csv.DictReader(fil, delimiter=";")

    for rad in leser:

        if rad["Stasjon"] == "SN18700":

            dato = rad["Tid(norsk normaltid)"]
            aarstall = int(dato[-4:])

            temperatur = float(rad["Maksimumstemperatur (døgn)"].replace(",", "."))

            if aarstall not in aar:
                aar.append(aarstall)
                sommerdager.append(0)
                hoysommerdager.append(0)
                tropedager.append(0)

            plass = aar.index(aarstall)

            if temperatur > 20:
                sommerdager[plass] += 1

            if temperatur > 25:
                hoysommerdager[plass] += 1

            if temperatur > 30:
                tropedager[plass] += 1

# Lager grafen
plt.plot(aar, sommerdager, label="Sommerdager")
plt.plot(aar, hoysommerdager, label="Høysommerdager")
plt.plot(aar, tropedager, label="Tropedager")

plt.xlabel("År")
plt.ylabel("Antall dager")
plt.title("Varme dager ved Oslo Blindern")
plt.legend()
plt.grid()
plt.show()
