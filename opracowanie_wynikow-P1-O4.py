import numpy as np
import matplotlib.pyplot as plt


STEZENIA = np.array([0, 2, 4, 6, 8, 10])

POMIARY = np.array([
    [1.00, 1.15, 0.85],
    [2.00, 2.30, 2.25],
    [3.70, 3.50, 3.45],
    [4.90, 5.30, 4.85],
    [6.45, 6.45, 6.35],
    [7.80, 7.85, 7.65],
])

POMIARY_Cx = np.array([4.35, 4.40, 4.30])

ILOSC_SERII = len(STEZENIA)
ILOSC_POMIAROW_W_SERII = len(POMIARY[0])
WSPOLCZYNNIK_STUDENTA_FISCHERA = 1.321

srednie_katy = np.mean(POMIARY, axis=1)
niepewnosc_ua = ( np.std(POMIARY, axis=1, ddof=1) * WSPOLCZYNNIK_STUDENTA_FISCHERA ) / np.sqrt(ILOSC_POMIAROW_W_SERII)

SKALA_POMIAROW = 0.05

niepewnosc_ub = SKALA_POMIAROW / np.sqrt(3)

niepewnosc_calkowita = np.sqrt(niepewnosc_ua ** 2 + niepewnosc_ub ** 2)

# stezenia  - oś X
#     katy  - oś Y

S_x = np.sum(STEZENIA)
S_y = np.sum(srednie_katy)
S_xx = np.sum(STEZENIA ** 2)
S_xy = np.sum(STEZENIA * srednie_katy)

wyznacznik_mianownik = ILOSC_SERII * S_xx - S_x ** 2

# nachylenie prostej
a = (((ILOSC_SERII * S_xy) - (S_x * S_y))
     / wyznacznik_mianownik)

# przeciecie prostej
b = (((S_xx * S_y) - (S_x * S_xy))
     / wyznacznik_mianownik)

epsilon = srednie_katy - a * STEZENIA - b
S_ee = np.sum(epsilon ** 2)

ua_nachylenia = np.sqrt(   (ILOSC_SERII/(ILOSC_SERII - 2))
                         * (S_ee / wyznacznik_mianownik) )

ub_nachylenia = np.sqrt(   (1/(ILOSC_SERII - 2))
                         * ((S_xx * S_ee) / wyznacznik_mianownik) )

srednia_Cx = np.mean(POMIARY_Cx)

Cx = (srednia_Cx - b) / a

odchylenie_Cx = np.std(POMIARY_Cx, ddof=1) * WSPOLCZYNNIK_STUDENTA_FISCHERA / np.sqrt(ILOSC_POMIAROW_W_SERII)

u_Cx = np.sqrt( odchylenie_Cx ** 2 + niepewnosc_ub ** 2)

# wzor na prawo propagacji niepewnosci
u_calkowita_Cx = np.sqrt(   ((1/a)*u_Cx ) ** 2
                          + ((-1/a) * ub_nachylenia) ** 2
                          + ((-Cx/a) * ua_nachylenia) ** 2 )

#
#
# rysowanie wykresu

plt.figure(figsize=(8, 6), dpi=500)
plt.plot(STEZENIA, a * STEZENIA + b,
         color='forestgreen', label="Prosta regresji liniowej")
plt.errorbar(STEZENIA, srednie_katy, niepewnosc_calkowita,
             fmt='o', capsize=4, color='navy', ecolor='navy', markersize=5, label="Pomiary laboratoryjne")
plt.errorbar(Cx, srednia_Cx, xerr=u_calkowita_Cx, yerr=u_Cx,
             fmt='o', capsize=4, color='orangered', ecolor='orangered', markersize=5, label="Wyznaczone stężenie Cx")

plt.xlabel("Stężenie sacharozy w roztworze[%]")
plt.ylabel("Kąt skręcenia [°]")
plt.title("Zależność kąta skręcenia polaryzacji płaszczyzny od stężenia roztworu sacharozy")

plt.legend()
plt.grid(True)


plt.savefig('wykres.png')

print("% --- KOD LATEX DO SKOPIOWANIA ---\n")

print("\\begin{table}[h]")
print("\\centering")
print("\\caption{Wyniki pomiarów kąta skręcenia płaszczyzny polaryzacji dla poszczególnych stężeń.}")
print("\\begin{tabular}{|c|c|c|c|c|c|}")
print("\\hline")
print("Stężenie $C$ [\\%] & $\\alpha_1$ [$^\\circ$] & $\\alpha_2$ [$^\\circ$] & $\\alpha_3$ [$^\\circ$] & $\\alpha_{sr}$ [$^\\circ$] & $u(\\alpha_{sr})$ [$^\\circ$] \\\\")
print("\\hline")

# Pętla generująca wiersze tabeli dla znanych stężeń
for i in range(ILOSC_SERII):
    print(f"{STEZENIA[i]} & {POMIARY[i][0]:.2f} & {POMIARY[i][1]:.2f} & {POMIARY[i][2]:.2f} & {srednie_katy[i]:.3f} & {niepewnosc_calkowita[i]:.4f} \\\\")

print("\\hline")
# Wiersz dla roztworu o nieznanym stężeniu Cx
print(f"$C_x$ & {POMIARY_Cx[0]:.2f} & {POMIARY_Cx[1]:.2f} & {POMIARY_Cx[2]:.2f} & {srednia_Cx:.3f} & {u_calkowita_Cx:.4f} \\\\")
print("\\hline")
print("\\end{tabular}")
print("\\end{table}")

print("\n% --- WYNIKI REGRESJI I OBLICZEŃ ---\n")

print("Równanie prostej regresji liniowej $y = ax + b$ dla uzyskanych danych posiada następujące parametry:")
print("\\begin{itemize}")
print(f"    \\item Współczynnik kierunkowy: $a = {a:.4f} \\pm {ua_nachylenia:.4f}$ [\\textsuperscript{{\\circ}}/\\%]")
print(f"    \\item Wyraz wolny: $b = {b:.4f} \\pm {ub_nachylenia:.4f}$ [\\textsuperscript{{\\circ}}]")
print("\\end{itemize}")

print("\nPo przekształceniu wzoru i podstawieniu średniego kąta dla nieznanego roztworu, otrzymano stężenie:")
print(f"$$C_x = {Cx:.2f} \\pm {u_Cx:.2f} \\% $$")