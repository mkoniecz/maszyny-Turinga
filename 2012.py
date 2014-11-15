# coding=utf-8
from collections import OrderedDict

import execute


"""
X = (0|1)*
L = X#X

Szukana jest maszyna akceptująca L.

Najprostszy słowem języka to "#". Można go rozbudować dodając 0: 0X0.
Ogólniej, mając już jakiś słowo w postaci ---#--- można je rozbudować tworząc 0---#0---.
Analogicznie można postępować dla 1 zamiast 0.

Maszyna akceptująca będzie działać w odwrotną stronę.

Szkic działania maszyny:

powtarzaj
    znajdujemy się w pierwszym elemencie zapisanej części taśmy
    (s)prawdź czy na taśmie znajduje się słowo "#"
        jeśli tak - akceptujemy
        jeśli nie - to wracamy na początek
    (u)suń znak z początku ciągu, i dojdź do znaku "#"
        jeśli za "#" nie był taki sam znak - to odrzuć ciąg
        jeśli był taki sam - idź na koniec
    (p)rzesuń ciąg od znaku "#" do końca o jedną pozycję w lewo, tracąc pierwszy znak po czym przejdź na początek
"""

double = OrderedDict()

double[("#", "start")] = ("#", "s.a", ">")
double[("0", "start")] = ("0", "u.a", "")
double[("1", "start")] = ("1", "u.a", "")
double[(" ", "s.a")] = ("#", "yes", ">")
double[("0", "s.a")] = ("0", "u.a", "<")
double[("1", "s.a")] = ("1", "u.a", "<")

double[("1", "u.a")] = (" ", "u1.b", ">")
double[("0", "u.a")] = (" ", "u0.b", ">")
double[("1", "u1.b")] = ("1", "u1.b", ">")
double[("0", "u1.b")] = ("0", "u1.b", ">")
double[("#", "u1.b")] = ("#", "u1.c", ">")
double[("1", "u1.c")] = ("1", "u.d", ">")
double[("1", "u0.b")] = ("1", "u0.b", ">")
double[("0", "u0.b")] = ("0", "u0.b", ">")
double[("#", "u0.b")] = ("#", "u0.c", ">")
double[("0", "u0.c")] = ("0", "u.d", ">")
double[("1", "u.d")] = ("1", "u.d", ">")
double[("0", "u.d")] = ("0", "u.d", ">")
double[(" ", "u.d")] = (" ", "p.a", "<")

double[("1", "p.a")] = (" ", "p1.b", "<")
double[("0", "p.a")] = (" ", "p0.b", "<")
double[("#", "p.a")] = ("#", "p.", "<")
double[("1", "p1.b")] = ("1", "p1.b", "<")
double[("0", "p1.b")] = ("1", "p0.b", "<")
double[("#", "p1.b")] = ("#", "p.c", "<")
double[("1", "p0.b")] = ("0", "p1.b", "<")
double[("0", "p0.b")] = ("0", "p0.b", "<")
double[("#", "p0.b")] = ("#", "p.c", "<")

double[("1", "p.c")] = ("1", "p.c", "<")
double[("0", "p.c")] = ("0", "p.c", "<")
double[(" ", "p.c")] = (" ", "start", ">")

execute.execute(double, "01#01")
execute.execute(double, "##")
execute.execute(double, "01#11")
