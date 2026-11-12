import csv
import matplotlib.pyplot as plt

# Alle CSV-filene
filer = [
    "sinnes_2014_2025_med_makstemperatur.csv",
    "oslo_blindern_1954_2025_med_makstemperatur.csv",
    "roeros_1954_2025_med_makstemperatur.csv",
    "tromsoe_1954_2025_med_makstemperatur.csv",
    "vaernes_1954_2025_med_makstemperatur.csv",
    "venabu_1954_2025_med_makstemperatur.csv"
]

# Dictionaries som lagrer temperatur og antall dager
temperatur_sum = {}
antall_dager = {}

# Leser inn alle filene
for filnavn in filer:

    with open(filnavn, "r", encoding="utf-8-sig") as fil:
        leser = csv.DictReader(fil, delimiter=";")

        for rad in leser:

            stasjon = rad["Navn"]
            dato = rad["Tid(norsk normaltid)"]
            temperatur = rad["Middeltemperatur (døgn)"]

            # Hopper over rader uten temperatur
            if temperatur == "" or temperatur == "-":
                continue

            # Finner årstallet fra datoen
            dato = dato.split()[0]

            if dato[:4].isdigit():
                aar = dato[:4]
            else:
                aar = dato[-4:]

            # Gjør om temperatur fra tekst til tall
            temperatur = float(temperatur.replace(",", "."))

            # Lager en nøkkel for hver stasjon og hvert år
            nøkkel = (stasjon, aar)

            # Oppretter plass i dictionary hvis nøkkelen ikke finnes
            if nøkkel not in temperatur_sum:
                temperatur_sum[nøkkel] = 0
                antall_dager[nøkkel] = 0

            # Legger sammen temperaturene og teller dagene
            temperatur_sum[nøkkel] += temperatur
            antall_dager[nøkkel] += 1


# Regner ut gjennomsnitt for hvert år
gjennomsnitt = {}

for nøkkel in temperatur_sum:

    if antall_dager[nøkkel] >= 300:

        gjennomsnitt[nøkkel] = (
            temperatur_sum[nøkkel] / antall_dager[nøkkel]
        )


# Plotter gjennomsnittstemperaturen for hver værstasjon
stasjoner = set()

for stasjon, aar in gjennomsnitt:
    stasjoner.add(stasjon)

#går gjennom en værstasjon av gangen
for stasjon in stasjoner:

    aarstall = []
    temperaturer = []

#Går gjennom alle årsgjennomsnittene
    for nøkkel in gjennomsnitt:

        if nøkkel[0] == stasjon:
            aarstall.append(int(nøkkel[1]))
            temperaturer.append(gjennomsnitt[nøkkel])

    # Sorterer årstallene i riktig rekkefølge
    sortert = sorted(zip(aarstall, temperaturer))

    aarstall = [rad[0] for rad in sortert]
    temperaturer = [rad[1] for rad in sortert]

    plt.plot(aarstall, temperaturer, marker="o", label=stasjon)


# Lager diagrammet
plt.xlabel("År")
plt.ylabel("Gjennomsnittstemperatur (°C)")
plt.title("Årlig gjennomsnittstemperatur for værstasjonene")
plt.legend()
plt.grid()
plt.show()
