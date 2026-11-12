import csv
import math
from datetime import datetime

import matplotlib.pyplot as plt

# Bytt filnavn her for å bruke en annen stasjon. Alternativer:
# oslo_blindern.csv, roeros.csv, tromsoe.csv, vaernes.csv, venabu.csv
FILNAVN = "oslo_blindern.csv"

MANEDER = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun",
           "Jul", "Aug", "Sep", "Okt", "Nov", "Des"]
MIN_MALINGER_NEDBOR = 20  # må ha flere enn 20 gyldige målinger i måneden


def til_tall(tekst):
    """Gjør om f.eks. '1,4' til 1.4. Manglende verdi ('-') blir NaN."""
    tekst = tekst.strip()
    if tekst in ("", "-"):
        return float("nan")
    return float(tekst.replace(",", "."))


def gyldige(verdier):
    """Returnerer listen uten manglende verdier (NaN)."""
    return [v for v in verdier if not math.isnan(v)]


def finn_kolonne(overskrifter, nokkelord):
    """Finner indeksen til kolonnen hvis navn inneholder nøkkelordet.

    Filene har ikke samme kolonner i samme rekkefølge, så vi slår opp
    på navn i stedet for å bruke faste tall.
    """
    for i, navn in enumerate(overskrifter):
        if nokkelord.lower() in navn.lower():
            return i
    raise KeyError(f"Fant ingen kolonne som inneholder '{nokkelord}'")


def les_data(filnavn):
    """Leser en csv-fil og returnerer (stasjonsnavn, liste med (dato, temp, nedbør, vind, snø))."""
    data = []
    stasjonsnavn = filnavn
    # utf-8-sig fjerner BOM-tegnet først i filen
    with open(filnavn, encoding="utf-8-sig", newline="") as fil:
        leser = csv.reader(fil, delimiter=";")
        overskrifter = next(leser)

        i_navn = finn_kolonne(overskrifter, "navn")
        i_tid = finn_kolonne(overskrifter, "tid")
        i_temp = finn_kolonne(overskrifter, "middeltemperatur")
        i_nedbor = finn_kolonne(overskrifter, "nedbør")
        i_vind = finn_kolonne(overskrifter, "middelvind")
        i_sno = finn_kolonne(overskrifter, "snødybde")

        for rad in leser:
            try:
                # Gjør datoen fra tekst til datetime-objekt
                dato = datetime.strptime(rad[i_tid], "%d.%m.%Y")
            except (ValueError, IndexError):
                continue  # hopper over bunntekst og ugyldige rader
            stasjonsnavn = rad[i_navn]
            data.append((
                dato,
                til_tall(rad[i_temp]),
                til_tall(rad[i_nedbor]),
                til_tall(rad[i_vind]),
                til_tall(rad[i_sno]),
            ))
    data.sort(key=lambda r: r[0])  # sikrer at radene er sortert på dato
    return stasjonsnavn, data


def maanedsverdier(data, aar):
    """Regner ut verdier for hver måned (1-12) i det valgte året.

    Returnerer en liste med én ordbok per måned. Verdien er None
    hvis det ikke finnes data å regne ut fra.
    """
    resultat = []
    for maaned in range(1, 13):
        rader = [r for r in data if r[0].year == aar and r[0].month == maaned]
        temp = gyldige([r[1] for r in rader])
        nedbor = gyldige([r[2] for r in rader])
        vind = gyldige([r[3] for r in rader])
        sno = gyldige([r[4] for r in rader])

        resultat.append({
            "snø_maks": max(sno) if sno else None,
            "nedbør_total": sum(nedbor) if len(nedbor) > MIN_MALINGER_NEDBOR else None,
            "temp_maks": max(temp) if temp else None,
            "temp_min": min(temp) if temp else None,
            "vind_maks": max(vind) if vind else None,
        })
    return resultat


