import csv
from datetime import datetime

FIL = "sinnes_2014_2025.csv"

# Les inn data: (dato, nedbør). Manglende verdier ("-" eller tomt) blir None.
data = []
with open(FIL, encoding="UTF-8-sig", newline="") as f:
    leser = csv.reader(f, delimiter=";")
    next(leser)  # hopp over overskriftslinjen
    for rad in leser:
        if len(rad) < 5:
            continue
        try:
            dato = datetime.strptime(rad[2], "%d.%m.%Y")
        except ValueError:
            continue  # hopp over linjer uten gyldig dato (f.eks. kildehenvisning nederst)
        try:
            nedbor = float(rad[4].replace(",", "."))
        except ValueError:
            nedbor = None
        data.append((dato, nedbor))

def hent_dato(x):
    return x[0]

data.sort(key=hent_dato)

# Finn lengste sammenhengende periode der døgnnedbør er 0.
# Manglende verdier regnes ikke som 0 og avbryter perioden.
beste_lengde = 0
beste_start = None
beste_slutt = None

lengde = 0
start = None
forrige = None

for dato, nedbor in data:
    if nedbor == 0:
        # Fortsetter perioden hvis forrige dag også var tørr og datoene henger sammen
        if lengde > 0 and (dato - forrige).days == 1:
            lengde += 1
        else:
            lengde = 1
            start = dato
        forrige = dato

        if lengde > beste_lengde:
            beste_lengde = lengde
            beste_start = start
            beste_slutt = dato
    else:
        lengde = 0

print(f"Lengde:     {beste_lengde} dager")
print(f"Startdato:  {beste_start.strftime('%d.%m.%Y')}")
print(f"Sluttdato:  {beste_slutt.strftime('%d.%m.%Y')}")