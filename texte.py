# nos fichier, cf : celui qui l'ecrit

from table import table

# librarie standard, cf : internet

from sys import stdout, stdin
from _io import TextIOWrapper

def run_texte(ta: table) -> int:
    """
    fonction principale en mode textuel
    """
    c = None
    if ta is None:
        while True:
            try:
                c = int(input("taille?"))
                ta = table('{"size": %d}' % c)
            except:
                continue
            else:
                break
    else:
        c = len(ta)
    if __debug__:
            assert(ta is not None)
    while True:
        cmd = " ".join(filter(None, input("? : ").split()))
        if cmd == "set value":
            try:
                x = int(input("x ? : "))
                y = int(input("y ? : "))
                v = int(input("v (0 pour retirer) ? : "))
                ta.set_value_at(x, y, v)
            except ValueError:
                continue
        elif cmd == "set vsign":
            try:
                x = int(input("x ? : "))
                y = int(input("y ? : "))
                v = int(input("True pour >, False pour <  : "))
                ta.set_v_sign_at(x, y, v)
            pass
        elif cmd == "set hsign":
            try:
                x = int(input("x ? : "))
                y = int(input("y ? : "))
                v = int(input("True pour >, False pour <  : "))
                ta.set_h_sign_at(x, y, v)
            pass
        else:
            print("commande inconnue")
        """


        """                
#    ta.set_h_sign_at(0, 0, True) => signe horizontal : case 0,0> 1,0 => limite x=c-2
#    ta.set_h_sign_at(1, 0, True) => 1,0 > 2.0
#    ta.set_h_sign_at(0, 1, True)
#    ta.set_h_sign_at(2, 3, False)
#    ta.set_v_sign_at(3, 2, True) => y_lim=c-2
#    print(ta)
    print(ta.gen_dimacs())
    return 0
