# nos fichier, cf : celui qui l'ecrit

from graphique import run_graphique     # contient le mode graphique
from texte import run_texte             # contient le mode texte
from table import table
from sat import solve

# librarie standard, cf : internet

import sys                              # les argument du programe
import argparse                         # lire les arguments du programe


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Futoshiki solver")

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-a', '--auto', action='store_const', const=None, dest='flag_graph', default=None)
    mode.add_argument('-t', '--text', action='store_false', dest='flag_graph')
    mode.add_argument('-g', '--graphic', action='store_true', dest='flag_graph')
    
    
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)

    args = parser.parse_args()

    if args.flag_graph is None:
        t = table(args.infile.read())
        #print(t)
        args.outfile.write(str(table(t.n, solve(t.gen_dimacs()))))
    else:
        if args.flag_graph:
            run_graphique(infile=args.infile)
        else:
            if sys.stdin == args.infile:
                run_texte(None)
            else:
                run_texte(table(args.infile.read()))
                args.infile.close()
