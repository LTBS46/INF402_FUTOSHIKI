# nos fichier, cf : celui qui l'ecrit

from table import table

# librarie standard, cf : internet

from sys import stdout, stdin
from _io import TextIOWrapper

def demander_un_nombre(msg: str = "") -> int | None:
    while True:
        try:
            rv = int(input(msg + " : "))
            return rv
        except ValueError:  # si c'est autre chose qu'un entier,
            print("Ce paramètre n'accepte que les valeurs entières. Veuillez réessayer.")
            continue        # on redemande la valeur
        except KeyBoardInterrupt:
            return None

def run_texte(ta: table) -> int:
    """
    fonction principale en mode textuel
    """
    c = None
    if ta is None:
        while True:
            try:
                c = demander_un_nombre("taille")
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
        cmd = " ".join(filter(None, input("cmd -> ").split())) # enlève tous les espaces en trop
        if cmd == "set value":
            try:
                print("Entrez les coordonnées de la case à modifier")
                x = demander_un_nombre("x")
                y = demander_un_nombre("y")
                v = demander_un_nombre("v (0 pour retirer)")
                ta.set_value_at(x, y, v)
            except ValueError:
                continue
        elif cmd == "set vsign":
            try:
                print("Quelle est la case se situant EN HAUT du signe à ajouter ?")
                x = demander_un_nombre("x")
                y = demander_un_nombre("y")
                v = int(input("orientation (True pour ⋁, False pour ⋀) : ")) # affichage des caractères spéciaux à vérifier
                ta.set_v_sign_at(x, y, v)
            except ValueError:
                continue
        elif cmd == "set hsign":
            try:
                print("Quelle est la case se situant À GAUCHE du signe à ajouter ?")
                x = demander_un_nombre("x")
                y = demander_un_nombre("y")
                v = int(input("orientation (True pour >, False pour <) : "))
                ta.set_h_sign_at(x, y, v)
            except ValueError:
                continue
        elif cmd == "display table": # afficher la table
            # il suffirait de convertir la table en chaîne de caractères
            try:
                print(string(ta))
            except:
                print("L'opération n'a pas fonctionnée")
        elif cmd == "quit": # mettre fin aux modifications
            break           # sortir de la boucle while True
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
