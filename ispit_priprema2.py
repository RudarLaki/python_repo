# a) Funkcija UCITAJ_EKSPERIMENTE(N)
def ucitaj_eksperimente(N):
    if N <= 0:
        return None
    rezultat = {}
    for _ in range(N):
        oznaka = input("Oznaka: ")
        broj_pokusaja = int(input("Broj pokusaja (>0): "))
        procenat = float(input("Procenat uspeha [0-100]: "))
        rezultat[oznaka] = [broj_pokusaja, procenat]
    return rezultat

# b) Funkcija OBRADI_EKSPERIMENTE(RE, prag)
def obradi_eksperimente(RE, prag):
    if not RE:
        return None
    for oznaka, vrednosti in RE.items():
        broj_pokusaja, procenat = vrednosti
        uspeh = round(broj_pokusaja * procenat / 100)
        if procenat >= prag:
            stabilnost = "stabilan"
        elif procenat >= 0.6 * prag:
            stabilnost = "na_oprezu"
        else:
            stabilnost = "kritican"
        RE[oznaka].extend([uspeh, stabilnost])
    return RE

# c) Funkcija NAJVISE_NUSPOJAVA(RE)
def najvise_nuspojava(RE):
    if not RE:
        return None
    max_uspeh = -1
    oznaka_max = None
    for oznaka, vrednosti in RE.items():
        # pretpostavimo da je uspeh na poziciji 2 posle obrade
        uspeh = vrednosti[2] if len(vrednosti) > 2 else 0
        if uspeh > max_uspeh:
            max_uspeh = uspeh
            oznaka_max = oznaka
    return oznaka_max

# d) Iterativna funkcija BALANSIRAJ_IT(lista_brojeva)
def balansiraj_it(lista):
    zbir = 0
    for i in range(len(lista)):
        zbir += lista[i]
        if zbir < 0:
            # povećaj element da bi zbir bio 0
            lista[i] += -zbir
            zbir = 0
    return lista

# e) Rekurzivna funkcija BALANSIRAJ_REK(lista_brojeva)
def balansiraj_rek(lista, i=0, zbir=0):
    if i == len(lista):
        return lista
    zbir += lista[i]
    if zbir < 0:
        lista[i] += -zbir
        zbir = 0
    return balansiraj_rek(lista, i+1, zbir)

# f) Funkcija OBRADI_DNEVNIKE(putanja, rezim)
def obradi_dnevnike(putanja, rezim):
    try:
        with open(putanja, 'r') as f:
            saldo = []
            for line in f:
                brojevi = list(map(int, line.strip().split()))
                # formiranje trenutnog salda
                if not saldo:
                    saldo = brojevi
                else:
                    saldo = [x + y for x, y in zip(saldo, brojevi)]
            print(f"Saldo pre balansiranja: {saldo}")
            if rezim == "iter":
                saldo = balansiraj_it(saldo)
            elif rezim == "rek":
                saldo = balansiraj_rek(saldo)
            else:
                print("Nepoznat režim, koristite 'iter' ili 'rek'")
                return
            print(f"Saldo posle balansiranja ({rezim}): {saldo}")
    except Exception as e:
        print(f"Greška u čitanju datoteke: {e}")

# --- Primer poziva funkcija ---

if __name__ == "__main__":
    # a) UCITAJ_EKSPERIMENTE
    print("--- Učitavanje eksperimenata ---")
    N = int(input("Unesite broj eksperimenata: "))
    eksperimenti = ucitaj_eksperimente(N)
    print("Učitani eksperimenti:", eksperimenti)

    # b) OBRADI_EKSPERIMENTE
    prag = float(input("Unesite prag stabilnosti: "))
    obradi_eksperimente(eksperimenti, prag)
    print("Obrađeni eksperimenti:", eksperimenti)

    # c) NAJVISE_NUSPOJAVA
    oznaka_max = najvise_nuspojava(eksperimenti)
    print(f"Najviše nuspojava ima eksperiment: {oznaka_max}")

    # d) BALANSIRAJ_IT
    print("--- Testiranje balansiranja iterativno ---")
    lista = [3, -5, 2, -1, 4]
    print(f"Original lista: {lista}")
    print(f"Balansirana lista: {balansiraj_it(lista[:])}")  # Koristimo kopiju liste

    # e) BALANSIRAJ_REK
    print("--- Testiranje balansiranja rekurzivno ---")
    print(f"Original lista: {lista}")
    print(f"Balansirana lista: {balansiraj_rek(lista[:])}")

    # # f) OBRADI_DNEVNIKE
    # print("--- Obrada dnevnika ---")
    # putanja = input("Unesite putanju do dnevnika: ")
    # rezim = input("Unesite režim ('iter' ili 'rek'): ")
    # obradi_dnevnike(putanja, rezim)
