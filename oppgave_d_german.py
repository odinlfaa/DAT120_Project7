import csv
import matplotlib.pyplot as plt
from pathlib import Path

# Finner CSV-filen i samme mappe som programmet
mappe = Path(__file__).resolve().parent
filnavn = mappe / 'oslo_blindern_1954_2025_med_makstemperatur.csv'

# Lager en liste for hver måned (indeks 0 = januar)
vind = [[] for i in range(12)]

# Åpner filen og leser den rad for rad, der kolonnene er delt med semikolon
with open(filnavn, encoding='utf-8-sig') as fil:
    for rad in csv.DictReader(fil, delimiter=';'):
        # Henter ut dato og vindstyrke fra riktig kolonne
        dato = rad['Tid(norsk normaltid)']
        styrke = rad['Høyeste middelvind (døgn)']
        # Hopper over rader der noe mangler
        if not dato or not styrke or styrke == '-':
            continue
        # Henter ut måneden fra datoen (dd.mm.åååå)
        maaned = int(dato.split('.')[1])
        # Bytter komma med punktum og legger verdien i riktig månedsliste
        vind[maaned - 1].append(float(styrke.replace(',', '.')))

# Lister som skal inneholde resultatene for hver måned
minimum = []
median = []
maksimum = []

# Går gjennom hver måned og finner minimum, median og maksimum
for liste in vind:
    # Sorterer verdiene fra lavest til høyest
    liste.sort()
    # Hvis måneden ikke har data, legges det inn None
    if len(liste) == 0:
        minimum.append(None)
        median.append(None)
        maksimum.append(None)
        continue
    # Første verdi er minimum, siste er maksimum
    minimum.append(liste[0])
    maksimum.append(liste[-1])
    # Medianen er verdien i midten (eller snittet av de to i midten)
    midten = len(liste) // 2
    if len(liste) % 2 == 1:
        median.append(liste[midten])
    else:
        median.append((liste[midten - 1] + liste[midten]) / 2)

# Navn på månedene som vises på x-aksen
maaneder = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun',
            'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des']

# Tegner én linje for minimum, median og maksimum
plt.plot(maaneder, minimum, label='Minimum', marker='o')
plt.plot(maaneder, median, label='Median', marker='o')
plt.plot(maaneder, maksimum, label='Maksimum', marker='o')
# Setter tittel og navn på aksene
plt.title('Vindstyrke per måned – Oslo Blindern')
plt.xlabel('Måned')
plt.ylabel('Vindstyrke (m/s)')
# Viser forklaringsboks og rutenett
plt.legend()
plt.grid()
# Justerer layouten så ingenting kuttes
plt.tight_layout()
# Lagrer grafen som bildefil og viser den på skjermen
plt.savefig(mappe / 'vindstatistikk.png')
plt.show()