# nos fichier, cf : celui qui l'ecrit

None

# librarie standard, cf : internet

from subprocess import run, DEVNULL
from collections.abc import Callable
from tempfile import mkstemp
from os import close, fdopen, remove

solver_data: dict[str, Callable[[str], str]] = {}

def get_solver(sat: str):
    """
    
    """
    return solver_data[sat]

def solve(dimacs : str, sat: str = "minisat") -> str:
    """
    
    """
    return get_solver(sat)(dimacs)

def solver(func: Callable[[str], str]):
    """

    """
    solver_data[func.__name__] = func

@solver
def minisat(dimacs : str) -> str:
    """

    """
    fd_in, path_in = mkstemp(text=True)
    f_in = fdopen(fd_in, mode="w")
    f_in.write(dimacs)
    f_in.close()
    fd_out, path_out = mkstemp(text=True)
    close(fd_out)
    # j'aurais pus utiliser os.system mais ca aurais pouri la console pour le mode texte
    v = run(
        ["minisat", path_in, path_out],
        stderr=DEVNULL,
        stdout=DEVNULL,
        stdin=DEVNULL
    )
    code = v.returncode
    remove(path_in)
    rv = ""
    if code == 10:
        with open(path_out, "r") as f:
            rv = f.read(None)
        remove(path_out)
        return rv
    if code == 20:
        return "UNSAT"
    else:
        remove(path_out)
        print(code)
        raise ValueError()

__all__ = ["solve", "solver"]