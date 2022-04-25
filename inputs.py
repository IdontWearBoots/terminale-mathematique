# j'ai du faire ça car .is_decimal est une méthode de str donc impossible
# d'utiliser des paramètres spéciaux (voir utilisation dans main.py dans new_intervalle)
def is_decimal(n:str):
    return n.isdecimal()

# j'ai du créer ce système de dialogue parceque sinon je faisait quelque chose dans le genre de :
#   n = input("Nom: ")
#   while not n in tous_nom:
#       print("Erreur")
#       n = input("Nom: ")
# a chaque fois qu'il me fallait un input
# qui a fini par faire trop de lignes donc
class Question:
    def __init__(self, mess_ques:str, verifie:callable, mess_err:str) -> None:
        self.ques = mess_ques
        self.verifieur = verifie
        self.erreur = mess_err

class Form:
    def __init__(self, ques:list) -> None:
        self.questions = ques
    def ask(self, tous_noms:list) -> list:
        reponses = []

        # j'aime beaucoup ce bloc de code
        for q in self.questions:
            end = "Erreur"
            while end == "Erreur":
                e = input(q.ques)

                if e == "exit":
                    return [None]*len(self.questions)

                #bool(e) verifie si il y a une valeure
                if not bool(e):
                    print("\tIl faut donner une valeure. Pour quitter taper 'exit'")

                if not q.verifieur(e, tous_noms):
                    print(q.erreur)
                    continue
                end = "pas d'erreur"
                reponses.append(e)

        return reponses
