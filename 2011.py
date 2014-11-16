# coding=utf-8
from collections import OrderedDict

import execute

"""
L: bin(n)#0^n

Innymi słowy po lewej od hasza to pewna liczba w zapisie binarnym, na prawo ta sama liczba w zapisie unarnym.
Zakładam brak zer wiodących dla zapisu binarnego.

Szkic działania maszyny:

powtórz
    #(s)prawdz
    jeśli ciąg to 0#
        akceptuj
    #(p)rzejdz do znaku po lewej od #
    jeśli liczba po lewej jest parzysta (tj. po lewej od # jest 0)
        #po(d)ziel obie strony przez 2
        przesuń # i znaki na prawo od # o jedną pozycję, tracąc najmłodszy bit liczby binarnej
        zamień połowę 0 po prawej od hasha na ^
        powtarzaj aż do określonego stopu
            przejdź w prawo
            przesuwaj ciąg w lewo o jeden znak
                jeśli dojdziesz do #
                    nadpisz go i wróć w prawo
                jeśli dojdziesz do blanka
                    nadpisz go, jest to ten określony stop
    jeśli liczba po lewej jest nieparzysta (tj. po lewej od # jest 1)
        #(o)dejmij od obu stron po jeden
        zamień 1 na lewo od # na 0
        usuń jedno zero po prawej strony ciągu
"""

convert = OrderedDict()
# [(znak, stan)] = (nowy_znak, nowy_stan, kierunek_przejścia)
convert[("0", "start")] = ("0", "s.a", ">")
convert[("#", "start")] = ("0", "p.a", "")
convert[("1", "start")] = ("1", "p.a", "")
convert[("#", "s.a")] = ("#", "s.b", ">")
convert[("0", "s.a")] = ("0", "p.a", "<")
convert[("1", "s.a")] = ("1", "p.a", "<")
convert[(" ", "s.b")] = (" ", "yes", ">")
convert[("#", "s.b")] = ("#", "s.c", "<")
convert[("0", "s.b")] = ("0", "s.c", "<")
convert[("1", "s.b")] = ("1", "s.c", "<")
convert[("#", "s.c")] = ("#", "p.a", "<")
convert[("0", "s.c")] = ("0", "p.a", "<")
convert[("1", "s.c")] = ("1", "p.a", "<")

convert[("#", "p.a")] = ("#", "p.b", "<")
convert[("0", "p.a")] = ("0", "p.a", ">")
convert[("1", "p.a")] = ("1", "p.a", ">")

convert[("0", "p.b")] = ("0", "d.a", "")
convert[("1", "p.b")] = ("1", "o.a", "")

convert[("1", "d.a")] = ("1", "d.a", ">")
convert[("#", "d.a")] = ("#", "d.a", ">")
convert[("0", "d.a")] = ("0", "d.a", ">")
convert[(" ", "d.a")] = (" ", "d.b", "<")  # przejdz do ostatniego znaku

convert[("0", "d.b")] = (" ", "d.c", "<")  # wytnij ostatni znak
convert[("0", "d.c")] = ("0", "d.c", "<")
convert[("#", "d.c")] = ("0", "d.d", "<")  # wklej go na hasz
convert[("0", "d.d")] = ("#", "d.e", ">")  # najmłodzy znak z liczby binarnej zastąp przez hasz
convert[("0", "d.e")] = ("0", "d.e", ">")
convert[(" ", "d.e")] = (" ", "d.f", "<")  # przejdz do ostatniego znaku

convert[("0", "d.f")] = ("0", "d.g", "<")
convert[("#", "d.f")] = ("#", "d.h", ">")
convert[("0", "d.g")] = ("^", "d.f", "<")  # zamień połowę zer z prawej na daszki

convert[("0", "d.h")] = ("0", "d.h", ">")
convert[("^", "d.h")] = ("^", "d.h", ">")
convert[(" ", "d.h")] = (" ", "d.i", "<")  # przejdz do ostatniego znaku

convert[("0", "d.i")] = ("0", "d.i", "<")
convert[("^", "d.i")] = ("0", "d.j", ">")
convert[("#", "d.i")] = ("#", "d.l", "<")  # stop, wszystkie daszki skasowane!
convert[("0", "d.j")] = ("0", "d.j", ">")
convert[(" ", "d.j")] = (" ", "d.k", "<")
convert[("0", "d.k")] = (" ", "d.i", "<")  # usuń jeden daszek i przejdz do ostatniego znaku

convert[("0", "d.l")] = ("0", "d.l", "<")
convert[("1", "d.l")] = ("1", "d.l", "<")
convert[(" ", "d.l")] = (" ", "start", ">")  # wróć na start

convert[("1", "o.a")] = ("0", "o.b", ">")
convert[("#", "o.b")] = ("#", "o.b", ">")
convert[("0", "o.b")] = ("0", "o.b", ">")
convert[(" ", "o.b")] = (" ", "o.c", "<")
convert[("0", "o.c")] = (" ", "o.d", "<")
convert[("1", "o.c")] = (" ", "o.d", "<")
convert[("#", "o.d")] = ("#", "o.d", "<")
convert[("0", "o.d")] = ("0", "o.d", "<")
convert[("1", "o.d")] = ("1", "o.d", "<")
convert[(" ", "o.d")] = (" ", "start", ">")

# execute.execute(convert, "1#0")
#execute.execute(convert, "1##0")
#execute.execute(convert, "11#000")
#execute.execute(convert, "1#1")
#execute.execute(convert, "10#00")

def checker(tape):
    if not "#" in tape:
        return False  # ensure termination of following loop
    if tape[0] == "0" and tape[1] != "#":
        return False  # leading zero
    if tape[0] == "#":
        return False  # empty string is not a binary number
    position = 0
    number = 0
    while True:
        if tape[position] == "0":
            number *= 2
        elif tape[position] == "1":
            number *= 2
            number += 1
        elif tape[position] == "#":
            break
        else:
            return False
        position += 1
    # tape[position] == "#"
    position += 1
    while position < len(tape):
        if tape[position] == "0":
            number -= 1
        elif tape[position] == " ":
            break
        else:
            return False
        position += 1
    return number == 0

# sprawdz czy MT da tą samą odpowiedź co checker na taśmach o długości do 9 znaków
execute.verify(convert, checker, 9)