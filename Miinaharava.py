import sys
import time
import random

def kysele_tiedot():
    '''Kyselee tietoja sek‰ koostaa niist‰ tiedostoon kirjoitettavan merkkijonon.'''
    tiedot = "Pelaajan nimi: {n}\n".format(n=nimi)
    rivi = "Tulos: {v}, Kentt‰: {k}, Miinat: {m}, Pvm: {p}, Aika: {km} minuuttia, Vuorot: {vr}\n".format(v=voitto, k=kenttakoko, m=miinat_lkm, p=pvm, km=aika, vr=vuorot)
    tiedot += rivi
    return tiedot


def kirjoita_tiedostoon(tiedosto, tiedot):
    '''Kirjoittaa annetun sis‰llˆn m‰‰r‰tyn nimiseen tiedostoon ja sulkee tiedoston.'''
    with open(tiedosto, "a") as kohde:
        kohde.write(tiedot)


def kysy_kentta():
    '''Kyselee k‰ytt‰j‰lt‰ kent‰n korkeuden ja leveyden, tarkistaa niiden k‰ytett‰vyyden kent‰n rajoina ja palauttaa ne.'''
    print("Syˆt‰ haluamasi kent‰n leveys ja korkeus. Huomaa, ett‰ peli ei pysty k‰sittelem‰‰n ihan ‰lyttˆmi‰ kentt‰kokoja.")
    while True:
        try:
            leveys = int(input("Anna kent‰n leveys: ").strip())
        except ValueError:
                print("Valitsemasi toiminto ei ole mahdollinen.")
        else:
            try:
                korkeus = int(input("Anna kent‰n korkeus: ").strip())
            except ValueError:
                    print("Valitsemasi toiminto ei ole mahdollinen.")
            else:
                if leveys <= 0 or korkeus <= 0:
                    print("Noin pienelle kent‰lle ei mahdu ainuttakaan pistett‰!")
                elif leveys * korkeus < 2:
                    print("Pelaamiseen vaaditaan enemm‰n kuin yksi ruutu!")
                elif (leveys * korkeus) > 900:
                    print("Ohjelma ei pysty k‰sittelem‰‰n noin suurta kentt‰‰!")
                else:
                    return leveys, korkeus


def luo_kentta(leveys, korkeus):
    '''Luo kent‰n #-merkkej‰ sis‰lt‰v‰n‰ listana annetun leveyden ja korkeuden mukaan'''
    kentta = []
    for i in range(korkeus):
        kentta.append([])
        for x in range(leveys):
            kentta[i].append("#")
    return kentta


def kysy_miinat(kentta):
    '''Kysyy miinojen lukum‰‰r‰n ja tarkistaa ettei niiden lukum‰‰r‰ ylit‰ kent‰n kokoa'''
    korkeus = len(kentta)
    leveys = len(kentta[0])
    while True:
        try:
            miinat_lkm = int(input("Anna miinojen lukum‰‰r‰: "))
        except ValueError:
            print("Lukum‰‰r‰ tarkoittaa positiivista kokonaislukua.")
        else:
            if miinat_lkm <= 0:
                print("Lukum‰‰r‰ tarkoittaa positiivista kokonaislukua.")
            elif miinat_lkm > (korkeus * leveys) -1:
                print("Kent‰lle ei mahdu noin montaa miinaa/ kent‰lle pit‰‰ j‰‰d‰ v‰hint‰‰n yksi tyhj‰ ruutu!")
            else:
                break
    return miinat_lkm


def miinoita_satunnainen(kentta, jaljella):
    '''Miinoittaa satunnaisen koordinaatin kent‰st‰. Loopataan p‰‰ohjelmassa tarvittava m‰‰r‰. Jaljella-argumentti on lista koordinaateista, joka sekin koostetaan p‰‰ohjelmassa'''
    miinakoord = random.choice(jaljella)
    miinalista = list(miinakoord)
    x, y = miinalista[0], miinalista[1]
    kentta[y][x] = "x"
    jaljella.remove(miinakoord)
    return x, y


def numeroi(kentta, jaljella, xkoord, ykoord):
    '''Numeroi miinakentt‰-listaan miinojen ymp‰rill‰ olevat ruudut vieress‰ olevien miinojen mukaan. !!muokkaa siis miinakentta-listaa'''
    korkeus = len(kentta) - 1
    leveys = len(kentta[0]) - 1
    numero = 0

    for y in [-1, 0, 1]:
        for x in [-1, 0, 1]:
            uusiy = ykoord + y
            uusix = xkoord + x
            if not (uusix > leveys or uusiy > korkeus or uusix < 0 or uusiy < 0):
                if kentta[uusiy][uusix] == "x":
                    numero = numero + 1
                if numero == 0:
                    kentta[ykoord][xkoord] = "."
                elif kentta[ykoord][xkoord] != "x":
                    kentta[ykoord][xkoord] = str(numero)
    return kentta


