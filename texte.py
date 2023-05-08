# nos fichier, cf : celui qui l'ecrit

from table import table

# librarie standard, cf : internet

from sys import stdout, stdin
from _io import TextIOWrapper

def demander_un_nombre(msg: str = "", val_max: int = 0) -> int | None:
    while True:
        try:
            rv = int(input(msg + " : "))
            if rv < 0 or rv > val_max:
                print("L'entier entré ici doit être compris entre 0 et " + str(val_max)
                      + ". Veuillez réessayer.")
                continue          
            else:
                return rv
        except ValueError:  # si c'est autre chose qu'un entier,
            print("Ce paramètre n'accepte que les valeurs entières. Veuillez réessayer.")
            continue        # on redemande la valeur
        except KeyboardInterrupt:
            print("\tValeur non remplie. Redémarrage.")
            return None

def run_texte(ta: table) -> int:
    """
    fonction principale en mode textuel
    """
    c = None
    if ta is None:
        while True:
            try:
                c = demander_un_nombre("Taille de la grille", 2<<16)
                ta = table(c)
            except Exception as e:
                print(e)
            if ta is not None:
                break
    else:
        c = len(ta)
    if __debug__:
            assert(ta is not None)
    while True:
        cmd = " ".join(filter(None, input("cmd -> ").split())) # enlève tous les espaces en trop
        if cmd == "set value": # rentrer une valeur dans une case
            try:
                print("Entrez les coordonnées de la case à modifier")
                x = demander_un_nombre("x", c-1)
                if x is None:   # si on a détecté un KeyboardInterrupt,
                    continue    # on quitte la commande
                y = demander_un_nombre("y", c-1)
                if y is None:    
                    continue
                v = demander_un_nombre("valeur (0 pour retirer)", c)
                if v is None:
                    continue                
                ta.set_value_at(x, y, v)
            except ValueError:
                continue
        elif cmd == "set vsign": # mettre un signe |vertical|
            try:
                print("Quelle est la case se situant AU DESSUS du signe à ajouter ?")
                x = demander_un_nombre("x", c-1)
                if x is None:
                    continue                
                y = demander_un_nombre("y", c-2)
                if y is None:
                    continue                
                v = demander_un_nombre("orientation (0 pour ⋀, 1 pour ⋁)", 1)
                ta.set_v_sign_at(x, y, v)
            except ValueError:
                continue
        elif cmd == "set hsign": # mettre un signe -horizontal-
            try:
                print("Quelle est la case se situant À GAUCHE du signe à ajouter ?")
                x = demander_un_nombre("x", c-2)
                if x is None:
                    continue                
                y = demander_un_nombre("y", c-1)
                if y is None:
                    continue                
                v = demander_un_nombre("orientation (0 pour <, 1 pour >) : ", 1)
                ta.set_h_sign_at(x, y, v)
            except ValueError:
                continue
        elif cmd == "display table": # afficher la table
            try:
                print("\n")
                print(ta)
            except Exception as e:
                print(e)
                print("L'opération n'a pas fonctionné")
                raise e
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
    print("Modifications terminées.")
    print("Aperçu du fichier Dimacs :")
    print("\n")
    print(ta.gen_dimacs())
    return 0
