import csv
import matplotlib.pyplot as plt
from pathlib import Path

# Finner CSV-filen i samme mappe som programmet
mappe = Path(__file__).resolve().parent
filnavn = mappe / 'oslo_blindern_1954_2025_med_makstemperatur.csv'

vind = [[] for i in range(12)]

with open(filnavn, encoding='utf-8-sig') as fil:
    for rad in csv.DictReader(fil, delimiter=';'):
        dato = rad['Tid(norsk normaltid)']
        styrke = rad['Høyeste middelvind (døgn)']
        if not dato or not styrke or styrke == '-':
            continue
        maaned = int(dato.split('.')[1])
        vind[maaned - 1].append(float(styrke.replace(',', '.')))

minimum = []
median = []
maksimum = []

for liste in vind:
    liste.sort()
    if len(liste) == 0:
        minimum.append(None)
        median.append(None)
        maksimum.append(None)
        continue
    minimum.append(liste[0])
    maksimum.append(liste[-1])
    midten = len(liste) // 2
    if len(liste) % 2 == 1:
        median.append(liste[midten])
    else:
        median.append((liste[midten - 1] + liste[midten]) / 2)

maaneder = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun',
            'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des']

plt.plot(maaneder, minimum, label='Minimum', marker='o')
plt.plot(maaneder, median, label='Median', marker='o')
plt.plot(maaneder, maksimum, label='Maksimum', marker='o')
plt.title('Vindstyrke per måned – Oslo Blindern')
plt.xlabel('Måned')
plt.ylabel('Vindstyrke (m/s)')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(mappe / 'vindstatistikk.png')
plt.show()