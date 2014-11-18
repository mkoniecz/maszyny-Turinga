# coding=utf-8
from collections import OrderedDict
import re

import execute


"""
X = (0|1|#)*
Y = (0|1|#)*
X jest podciągiem Y
L: X#Y

Tem sam język można opisać prościej:

X = (0|1)*
Y = (0|1|#)*
X jest podciągiem Y
L: X#Y
"""

"""
Każde 0 i 1 po pierwszym haszu będzie sprawdzane czy nie jest początkiem szukanego ciągu.
"""

"""
przetworzone 0 oznaczam jako @
przetworzone 1 oznaczam jako !

przejdź do pierwszego nieprzetworzonego znaku (start)
    jeśli znak ten to hasz - zaakceptuj
    zapamiętaj ten znak i oznacz go jako przetworzony
    dojdź do pierwszego (h)asza
    dojdz do ostatniego (h)asza w ciągu haszów
    dojdź do pierwszego znaku będącego 0 (l)ub 1
    jeśli znak ten to blank - przejdź w stan odrzucający
    jeśli znak to nie ten co zapamiętany
        (w)róć, usuwając oznaczenia jako przetworzone
        ostatni znak przed haszem zamień w hasza
        wróć na początek usuwając oznaczenia jako przetworzone
    jeśli znak pasuje do zapamiętanego
        oznacz go jako przetworzony
        (p)rzejdź na początek ciągu
"""
subsequence = OrderedDict()

# [(znak, stan)] = (nowy_znak, nowy_stan, kierunek_przejścia)
subsequence[("@", "start")] = ("@", "start", ">")
subsequence[("!", "start")] = ("!", "start", ">")
subsequence[("#", "start")] = ("#", "yes", "")
subsequence[("0", "start")] = ("@", "h0.a", ">")
subsequence[("1", "start")] = ("!", "h1.a", ">")
subsequence[("0", "h1.a")] = ("0", "h1.a", ">")
subsequence[("1", "h1.a")] = ("1", "h1.a", ">")
subsequence[("#", "h1.a")] = ("#", "h1.b", ">")
subsequence[("#", "h1.b")] = ("#", "h1.b", ">")
subsequence[("0", "h1.b")] = ("0", "l1", "")
subsequence[("1", "h1.b")] = ("1", "l1", "")
subsequence[("#", "h1.b")] = ("#", "h1.b", ">")
subsequence[("@", "h1.b")] = ("@", "l1", "")
subsequence[("!", "h1.b")] = ("!", "l1", "")
subsequence[("@", "l1")] = ("@", "l1", ">")
subsequence[("!", "l1")] = ("!", "l1", ">")
subsequence[("0", "l1")] = ("0", "w.a", "<")
subsequence[("1", "l1")] = ("!", "p", "<")
subsequence[("#", "l1")] = ("#", "w.a", "<")
subsequence[("0", "h0.a")] = ("0", "h0.a", ">")
subsequence[("1", "h0.a")] = ("1", "h0.a", ">")
subsequence[("#", "h0.a")] = ("#", "h0.b", ">")
subsequence[("#", "h0.b")] = ("#", "h0.b", ">")
subsequence[("0", "h0.b")] = ("0", "l0", "")
subsequence[("1", "h0.b")] = ("1", "l0", "")
subsequence[("#", "h0.b")] = ("#", "h0.b", ">")
subsequence[("@", "h0.b")] = ("@", "l0", "")
subsequence[("!", "h0.b")] = ("!", "l0", "")
subsequence[("@", "l0")] = ("@", "l0", ">")
subsequence[("!", "l0")] = ("!", "l0", ">")
subsequence[("0", "l0")] = ("@", "p", "<")
subsequence[("1", "l0")] = ("1", "w.a", "<")
subsequence[("#", "l0")] = ("#", "w.a", "<")
subsequence[("@", "p")] = ("@", "p", "<")
subsequence[("!", "p")] = ("!", "p", "<")
subsequence[("#", "p")] = ("#", "p", "<")
subsequence[("0", "p")] = ("0", "p", "<")
subsequence[("1", "p")] = ("1", "p", "<")
subsequence[(" ", "p")] = (" ", "start", ">")
subsequence[("@", "w.a")] = ("0", "w.a", "<")
subsequence[("!", "w.a")] = ("1", "w.a", "<")
subsequence[("#", "w.a")] = ("#", "w.b", ">")
subsequence[("0", "w.b")] = ("#", "w.c", "<")
subsequence[("1", "w.b")] = ("#", "w.c", "<")
subsequence[("#", "w.c")] = ("#", "w.c", "<")
subsequence[("0", "w.c")] = ("0", "w.c", "<")
subsequence[("1", "w.c")] = ("1", "w.c", "<")
subsequence[("@", "w.c")] = ("0", "w.c", "<")
subsequence[("!", "w.c")] = ("1", "w.c", "<")
subsequence[(" ", "w.c")] = (" ", "start", ">")

# execute.execute(subsequence, "1#01")
#execute.execute(subsequence, "##")
#execute.execute(subsequence, "10#01")

def checker(tape):
    m = re.search('^ *(?P<x>[01]*)#[01#]*(?P=x)[01#]* *$', tape)
    if m is None:
        return False
    else:
        return True


# sprawdz czy MT da tą samą odpowiedź co checker na taśmach o długości do 10 znaków
execute.verify(subsequence, checker, 10, "01#")