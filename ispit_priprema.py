import csv

# ============================================
# a) UCITAJ_PROIZVODE iz CSV fajla
# ============================================
def ucitaj_proizvode(staza):
    try:
        with open(staza, 'r', encoding='utf-8') as unos:
            sadrzaj = unos.read().strip()
            redovi = sadrzaj.split('\n')
            rezultat = {}
            print(redovi)
            for red in redovi[1:]:  # preskačemo zaglavlje
                podaci = red.split(',')
                # očekujemo format: oznaka, cena, kolicina
                oznaka = podaci[0].strip()
                cena = float(podaci[1])
                kolicina = int(podaci[2])
                rezultat[oznaka] = [cena, kolicina]
            return rezultat
    except Exception as e:
        print("Greška u učitavanju:", e)
        return None


# ============================================
# b) OBELEZI_ZALIHE
# ============================================
def OBELEZI_ZALIHE(RP, L, U):
    for oznaka, podaci in RP.items():
        cena, kol = podaci
        ukupno = round(cena * kol, 2)
        if kol < L:
            status = "nisko"
        elif kol > U:
            status = "visoko"
        else:
            status = "srednje"
        RP[oznaka] = [cena, kol, ukupno, status]
    return RP


# ============================================
# c) MAX_VREDNOST
# ============================================
def MAX_VREDNOST(RP):
    max_oznaka = None
    max_vrednost = -1
    for oznaka, podaci in RP.items():
        vrednost = podaci[2]
        if vrednost > max_vrednost:
            max_vrednost = vrednost
            max_oznaka = oznaka
    return max_oznaka


# ============================================
# d) TALAS_IT
# ============================================
def TALAS_IT(lista):
    for i in range(1, len(lista)):
        if i % 2 == 1 and lista[i] > lista[i - 1]:
            lista[i], lista[i - 1] = lista[i - 1], lista[i]
        elif i % 2 == 0 and lista[i] < lista[i - 1]:
            lista[i], lista[i - 1] = lista[i - 1], lista[i]
    return lista


# ============================================
# e) TALAS_REK
# ============================================
def TALAS_REK(lista, i=1):
    if i >= len(lista):
        return lista
    if i % 2 == 1 and lista[i] > lista[i - 1]:
        lista[i], lista[i - 1] = lista[i - 1], lista[i]
    elif i % 2 == 0 and lista[i] < lista[i - 1]:
        lista[i], lista[i - 1] = lista[i - 1], lista[i]
    return TALAS_REK(lista, i + 1)


# ============================================
# TEST PRIMER
# ============================================

if __name__ == "__main__":
    RP = ucitaj_proizvode("ulaz2.csv")
    print(RP)

    print("\n--- Učitani proizvodi ---")
    for k, v in RP.items():
        print(k, v)

    RP = OBELEZI_ZALIHE(RP, L=10, U=40)

    print("\n--- Nakon obeležavanja zaliha ---")
    for k, v in RP.items():
        print(k, v)

    najv = MAX_VREDNOST(RP)
    print("\nProizvod sa najvećom vrednošću zaliha:", najv)

    lista1 = [3, 1, 4, 2, 2]
    print("\nTalas IT:", TALAS_IT(lista1.copy()))
    print("Talas REK:", TALAS_REK(lista1.copy()))
