
import csv
from datetime import date
import matplotlib.pyplot as plt

# Våre fem værstasjoner
filer = {
    "Oslo": "oslo_blindern_1954_2025_med_makstemperatur.csv",
    "Røros": "roeros_1954_2025_med_makstemperatur.csv",
    "Tromsø": "tromsoe_1954_2025_med_makstemperatur.csv",
    "Værnes": "vaernes_1954_2025_med_makstemperatur.csv",
    "Venabu": "venabu_1954_2025_med_makstemperatur.csv"
}

resultater = {}

for stasjon, filnavn in filer.items():
    maalinger = {}
    skidager = {}

    with open(filnavn, encoding="utf-8-sig") as fil:
        for rad in csv.DictReader(fil, delimiter=";"):
            dato = rad["Tid(norsk normaltid)"]
            sno = rad["Snødybde"]

            # Hopper over manglende data
            if not dato or not sno.isdigit():
                continue

            deler = dato.split(".")
            maaned = int(deler[1])
            aar = int(deler[2])

            # Bare november til mai
            if maaned not in [11, 12, 1, 2, 3, 4, 5]:
                continue

            # November og desember tilhører neste sesong
            if maaned >= 11:
                aar += 1

            # Teller målinger og skidager
            maalinger[aar] = maalinger.get(aar, 0) + 1

            if int(sno) >= 20:
                skidager[aar] = skidager.get(aar, 0) + 1

    resultater[stasjon] = {}

    # Sjekker om minst halvparten av dagene har data
    for aar in maalinger:
        dager = (date(aar, 6, 1) - date(aar - 1, 11, 1)).days

        if maalinger[aar] >= dager / 2:
            resultater[stasjon][aar] = skidager.get(aar, 0)


# Brukeren velger år
valgt_aar = int(input("Skriv inn årstall: "))

print("Skisesongen", valgt_aar - 1, "til", valgt_aar)

for stasjon, sesonger in resultater.items():
    if valgt_aar in sesonger:
        print(stasjon, ":", sesonger[valgt_aar], "skidager")
    else:
        print(stasjon, ": Ikke nok data")


# Lager graf for alle værstasjonene
for stasjon, sesonger in resultater.items():
    aarstall = range(min(sesonger), max(sesonger) + 1)
    antall = []

    for aar in aarstall:
        antall.append(sesonger.get(aar))

    plt.plot(aarstall, antall, label=stasjon)

plt.title("Antall dager med skiføre")
plt.xlabel("Skisesong")
plt.ylabel("Antall dager")
plt.legend()
plt.grid()
plt.show()
