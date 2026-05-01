#!/usr/bin/env python3
import numpy as np


POLOZENIA_SOCZEWKA_1_POWIEKSZONE = np.array([
        [19.8, 20.2, 20.1],
        [19.1, 19.2, 19.0],
        [20.2, 20.4, 20.5]
        ])

POLOZENIA_SOCZEWKA_2_POWIEKSZONE = np.array([
        [28.2, 28.0, 28.4],
        [25.8, 26.0, 25.7],
        [25.3, 25.4, 25.5]
        ])

POLOZENIA_SOCZEWKA_3_POWIEKSZONE = np.array([
        [48.0, 47.9, 48.0],
        [45.5, 45.8, 45.7],
        [46.8, 47.0, 46.9]
        ])

POLOZENIA_SOCZEWKA_1_POMNIEJSZONE = np.array([
        [44.9, 44.4, 44.6],
        [64.0, 64.3, 64.2],
        [32.9, 33.1, 33.0]
        ])

POLOZENIA_SOCZEWKA_2_POMNIEJSZONE = np.array([
        [45.6, 45.4, 45.5],
        [66.0, 66.3, 66.1],
        [77.0, 77.1, 76.9]
        ])

POLOZENIA_SOCZEWKA_3_POMNIEJSZONE = np.array([
        [85.6, 86.0, 85.8],
        [97.4, 97.6, 97.3],
        [91.4, 91.4, 91.7]
        ])

POLOZENIA_SOCZEWKA_ROZPRASZAJACA = np.array([
        86.5, 
        85.8, 
        86.2
        ])

POLOZENIA_EKRANU_1 = np.array([51.6, 70.7, 41.1])
POLOZENIA_EKRANU_2 = np.array([61.5, 79.3, 90.0])
POLOZENIA_EKRANU_3 = np.array([121.0, 130.5, 125.0])

POLOZENIE_EKRANU_ROZPRASZAJACA = 98.5

ODLEGLOSC_OBIEKTU = 13.5

WSP_STUDENTA_FISCHERA = 1.321

ILOSC_POMIAROW = 3

def metoda_bezposrednia(polozenia_soczewek, polozenia_ekranu):
    srednie_polozenia = np.mean(polozenia_soczewek, axis=1)
    ogniskowe = []
    for i in range(0, 2):
        x = srednie_polozenia[i] - ODLEGLOSC_OBIEKTU
        y = polozenia_ekranu[i] - srednie_polozenia[i]
        f = (x*y)/(x+y)
        ogniskowe.append(f)
    srednia_ogniskowa = np.mean(ogniskowe)
    odch_std = np.std(ogniskowe, ddof=1)
    ua = np.sqrt(odch_std) / np.sqrt(ILOSC_POMIAROW)
    ub = 0.1 / np.sqrt(3)
    niepewnosc_calkowita = np.sqrt(ua**2 + ub**2)
    print(f"Średnia ogniskowa wynosi {srednia_ogniskowa:.4f} cm z niepewnością {niepewnosc_calkowita:.2g}")

counter_serii = 1

def metoda_bessela(polozenia_zmniejszone, polozenia_zwiekszone, polozenia_ekranu):
    global counter_serii
    print(f"SERIA NR {counter_serii}")
    print(f"--------------------------------------")
    for i in range(0, 3):
        L = polozenia_ekranu[i] - ODLEGLOSC_OBIEKTU
        print(f"L = {L:.4f}")
        z1 = polozenia_zmniejszone[i] - ODLEGLOSC_OBIEKTU
        print(f"z1 = {np.mean(z1):.4f}")
        z2 = polozenia_zwiekszone[i] - ODLEGLOSC_OBIEKTU
        print(f"z2 = {np.mean(z2):.4f}")
        y1 = polozenia_ekranu[i] - z1
        print(f"y1 = {np.mean(y1):.4f}")
        y2 = polozenia_ekranu[i] - z2
        print(f"y2 = {np.mean(y2):.4f}")
        x1 = z1 - ODLEGLOSC_OBIEKTU
        print(f"x1 = {np.mean(x1):.4f}")
        x2 = z2 - ODLEGLOSC_OBIEKTU
        print(f"x2 = {np.mean(x2):.4f}")
        d_seria = abs(y1 - y2)
        d = np.mean(d_seria)
        print(f"d = {d:.4f}")
        f = (L**2 - d**2)/(4*L)
        print(f"Ogniskowa wynosi {f:.4f} cm")
        print("")
        counter_serii += 1
    print(f"--------------------------------------")
    print("")

print("================== METODA BEZPOŚREDNIA ==================")
print("Obraz pomniejszony:")
metoda_bezposrednia(POLOZENIA_SOCZEWKA_1_POMNIEJSZONE, POLOZENIA_EKRANU_1)
metoda_bezposrednia(POLOZENIA_SOCZEWKA_2_POMNIEJSZONE, POLOZENIA_EKRANU_2)
metoda_bezposrednia(POLOZENIA_SOCZEWKA_3_POMNIEJSZONE, POLOZENIA_EKRANU_3)
print("")
print("Obraz powiększony:")
metoda_bezposrednia(POLOZENIA_SOCZEWKA_1_POWIEKSZONE, POLOZENIA_EKRANU_1)
metoda_bezposrednia(POLOZENIA_SOCZEWKA_2_POWIEKSZONE, POLOZENIA_EKRANU_2)
metoda_bezposrednia(POLOZENIA_SOCZEWKA_3_POWIEKSZONE, POLOZENIA_EKRANU_3)


print("================== METODA BESSELA ==================")
metoda_bessela(POLOZENIA_SOCZEWKA_1_POMNIEJSZONE, POLOZENIA_SOCZEWKA_1_POWIEKSZONE, POLOZENIA_EKRANU_1)
print("")
metoda_bessela(POLOZENIA_SOCZEWKA_2_POMNIEJSZONE, POLOZENIA_SOCZEWKA_2_POWIEKSZONE, POLOZENIA_EKRANU_2)
print("")
metoda_bessela(POLOZENIA_SOCZEWKA_3_POMNIEJSZONE, POLOZENIA_SOCZEWKA_3_POWIEKSZONE, POLOZENIA_EKRANU_3)
