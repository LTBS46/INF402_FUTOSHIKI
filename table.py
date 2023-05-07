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
from math import log10, floor


class table(object):
    """
    constructeur de la table
    prend comme argument
    - soit un entier: et construit une table vide
    - soit une chaine de caractères : et le decompose en objet json

    """
    def __init__(self: Self, i: int | str = 5) -> None:
        """"""
        _t = type(i)
        if _t == int:
            if i > 0:
                self.n = i
                self.values : list[list[int]] = [[0 for m in range(i)] for l in range(i)]
                self.h_sign = [[None for m in range(i)] for l in range(i - 1)]
                self.v_sign = [[None for m in range(i - 1)] for l in range(i)]
                self._s : int = floor(log10(self.n)) + 1
            else:
                raise ValueError()
        elif _t == str:
            _v = loads(i)
            self.__init__(_v["size"])
            # TODO
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
        rv : list[str] = list((("-" * self._s).join(["|" for i in range(self.n + 1)]) + "\n").join(
            map(lambda _x: _x + "\n", ["", *[
                "|".join(["", *[
                    self._pad_f(str(self.values[x][y]) if self.values[x][y] != 0 else "")
                    for y in range(self.n)
                ], ""]) for x in range(self.n)
            ], ""])
        )[1:])
        h_base_off = 3 + self.n + self._s * self.n + self._s
        h_x_off = 1 + self._s
        h_y_off = 2 * (self.n + self._s * self.n + self._s)
        v_base_off = 2 * (2 + self._s * self.n + self.n) + 1
        v_x_off = 1 + self._s
        v_y_off = 2 * (2 + self._s * self.n + self.n)
        for x in range(self.n):
            for y in range(self.n):
                if y + 1 < self.n:
                    if self.v_sign[x][y] is not None:
                        rv[v_base_off + v_x_off * x + v_y_off * y
                        ] = "v" if self.v_sign[x][y] else "^"
                if x + 1 < self.n:
                    if self.h_sign[x][y] is not None:
                        rv[h_base_off + h_x_off * x + h_y_off * y
                        ] = ">" if self.h_sign[x][y] else "<"
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
        if v is None:
            v = 0
        elif not -self.n < v < self.n:
            raise ValueError()
        self.values[x][y] = v        

    def set_v_sign_at(self: Self, x: int, y: int, v: bool | None) -> None:
        """
    
        """
        self.v_sign[x][y] = v

    def set_h_sign_at(self: Self, x: int, y: int, v: bool | None) -> None:
        """
    
        """
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
        if x is None:
            return sum([self.gen_v_clauses(_x) for _x in range(self.n)], [])
        else:
            return sum([[   # la valeur est deja dans la colone
                f"-{self.gen_id(x, y + 1, v)} 0"
                for y in range(self.n) if y != self.values[x].index(v + 1)
            ] if v + 1 in self.values[x] else [
                # la valeur doit etre dans la colonne au moins une fois
                " ".join(str(self.gen_id(x, y, v + 1)) for y in range(self.n) if not self.values[x][y]) + " 0",
                # la valeur ne doit pas être présente plusieurs fois
                *[
                    f"-{self.gen_id(x, y, v + 1)} {self.gen_id(x, y2, v + 1)} 0"
                    for y in range(self.n) for y2 in range(y + 1, self.n)
                ]
            ] for v in range(self.n)], [])

    def gen_h_clauses(self: Self) -> list[str]:
        """
    
        """
        return []

    def gen_h_sign_clauses(self: Self) -> list[str]:
        """
    
        """
        return sum([
            # si supérieur
            (
                # valeur seulement du côte inférieur
                [" ".join([
                    self.gen_id(x, y, v + 1) for v in range(self.values[x][y + 1], self.n)
                ]) + " 0", "-" + " -".join([
                    self.gen_id(x, y, v + 1) for v in range(self.values[x][y + 1])
                ]) + " 0"]
                if self.values[x][y + 1] else
                # aucune valeur autour du signe
                []
            ) if self.h_sign[x][y] else (            # si inférieur
                []
                if self.values[x][y + 1] else
                # aucune valeur autour du signe
                []
            )
            for x in range(self.n - 2) for y in range(self.n) if self.h_sign[x][y] is not None and not self.values[x][y]
        ], []) + sum([
            ([] if self.values[self.n - 1][y] else (

            )) if self.values[self.n - 2][y] else ((

            ) if self.values[self.n - 1][y] else (

            ))
            for y in range(self.n) if self.h_sign[self.n - 2][y] is not None
        ], [])
        
    def gen_v_sign_clauses(self: Self) -> list[str]:
        """"""
        return []

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