def skriv_tabell(verdier, stasjon, aar):
    def fmt(v):
        return "-" if v is None else f"{v:.1f}"

    print(f"\nMånedlige verdier for {stasjon}, {aar}")
    print(f"{'Mnd':<5}{'Snø maks':>10}{'Nedbør tot':>13}{'Temp maks':>11}{'Temp min':>10}{'Vind maks':>11}")
    for navn, v in zip(MANEDER, verdier):
        nedbor = "ikke reg." if v["nedbør_total"] is None else f"{v['nedbør_total']:.1f}"
        print(f"{navn:<5}{fmt(v['snø_maks']):>10}{nedbor:>13}"
              f"{fmt(v['temp_maks']):>11}{fmt(v['temp_min']):>10}{fmt(v['vind_maks']):>11}")


def stolper(ax, verdier, noekkel, farge):
    """Tegner stolper bare for måneder som har en verdi."""
    x = [m for m, v in enumerate(verdier, start=1) if v[noekkel] is not None]
    y = [v[noekkel] for v in verdier if v[noekkel] is not None]
    ax.bar(x, y, color=farge)


def plott_aar(data, stasjon, aar):
    if not any(r[0].year == aar for r in data):
        print(f"Ingen data funnet for {aar}.")
        return None

    verdier = maanedsverdier(data, aar)
    skriv_tabell(verdier, stasjon, aar)

    fig, akser = plt.subplots(4, 1, figsize=(11, 10), sharex=True)
    ax_sno, ax_nedbor, ax_temp, ax_vind = akser

    # Maks snødybde
    stolper(ax_sno, verdier, "snø_maks", "tab:blue")
    ax_sno.set_ylabel("Maks snødybde (cm)")

    # Total nedbør, med tekst der den ikke er registrert
    stolper(ax_nedbor, verdier, "nedbør_total", "tab:cyan")
    ax_nedbor.set_ylabel("Total nedbør (mm)")
    for maaned, v in enumerate(verdier, start=1):
        if v["nedbør_total"] is None:
            ax_nedbor.text(maaned, 0.02, "ikke registrert", rotation=90,
                           ha="center", va="bottom", color="gray", fontsize=8,
                           transform=ax_nedbor.get_xaxis_transform())

    # Maks og min middeltemperatur
    mnd_maks = [m for m, v in enumerate(verdier, start=1) if v["temp_maks"] is not None]
    mnd_min = [m for m, v in enumerate(verdier, start=1) if v["temp_min"] is not None]
    ax_temp.plot(mnd_maks, [verdier[m - 1]["temp_maks"] for m in mnd_maks],
                 "o-", color="tab:red", label="Maks")
    ax_temp.plot(mnd_min, [verdier[m - 1]["temp_min"] for m in mnd_min],
                 "o-", color="tab:blue", label="Min")
    ax_temp.axhline(0, color="gray", linewidth=0.8)
    ax_temp.set_ylabel("Middeltemperatur (°C)")
    ax_temp.legend()

    # Maks middelvind
    stolper(ax_vind, verdier, "vind_maks", "tab:green")
    ax_vind.set_ylabel("Maks middelvind (m/s)")

    for ax in akser:
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0.4, 12.6)  # plass til alle 12 måneder
    ax_vind.set_xticks(range(1, 13))
    ax_vind.set_xticklabels(MANEDER)
    ax_vind.set_xlabel("Måned")

    fig.suptitle(f"Månedlige værdata for {stasjon}, {aar}")
    fig.tight_layout()
    return fig

def main():
    stasjon, data = les_data(FILNAVN)
    forste, siste = data[0][0].year, data[-1][0].year

    while True:
        try:
            aar = int(input(f"Skriv inn et årstall ({forste}-{siste}): "))
            break
        except ValueError:
            print("Ugyldig input, skriv et heltall.")

    fig = plott_aar(data, stasjon, aar)
    if fig:
        plt.show()

if __name__ == "__main__":
    main()