# nos fichier, cf : celui qui l'ecrit

None

# librarie standard, cf : internet

from sys import version_info

assert version_info.major == 3

if version_info.minor < 11:
    from typing import Any as Self
else:
    from typing import Self # nouveau en 3.11

from json import loads
from json.decoder import JSONDecodeError
from math import log10, floor


class table(object):
    """
    constructeur de la table
    prend comme argument
    - soit un entier: et construit une table vide
    - soit une chaine de caractères : et le decompose en objet json
    - soit un entier: et une chaine de caractère
    """
    def __init__(self: Self, i: int | str = 5, ret: str | None = None):
        """"""
        _t = type(i)
        if _t == int:
            if i > 0:
                self.n = i
                self.values : list[list[int]] = [[0 for m in range(i)] for l in range(i)]
                self.h_sign = [[None for m in range(i)] for l in range(i - 1)]
                self.v_sign = [[None for m in range(i - 1)] for l in range(i)]
                self._s : int = floor(log10(self.n)) + 1
                if ret is not None:
                    l = ret.split()
                    if l[0] == "SAT":
                        nl = l[1:-1]
                        for v in nl:
                            vi = int(v) - 1
                            if vi >= 0:
                                val = vi % self.n
                                vi //= self.n
                                x_ = vi % self.n
                                y_ = vi // self.n
                                self.values[x_][y_] = val + 1 
                    elif l[0] == "UNSAT":
                        print("failure to solve")
                    else:
                        raise ValueError()
            else:
                raise ValueError()
        elif _t == str:
            _v = loads(i)
            self.__init__(_v["size"])
            e = _v["hsign"]
            for k, v in e.items():
                x, y = (int(tmp) for tmp in k.split(":"))
                self.h_sign[x][y] = v
            e = _v["value"]
            for k,v in e.items():
                x, y = (int(tmp) for tmp in k.split(":"))
                self.values[x][y] = v
            e = _v["vsign"]
            for k, v in e.items():
                x, y = (int(tmp) for tmp in k.split(":"))
                self.v_sign[x][y] = v
        else: # inatteignable
            raise TypeError()
        return None

    def _pad_f(self: Self, to_pad: str) -> str:
        """
    
        """
        return " " * (self._s - len(to_pad)) + to_pad

    def __repr__(self: Self) -> str:
        """
    
        """

        n = self.n
        side = n * 2 + 1
        sideh = self._s * "-"
        spaces = self._s * " "
        s = sideh[:-1]
        vv = "v" + s
        vup = "^" + s
        line_sep = (["|",sideh]*int(n)) + ["|\n"]
        line_content = (["|",spaces]*int(n)) + ["|\n"]

        rv = (line_sep + line_content) * n + line_sep

        for i in range(n):
            for j in range(n):
                v = self.values[i][j]
                if v:
                    try:
                        rv[1 + side + i * 2 + j * side * 2] = self._pad_f(str(v))
                    except Exception as e:
                        print("c", e)
                        raise e
                if i < (n - 1):
                    v = self.h_sign[i][j]
                    if v is not None:
                        try:
                            rv[2*i + 2*side*j+2+side] = ">" if v else "<"
                        except Exception as e:
                            print("h", e)
                            raise e

                if j < (n - 1):
                    v = self.v_sign[i][j]
                    if v is not None:
                        try:
                            rv[2*i + 2*side*j+1+side*2] = vv if v else vup
                        except Exception as e:
                            print("v", e)
                            raise e

        return "".join(rv)


    def __len__(self: Self) -> int:
        """"""
        return self.n

    def __str__(self: Self) -> str:
        """"""
        return self.__repr__()

    def __int__(self: Self) -> int:
        """"""
        return self.__len__()

    def __bool__(self: Self) -> bool:
        """
    
        """
        return any(map(any, self.values))

    def gen_id(self: Self, x: int, y: int, v: int) -> int:
        """
        0 <= x < n, 0 <= y < n, 0 < v <= n    
        """
        return (x * self.n + y) * self.n + v

    def set_value_at(self: Self, x: int, y: int, v: int | None = None) -> None:
        """
    
        """
        n = self.n
        if v is None:
            v = 0
        elif not (0 <= v and v <= self.n):
            raise ValueError()
        self.values[x][y] = v        

    def set_v_sign_at(self: Self, x: int, y: int, v: bool | None) -> None:
        """
    
        """
        n = self.n
        if x < 0 or y < 0 or y >= n or x > (n-2):
            raise ValueError()
        self.v_sign[x][y] = v

    def set_h_sign_at(self: Self, x: int, y: int, v: bool | None) -> None:
        """
    
        """
        n = self.n
        if x < 0 or y < 0 or y >= n or x > (n-2):
            raise ValueError()
        self.h_sign[x][y] = v

    def gen_c_clauses(self: Self) -> list[str]:
        """
    
        """
        return sum([([
                ("" if v + 1 == self.values[x][y] else "-") + str(self.gen_id(x, y, v + 1)) + " 0"
                for v in range(self.n)
        ] if self.values[x][y] != 0 else [
            " ".join(str(self.gen_id(x, y, v + 1)) for v in range(self.n)) + " 0", *[
                f"-{self.gen_id(x, y, v1 + 1)} -{self.gen_id(x, y, v2 + 1)} 0"
                for v1 in range(self.n) for v2 in range(v1 + 1, self.n)
            ]
        ]) for x in range(self.n) for y in range(self.n)], [])

    def gen_v_clauses(self: Self, x: int | None = None) -> list[str]:
        """
    
        """
        return sum([sum([
            ([" ".join([("" if v + 1 == self.values[x][y] else "-") + f"{self.gen_id(x, y, v + 1)}" for y in range(self.n)]) + " 0"]) if
            (v + 1) in [self.values[x][y] for y in range(self.n)]
            else ([" ".join(str(self.gen_id(x, y, v + 1)) for y in range(self.n)) + " 0"] + sum([
                [f"-{self.gen_id(x,y,v+1)} -{self.gen_id(x,y2, v+1)} 0" for y2 in range(y + 1, self.n)] for y in range(self.n - 1)
            ], []))
        for v in range(self.n)], []) for x in range(self.n)], [])

    def gen_h_clauses(self: Self) -> list[str]:
        """
    
        """
        return sum([sum([
            ([" ".join([("" if v + 1 == self.values[x][y] else "-") + f"{self.gen_id(x, y, v + 1)}" for x in range(self.n)]) + " 0"]) if
            (v + 1) in [self.values[x][y] for x in range(self.n)]
            else ([" ".join(str(self.gen_id(x, y, v + 1)) for x in range(self.n)) + " 0"] + sum([
                [f"-{self.gen_id(x, y, v + 1)} -{self.gen_id(x2, y, v + 1)} 0" for x2 in range(x + 1, self.n)] for x in range(self.n - 1)
            ], []))
         for v in range(self.n)],[]) for y in range(self.n)], [])

    def gen_h_sign_clauses(self: Self) -> list[str]:
        """
    
        """
        rv = []
        for x in range(self.n - 1):
            for y in range(self.n):
                if self.h_sign[x][y] is None:
                    continue
                else:
                    if self.values[x][y] != 0:
                        if self.values[x+1][y] != 0: # nested condition either trivialy valid or trivialy invalid
                            if self.h_sign[x][y]:
                                for v1 in range(self.n):
                                    for v2 in range(v1, self.n):
                                        rv.append(f"-{self.gen_id(x, y, v1 + 1)} -{self.gen_id(x, y + 1, v2 + 1)} 0")
                            else:
                                for v1 in range(self.n):
                                    for v2 in range(v1, self.n):
                                        rv.append(f"-{self.gen_id(x, y, v2 + 1)} -{self.gen_id(x, y + 1, v1 + 1)} 0")
                        elif self.h_sign[x][y]: # superieur
                            rv.append(" ".join([str(self.gen_id(x + 1, y, v+1)) for v in range(self.values[x][y])]) + " 0")
                        else:
                            rv.append(" ".join([str(self.gen_id(x + 1, y, v+1)) for v in range(self.values[x][y] , self.n)]) + " 0")
                    elif self.values[x+1][y] != 0:
                        if self.h_sign[x][y]:
                            rv.append(" ".join([str(self.gen_id(x, y, v+1)) for v in range(self.values[x+1][y] , self.n)]) + " 0")
                        else:
                            rv.append(" ".join([str(self.gen_id(x,y,v+1)) for v in range(self.values[x+1][y])]) + " ")
                    elif self.h_sign[x][y]:
                        for v1 in range(self.n):
                            for v2 in range(v1, self.n):
                                rv.append(f"-{self.gen_id(x, y, v1 + 1)} -{self.gen_id(x, y + 1, v2 + 1)} 0")
                    else:
                        for v1 in range(self.n):
                            for v2 in range(v1, self.n):
                                rv.append(f"-{self.gen_id(x, y, v2 + 1)} -{self.gen_id(x, y + 1, v1 + 1)} 0")
        return rv
        
    def gen_v_sign_clauses(self: Self) -> list[str]:
        """"""
        rv = []
        for x in range(self.n):
            for y in range(self.n - 1):
                if self.v_sign[x][y] is None:
                     continue
                else:
                    if self.values[x][y] != 0:
                        if self.values[x][y+1] != 0:
                            if self.h_sign[x][y]:
                                for v1 in range(self.n):
                                    for v2 in range(v1, self.n):
                                        rv.append(f"-{self.gen_id(x, y, v1 + 1)} -{self.gen_id(x+ 1, y , v2 + 1)} 0")
                            else:
                                for v1 in range(self.n):
                                    for v2 in range(v1, self.n):
                                        rv.append(f"-{self.gen_id(x, y, v2 + 1)} -{self.gen_id(x + 1, y, v1 + 1)} 0")
                        elif self.v_sign[x][y]:
                            rv.append(" ".join([f"{self.gen_id(x, y + 1, v + 1)}" for v in range(self.values[x][y])]) + " 0")
                        else:
                            rv.append(" ".join([str(self.gen_id(x , y+1, v+1)) for v in range(self.values[x][y] , self.n)]) + " 0")
                    elif self.values[x][y+1] != 0:
                        if self.v_sign[x][y]:
                            rv.append(" ".join([str(self.gen_id(x, y, v+1)) for v in range(self.values[x][y+1] , self.n)]) + " 0")
                        else:
                            rv.append(" ".join([str(self.gen_id(x,y,v+1)) for v in range(self.values[x][y+1])]) + " ")
                    elif self.v_sign[x][y]:
                        for v1 in range(self.n):
                            for v2 in range(v1, self.n):
                                rv.append(f"-{self.gen_id(x, y, v1 + 1)} -{self.gen_id(x + 1, y, v2 + 1)} 0")
                    else:
                        for v1 in range(self.n):
                            for v2 in range(v1, self.n):
                                rv.append(f"-{self.gen_id(x, y, v2 + 1)} -{self.gen_id(x+1, y, v1 + 1)} 0")
        return rv

    def gen_clauses(self: Self) -> list[str]:
        """"""
        return [
            *self.gen_c_clauses(),
            *self.gen_h_clauses(),
            *self.gen_v_clauses(),
            *self.gen_h_sign_clauses(),
            *self.gen_v_sign_clauses()
        ]

    def gen_dimacs(self: Self) -> str:
        """"""
        cl = self.gen_clauses()
        return f"p cnf {self.n ** 3} {len(cl)}\n" + "\n".join(cl)
