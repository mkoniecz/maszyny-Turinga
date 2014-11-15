# coding=utf-8
from collections import OrderedDict

import execute

"""
L: bin(n)#0^n

Innymi słowy po lewej od hasza to pewna liczba w zapisie binarnym, na prawo ta sama liczba w zapisie unarnym.

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

double = OrderedDict()
double[("0", "start")] = ("0", "s.a", ">")
double[("#", "start")] = ("0", "p.a", "")
double[("1", "start")] = ("1", "p.a", "")
double[("#", "s.a")] = ("#", "s.b", ">")
double[("0", "s.a")] = ("0", "p.a", "<")
double[("1", "s.a")] = ("1", "p.a", "<")
double[(" ", "s.b")] = (" ", "yes", ">")
double[("#", "s.b")] = ("#", "s.c", "<")
double[("0", "s.b")] = ("0", "s.c", "<")
double[("1", "s.b")] = ("1", "s.c", "<")
double[("#", "s.c")] = ("#", "p.a", "<")
double[("0", "s.c")] = ("0", "p.a", "<")
double[("1", "s.c")] = ("1", "p.a", "<")

double[("#", "p.a")] = ("#", "p.b", "<")
double[("0", "p.a")] = ("0", "p.a", ">")
double[("1", "p.a")] = ("1", "p.a", ">")

double[("0", "p.b")] = ("0", "d.a", "")
double[("1", "p.b")] = ("1", "o.a", "")

double[("1", "d.a")] = ("1", "d.a", ">")
double[("#", "d.a")] = ("#", "d.a", ">")
double[("0", "d.a")] = ("0", "d.a", ">")
double[(" ", "d.a")] = (" ", "d.b", "<")  # przejdz do ostatniego znaku

double[("0", "d.b")] = (" ", "d.c", "<")  # wytnij ostatni znak
double[("0", "d.c")] = ("0", "d.c", "<")
double[("#", "d.c")] = ("0", "d.d", "<")  # wklej go na hasz
double[("0", "d.d")] = ("#", "d.e", ">")  # najmłodzy znak z liczby binarnej zastąp przez hasz
double[("0", "d.e")] = ("0", "d.e", ">")
double[(" ", "d.e")] = (" ", "d.f", "<")  # przejdz do ostatniego znaku

double[("0", "d.f")] = ("0", "d.g", "<")
double[("#", "d.f")] = ("#", "d.g", ">")
double[("0", "d.g")] = ("^", "d.h", "<")  # zamień połowę zer z prawej na daszki

double[("0", "d.h")] = ("0", "d.h", ">")
double[("^", "d.h")] = ("^", "d.h", ">")
double[(" ", "d.h")] = (" ", "d.i", "<")  # przejdz do ostatniego znaku

double[("0", "d.i")] = ("0", "d.i", "<")
double[("^", "d.i")] = ("0", "d.j", ">")
double[("#", "d.i")] = ("#", "d.l", ">")  # stop, wszystkie daszki skasowane!
double[("0", "d.j")] = ("0", "d.j", ">")
double[(" ", "d.j")] = (" ", "d.k", "<")
double[("0", "d.k")] = (" ", "d.i", "<")  # usuń jeden daszek i przejdz do ostatniego znaku

double[("0", "d.l")] = ("0", "d.l", "<")
double[("1", "d.l")] = ("1", "d.l", "<")
double[(" ", "d.l")] = (" ", "start", ">")  # wróć na start

double[("1", "o.a")] = ("0", "o.b", ">")
double[("#", "o.b")] = ("#", "o.b", ">")
double[("0", "o.b")] = ("0", "o.b", ">")
double[("1", "o.b")] = ("1", "o.b", ">")
double[(" ", "o.b")] = (" ", "o.c", "<")
double[("0", "o.c")] = (" ", "o.d", "<")
double[("1", "o.c")] = (" ", "o.d", "<")
double[("#", "o.d")] = ("#", "o.d", "<")
double[("0", "o.d")] = ("0", "o.d", "<")
double[("1", "o.d")] = ("1", "o.d", "<")
double[(" ", "o.d")] = (" ", "start", ">")

execute.execute(double, "1#0")
execute.execute(double, "1##0")
execute.execute(double, "11#000")
