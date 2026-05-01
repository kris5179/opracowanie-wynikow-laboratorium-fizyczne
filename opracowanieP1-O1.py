import numpy as np
import math
import matplotlib.pyplot as plt

POMIARY_PRYZMAT_1 = np.array([
    [23.5, 24.0],
    [23.7, 24.1],
    [23.3, 24.8],
    [22.9, 23.9],
    [23.5, 23.8]
        ])
POMIARY_PRYZMAT_2 = np.array([
    [38.2, 38.9],
    [37.6, 39.0],
    [38.4, 38.4],
    [38.1, 38.6],
    [38.3, 38.5]
           ])
POMIARY_PRYZMAT_3 = np.array([
    [48.0, 48.3],
    [48.1, 48.5],
    [48.9, 48.4],
    [48.2, 48.1],
    [47.9, 48.5],
        ])


WSP_STUDENTA_FISHERA = 1.141
POMIAROW_W_SERII = 5

PODZIALKA_STOLIKA = 0.1


NIEPEWNOSC_STOLIKA = PODZIALKA_STOLIKA / np.sqrt(3)
NIEPEWNOSC_UB_KAT_DELTA = np.sqrt( (NIEPEWNOSC_STOLIKA ** 2) )

PHI = 60

def obliczenia(pomiary, nazwa_pryzmatu):
    print(f"========== {nazwa_pryzmatu} ==========")
    katy_delta = np.mean(pomiary, axis=1)
    i = 1
    for kat in katy_delta:
        print(f"{i}): {kat:.2f}")
        i += 1
    sredni_kat_delta = np.mean(katy_delta)
    print(f"Średni kąt delta : {sredni_kat_delta}")

    odch_stand_sr_kat_delta = np.std(katy_delta, ddof=1)
    print(f"Odchylenie standardowe średniego kąta delta : {odch_stand_sr_kat_delta:.2g}")

    niepewnosc_ua_kat_delta = odch_stand_sr_kat_delta * WSP_STUDENTA_FISHERA / np.sqrt(POMIAROW_W_SERII)
    print(f"Niepewność ua dla kąta delta : {niepewnosc_ua_kat_delta:.2g}")
    print(f"Niepewność ub dla kąta delta : {NIEPEWNOSC_UB_KAT_DELTA:.2g}")

    niepewnosc_calkowita_kat_delta = np.sqrt( (niepewnosc_ua_kat_delta ** 2) + (NIEPEWNOSC_UB_KAT_DELTA ** 2) )
    print(f"Niepewność całkowita dla kąta delta : {niepewnosc_calkowita_kat_delta:.2g}")

    print(f"Zatem końcowy wynik to: {sredni_kat_delta} stopnia, z niepewnością {niepewnosc_calkowita_kat_delta:.2g}")
    
    kat_w_liczniku = np.radians( (PHI + sredni_kat_delta)/2 )
    kat_w_mianowniku = np.radians( (PHI)/2 )
    n = (np.sin(kat_w_liczniku)) / (np.sin(kat_w_mianowniku))

    print(f"Współczynnik załamania światła : {n:.5g}")

    pochodna_delta =  ((np.cos(kat_w_liczniku)) / (2 * np.sin(kat_w_mianowniku))) * niepewnosc_calkowita_kat_delta
    pochodna_phi = ((np.cos(kat_w_liczniku) * np.sin(kat_w_mianowniku)) - (np.sin(kat_w_liczniku) * np.cos(kat_w_mianowniku))) / (2 * (np.sin(kat_w_mianowniku) ** 2))

    propagacja_niepewnosci = np.sqrt(((pochodna_delta * niepewnosc_calkowita_kat_delta) ** 2) + ((pochodna_phi * 0) ** 2))
    print(f"Niepewność współczynnika załamania światła : {propagacja_niepewnosci:.2g}")

    print("")


obliczenia(POMIARY_PRYZMAT_1, "PRYZMAT Z WODĄ") 
obliczenia(POMIARY_PRYZMAT_2, "PRYZMAT ZE SZKŁA TYPU CROWN") 
obliczenia(POMIARY_PRYZMAT_3, "PRYZMAT ZE SZKŁA FLINTOWEGO") 
