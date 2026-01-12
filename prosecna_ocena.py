# ============================================
# vezbe.py - Student data processing
# ============================================

# Učitavanje CSV fajla
def ucitaj(staza):
    try:
        with open(staza, 'r', encoding='utf-8') as unos:
            sadrzaj = unos.read().strip()
            redovi = sadrzaj.split('\n')
            rezultat = []
            print(redovi)
            for red in redovi[1:]:  # preskače zaglavlje
                podaci = red.split(',')
                rezultat.append(tuple(podaci))
            return rezultat
    except Exception as e:
        print('Greška u učitavanju:', e)
        return None


# Provera da li je ocena ispravna (1–10)
def ispravna_ocena(tekst):
    try:
        return 5 <= int(tekst.strip()) <= 10
    except:
        return False


# Štampa podatke o studentima (lista torki)
def stampa(studenti):
    if studenti is None:
        print("Nema podataka za prikaz.")
        return
    for student in studenti:
        print('\t'.join(student))
    print('=' * 80)


# Računanje prosečne ocene svakog studenta
def prosecna_ocena(studenti):
    rezultat = []
    for student in studenti:
        ocene = student[3:7]
        ocene_broj = [int(o) for o in ocene if ispravna_ocena(o)]
        if ocene_broj:
            prosek = sum(ocene_broj) / len(ocene_broj)
        else:
            prosek = 0
        rezultat.append((prosek, *student))
    # Sortiramo po proseku opadajuće
    rezultat.sort(reverse=True)
    return rezultat


# Glavni deo
if __name__ == '__main__':
    studenti = ucitaj('ulaz.csv')
    stampa(studenti)
    rezultati = prosecna_ocena(studenti)
    for r in rezultati:
        print(r)
