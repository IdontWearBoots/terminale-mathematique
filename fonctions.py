import re
from math import cos, sin, tan

class Fonction:
    def __init__(self, n:str, exp:str) -> None:
        self.nom = f"{n}(x)"
        self.exec = Fonction.parse_expression(exp)
        self.exp = f"{self.nom} = {exp}"

    def to_tuple(self):
        return (self.exp, self.exec)

    @staticmethod
    # renvoi (Maximum, en x) <== en x ne marche pas encore
    def maxi(s:int, e:int, f:callable, p:int) -> tuple:
        l = list(map(f, range(s, e + 1, p)))
        M = float(max(*l))
        return (M, l.index(M))
    @staticmethod
    # même chose: renvoi (minimum, en x)  <== en x ne marche pas encore
    def mini(s:int, e:int, f:callable, p:int) -> tuple:
        # reversed pour avoir l'ordre
        l = list(map(f, range(s, e + 1, p)))
        m = float(min(*l))
        return (m, l.index(m))

    @staticmethod
    def parse_expression(exp:str) -> callable:
        if Fonction.expression_valide(exp):
            return lambda x: eval(exp)

    @staticmethod
    def expression_valide(exp:str) -> bool:
        exp = exp.replace(" ", "")

        # regex amélioré
        chars = r"[\dx)(+/*-]|(?:cos)|(?:tan)|(?:sin)"
        z = re.findall(chars, exp)

        # verifie que :
        #       1) l'expression ne contient que les caractères permises (+, -, /, *, nombre, cos, sin, tan)
        #       2) la dernier caractère soit soit un nombre, ), ou x
        #       3) le premier caractère soit soit un nombre, (, c de cos, s de sin, t de tan, - ou x
        return "".join(z) == exp and re.match(r"[\dx)]", exp[-1]) != None and re.match(r"[\dx(cst-]", exp[0]) != None

    @staticmethod
    def conventions_expressions(lst) -> str:
        out = "\tCe programme a été conçu de façon que les expressions de fonction doivent obeir a 4 règles: \n"
        out += "\t\t1) Que les expressions ne contiennent que de la trigo de base (en radians) ainsi que des symboles d'arithmétique (les paranthèses aussi). \n"
        out += "\t\t2) Que la trigo soit : cos() -> cosinus, sin() -> sinus et tan() -> tangeante. \n"
        out += "\t\t3) Que les expressions n'ont pas de réferences à d'autres fonctions ni à d'autres variables. \n"
        out += "\t\t4) Que les expressions ne commencent pas ou ne finissent pas par de symboles d'arithmétique (à l'exception de - pour nombres négatifs). \n"
        out += "\t\t5) Que les expressions NE CONTIENNENT AUCUN ESPACE car cela va casser le programme et supprimer tous les données crées. \n"
        out += "\tDu moment ou vos expressions de fonctions obéissent à ces règles, tout marche (normalement). \n"
        return out

class Plot:
    def __init__(self, n:str, s:int, e:int, p:int) -> None:
        self.nom = n
        self.deb = s
        self.fin = e
        self.pas = p
        self.fonctions = []
        self.maximums = []
        self.minimums = []

    def add_fonction(self, f:Fonction) -> None:
        self.fonctions.append(f)
        dernier = len(self.fonctions) - 1
        self.maximums = [Fonction.maxi(self.deb, self.fin, self.fonctions[dernier].exec, self.pas)]
        self.minimums = [Fonction.mini(self.deb, self.fin, self.fonctions[dernier].exec, self.pas)]

    def get_fonction(self, index:int) -> tuple:
        return (*self.fonctions[index].to_tuple(), self.maximums[index], self.minimums[index])

    def to_string(self) -> str:
        return f"L'intervalle {self.nom} = [{self.deb} ; {self.fin}], elle contient {len(self.maximums)} fonctions"

    def extrema(self) -> str:
        out = "\t" + self.to_string() + "\n"
        for i in range(0, len(self.fonctions)):
            M = self.maximums[i]
            m = self.minimums[i]
            f = self.fonctions[i]
            # TODO: ajout de l'antecedant du maximum et du minimum ('admet max de y en x = z')
            #   ^
            out += f"\t\t1. La fonction {f.nom}: admet un maximum de {M[0]} en et un minimum de {m[0]}\n"

        return out