def kysy_koordinaatit(leveys, korkeus, kentta):
    '''Kysyy, tarkistaa ja palauttaa kent‰lt‰ avattavat koordinaatit.'''
    while True:
        try:
            while True:
                jono = input("Anna koordinaatit v‰lilyˆnnill‰ erotettuna tai lopeta tyhj‰ll‰: ")
                if not jono:
                    return None, None
                luvut = jono.split(" ")
                xkoord = int(luvut[0])
                ykoord = int(luvut[1])
                if len(luvut) != 2:
                    print("Anna kaksi koordinaattia v‰lilyˆnnill‰ erotettuna!")
                elif xkoord > leveys - 1 or ykoord > korkeus - 1 or xkoord < 0 or ykoord < 0:
                    print("Antamasi piste (x: {luku1}, y: {luku2}) on kent‰n rajojen ulkopuolella!.".format(luku1=xkoord, luku2=ykoord))
                elif kentta[ykoord][xkoord] != "#":
                    print("Olet jo avannut t‰m‰n koordinaatin!")
                else:
                    break
        except ValueError:
            print("Anna koordinaatit kokonaislukuina!")
        except IndexError:
            print("Anna kaksi koordinaattia v‰lilyˆnnill‰ erotettuna")
        except (KeyboardInterrupt, EOFError):
            sys.exit()
        else:
            return xkoord, ykoord


def tulvataytto(xkoord, ykoord, pelikentta, miinakentta):
    '''Avaa annetun koordinaatin: jos se on numeroruutu, avaa vaan sen; jos se on tyhj‰, tulvat‰ytt‰‰ pelikentt‰‰ rajoihin/numeroruutuihin asti'''
    lista = [(xkoord, ykoord)]
    jono = ["1", "2", "3", "4", "5", "6", "7", "8"]
    while True:
            try:
                xkoord, ykoord = lista[0]
            except IndexError:
                break
            else:
                if miinakentta[ykoord][xkoord] in jono:
                    pelikentta[ykoord][xkoord] = miinakentta[ykoord][xkoord]
                    break
                elif miinakentta[ykoord][xkoord] == ".":
                    pelikentta[ykoord][xkoord] = "."
                    lista.remove((xkoord, ykoord))
                    for xk in [-1, 0, 1]:
                        for yk in [-1, 0, 1]:
                            uusiy = ykoord + yk
                            uusix = xkoord + xk
                            if uusiy >= 0 and uusix >= 0 and uusix < len(miinakentta[0]) and uusiy < len(miinakentta) and pelikentta[uusiy][uusix] == "#"  and miinakentta[uusiy][uusix] == ".":
                                lista.append((uusix, uusiy))
                            elif lista == None:
                                print("Ruutujen aukaisemisessa tapahtui virhe.")
                                break
                    for y in [-1, 0, 1]:
                        for x in [-1, 0, 1]:
                            uusiy = ykoord + y
                            uusix = xkoord + x
                            if x == 0 and y == 0:
                                continue
                            if uusiy >= 0 and uusix >= 0 and uusix < len(miinakentta[0]) and uusiy < len(miinakentta) and pelikentta[uusiy][uusix] == "#" and miinakentta[uusiy][uusix] in jono:
                                pelikentta[uusiy][uusix] = miinakentta[uusiy][uusix]
                            elif lista == None:
                                print("Ruutujen aukaisemisessa tapahtui virhe.")
                                break

                elif not pelikentta[ykoord][xkoord] == "#":
                    lista.remove((xkoord, ykoord))
                    continue
                else:
                    print("Ruutujen ayyy")
                    break


def tulostus(kentta):
    '''Tulostaa syˆtetyn kent‰n sek‰ numeroi x- ja y-akselit leveyden ja korkeuden mukaan'''
    m = 0
    l = 0
    xnumerot = []
    xnumerot1 = []
    for i in range(len(kentta[0])):
        ayy = xnumerot.append(str(m))
        str(xnumerot[i])
        kives = xnumerot1.append(str(m))
        str(xnumerot1[i])
        m = m + 1
        l = l + 1
    if m <= 10:
        print("   " + "  ".join(xnumerot))
    elif 11 <= l < 100:
        print(("   " + "  ".join(xnumerot[0:10])) + ("  " + " ".join(xnumerot1[10:])))
    n = 0
    while True:
        try:
            if n < 10:
                print(str(n) + "  " + "  ".join(kentta[n]))
                #print()
            elif 10 <= n < 100:
                print(str(n) + " " + "  ".join(kentta[n]))
                #print()
            n = n + 1
        except IndexError:
            break


def tulosta_tilastot(tiedosto):
    try:
        with open(tiedosto) as lahde:
            for rivi in lahde.readlines():
                print(rivi)
    except IOError:
        print("Tiedoston avaaminen ei onnistunut. Aloitetaan tyhj‰ll‰ kokoelmalla")


