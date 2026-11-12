import os
import matplotlib.pyplot as plt

# Gå til mappen der scriptet ligger, så filen blir funnet
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# En liste for hver måned (indeks 0 = januar)
vind = [[] for _ in range(12)]

# Les filen linje for linje
for linje in open("oslo_blindern_1954_2025_med_makstemperatur.csv", encoding="utf-8-sig"):
    deler = linje.strip().split(";")
    try:
        maaned = int(deler[2].split(".")[1])         # dato er dd.mm.åååå
        verdi = float(deler[6].replace(",", "."))    # komma -> punktum
    except (ValueError, IndexError):
        continue  # hopper over overskrift, bunntekst og manglende verdier
    vind[maaned - 1].append(verdi)

def median(liste):
    s = sorted(liste)
    midt = len(s) // 2
    if len(s) % 2 == 1:
        return s[midt]
    return (s[midt - 1] + s[midt]) / 2

# Minimum, median og maksimum for hver måned
minimum = [min(v) for v in vind]
medianer = [median(v) for v in vind]
maksimum = [max(v) for v in vind]

# Plott
plt.plot(range(1, 13), minimum, label="Minimum")
plt.plot(range(1, 13), medianer, label="Median")
plt.plot(range(1, 13), maksimum, label="Maksimum")
plt.xlabel("Måned")
plt.ylabel("Vindstyrke (m/s)")
plt.title("Oslo - Blindern: vindstyrke per måned")
plt.legend()
plt.show()