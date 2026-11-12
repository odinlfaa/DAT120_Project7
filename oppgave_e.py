
import csv
import os
from datetime import date, datetime
 
# Finner table.csv i samme mappe som denne filen, uansett hvor du kjører fra
MAPPE = os.path.dirname(os.path.abspath(__file__))
FILNAVN = os.path.join(MAPPE, "table.csv")
 
data = []  # liste med (dato, snødybde)
with open(FILNAVN, encoding="utf-8-sig", newline="") as f:
    for rad in csv.DictReader(f, delimiter=";"):
        try:
            dato = datetime.strptime(rad["Tid(norsk normaltid)"], "%d.%m.%Y").date()
            sno = float(rad["Snødybde"].replace(",", "."))
        except (ValueError, KeyError, AttributeError):
            continue  # hopper over rader uten dato eller uten måling ("-")
        data.append((dato, sno))
 
 
def skiforedager(aar):
    """Antall dager med snødybde >= 20 cm, 1. nov (aar-1) til 31. mai (aar)."""
    start = date(aar - 1, 11, 1)
    slutt = date(aar, 5, 31)
    return sum(1 for dato, sno in data if start <= dato <= slutt and sno >= 20)
 
 
aar = int(input("Skriv inn årstall: "))
print(f"Det var skiføre i {skiforedager(aar)} dager i skisesongen {aar - 1}/{aar}.")