miinantallaaja = ("""
 /$$      /$$ /$$$$$$ /$$$$$$ /$$   /$$  /$$$$$$  /$$   /$$ /$$$$$$$$  /$$$$$$  /$$       /$$        /$$$$$$   /$$$$$$     /$$$$$  /$$$$$$
| $$$    /$$$|_  $$_/|_  $$_/| $$$ | $$ /$$__  $$| $$$ | $$|__  $$__/ /$$__  $$| $$      | $$       /$$__  $$ /$$__  $$   |__  $$ /$$__  $$
| $$$$  /$$$$  | $$    | $$  | $$$$| $$| $$  \ $$| $$$$| $$   | $$   | $$  \ $$| $$      | $$      | $$  \ $$| $$  \ $$      | $$| $$  \ $$
| $$ $$/$$ $$  | $$    | $$  | $$ $$ $$| $$$$$$$$| $$ $$ $$   | $$   | $$$$$$$$| $$      | $$      | $$$$$$$$| $$$$$$$$      | $$| $$$$$$$$
| $$  $$$| $$  | $$    | $$  | $$  $$$$| $$__  $$| $$  $$$$   | $$   | $$__  $$| $$      | $$      | $$__  $$| $$__  $$ /$$  | $$| $$__  $$
| $$\  $ | $$  | $$    | $$  | $$\  $$$| $$  | $$| $$\  $$$   | $$   | $$  | $$| $$      | $$      | $$  | $$| $$  | $$| $$  | $$| $$  | $$
| $$ \/  | $$ /$$$$$$ /$$$$$$| $$ \  $$| $$  | $$| $$ \  $$   | $$   | $$  | $$| $$$$$$$$| $$$$$$$$| $$  | $$| $$  | $$|  $$$$$$/| $$  | $$
|__/     |__/|______/|______/|__/  \__/|__/  |__/|__/  \__/   |__/   |__/  |__/|________/|________/|__/  |__/|__/  |__/ \______/ |__/  |__/
""")




#p‰‰ohjelma
if __name__ == "__main__":
    try:
        tiedosto = (sys.argv[1])
    except IndexError:
        print("Virhe: tilastotiedoston nimi on annettava komentoriviargumenttina!")
    else:
        print(miinantallaaja)
        print()
        while True:
            while True:
                #Alkuvalikko
                valinta = input("Valitse:\n  'p' -- pelaa peli\n  'q' -- lopeta ohjelma\n  't' -- n‰yt‰ tilastot\n\nValintasi: ")
                if valinta.lower() == "p":
                    break
                elif valinta.lower() == "q":
                    sys.exit()
                elif valinta.lower() == "t":
                    tulosta_tilastot(tiedosto)
                else:
                    print("Valintasi on invalidi.")

            #pelin alustus: tilastojen 'aloitus', pelikent‰n kysely ja luonti
            nimi = input("Anna pelaajan nimi: ")
            pvm = time.ctime()
            alku = time.time()
            leveys, korkeus = kysy_kentta()
            pelikentta = luo_kentta(leveys, korkeus)
            miinakentta = luo_kentta(leveys, korkeus)
            miinat_lkm = kysy_miinat(miinakentta)
            kenttakoko = "{}x{}".format(leveys, korkeus)

            jaljella = []
            for x in range(leveys):
                for y in range(korkeus):
                    jaljella.append((x, y))
            #print(jaljella) #tarkistusta varten

            for i in range(miinat_lkm):
                miinoita_satunnainen(miinakentta, jaljella)
            #print(jaljella) #tarkistusta varten

            n = 0
            for i in range(len(jaljella)):
                xkoord, ykoord = jaljella[n]
                numeroi(miinakentta, jaljella, xkoord, ykoord)
                n = n + 1

            #itse pelisilmukka alkaa t‰st‰
            vuorot = 0
            while True:
                print("\n\n")
                tulostus(pelikentta)
                print("\n")
                #tulostus(miinakentta) #tarkastusta varten
                xkoord, ykoord = kysy_koordinaatit(leveys, korkeus, pelikentta)
                if xkoord == None or ykoord == None:
                    break

                elif miinakentta[ykoord][xkoord] == "x":
                    print("Tallasit miinaan, h‰visit pelin. :(")
                    tulostus(miinakentta)
                    loppu = time.time()
                    aika = int((abs(loppu - alku) / 60))
                    voitto = "h"
                    vuorot = vuorot + 1
                    tiedot = kysele_tiedot()
                    kirjoita_tiedostoon(tiedosto, tiedot)
                    break
                else:
                    tulvataytto(xkoord, ykoord, pelikentta, miinakentta)
                    avaamattomat = 0
                    for i in range(len(pelikentta)):
                        avaamattomat = avaamattomat + pelikentta[i].count("#")
                    if miinat_lkm == avaamattomat:
                        print("Voitit pelin!")
                        tulostus(miinakentta)
                        loppu = time.time()
                        aika = int((abs(loppu - alku) / 60))
                        voitto = "v"
                        vuorot = vuorot + 1
                        tiedot = kysele_tiedot()
                        kirjoita_tiedostoon(tiedosto, tiedot)
                        break
                    else:
                        tulvataytto(xkoord, ykoord, pelikentta, miinakentta)

#Tekij‰t: Markus Savusalo, Ville Karjalainen, Juho Sipola, Abazi Bekim, Ville Karsikko
