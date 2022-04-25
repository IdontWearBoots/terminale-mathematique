from terminal import *
from inputs import Question, Form, is_decimal
from fonctions import Plot, Fonction

t = Terminal("==>", None, None)

# arguments par défaut permettent de faire:
# fonction -new ${params de fonction}
# au lieu de devoir passer par la creation de fonction
# ceci n'est pas recommandé car je n'ai pas encore implimenté la verification de parmètres données.
# On pourra donc faire 'fonction -new 17 nom' => entrainant une erreur qui supprime tous les données crées
# TODO : fix inline func creation (so that its safe) -> currently no checking for param types etc
def new_fonction(n=None, expr=None) -> str:
    global t
    noms_fonc = list(map(lambda x: x.nom, t.fonctions))

    if n != None and expr != None:
        t.add_fonction(Fonction(n, expr))
        return f"\t{n}(x) = {expr} à été crée."

    q1 = Question(*[
        "\tDonnez le nom de la fonction (ne pas inclure (x)): ",
        lambda n, tn: not(n in tn),
        "\t" + ErrorMessage.FONCTION_EXISTE_MEME_NOM.value
    ])
    q2 = Question(*[
        "\tDonnez l'expression de la fonction: ",
        lambda exp, tn: Fonction.expression_valide(exp),
        "\t" + ErrorMessage.EXPRESSION_FONCTION_NON_VALIDE.value
    ])
    form = Form([q1, q2])

    nom, exp = form.ask(noms_fonc)

    if nom == None and exp == None:
        return ""

    t.add_fonction(Fonction(nom, exp))
    return f"\t{nom}(x) = {exp} à été crée."


# TODO : fix inline func creation (so that its safe) -> currently no checking for param types etc
def new_intervalle(n=None, s=None, e=None, p=None) -> str:
    global t
    noms_plot = list(map(lambda x: x.nom, t.intervalles))

    # pour faire une déclaration en une ligne
    if n != None and s != None and e != None and p != None:
        t.add_intervalle(Plot(n, int(s), int(e), int(p)))
        return f"\tIntervalle {n} à été crée."

    q1 = Question(*[
        "\tDonnez le nom de l'intervalle: ",
        lambda n, tn: not(n in tn),
        "\t" + ErrorMessage.INTERVALLE_EXISTE_MEME_NOM.value
    ])
    q2 = Question(*[
        "\tDonnez la borne inférieure de l'intervalle: ",
        lambda inf, tn: is_decimal(inf[1:len(inf)] if inf[0] == "-" else inf),
        "\t" + ErrorMessage.VALEUR_PAS_ENTIER.value
    ])
    q3 = Question(*[
        "\tDonnez la borne supérieure de l'intervalle: ",
        lambda sup, tn: is_decimal(sup[1:len(sup)] if sup[0] == "-" else sup),
        "\t" + ErrorMessage.VALEUR_PAS_ENTIER.value
    ])
    q4 = Question(*[
        "\tDonnez le pas de ballayage de l'intervalle (entier naturel): ",
        lambda p, tn: is_decimal(p),
        "\t" + ErrorMessage.VALEUR_PAS_ENTIER_NATUREL.value
    ])
    form = Form([q1, q2, q3, q4])
    nom, inf, sup, pas = form.ask(noms_plot)


    if nom == None and inf == None and sup == None and pas == None:
        return ""

    t.add_intervalle(Plot(nom, int(inf), int(sup), int(pas)))
    return f"\tIntervalle {nom} à été crée."


# commande "aide"
flags = {
    "-all": CommandeAide.aide_toutes,
    "-cmd": CommandeAide.aide_nom,
    "-obj": t.info,
    "-exp": Fonction.conventions_expressions
}
desc = [
    "commande qui informe sur les autres commandes",
    "-all: donne la description briève de tous les autres commandes",
    "-cmd $NOM_COMMANDE: donne la description complète de la commande donnée (remplacer $NOM_COMMANDE par la commande que vous voulez)",
    "-obj: informe sur tous les objets crées (instantiés)",
    "-exp: donne les conventions d'écriture de fonction (très utile si vous voulez creer des fonctions)"
]
aide = CommandeAide("aide", flags, desc)

# commande "fonction"
flags = {
    "-new": new_fonction,
    "-del": t.remove_fonction
}
desc = [
    "commande qui crée et gère les fonctions",
    "-new [nom_f, exp]: instantie une nouvelle fonction",
    "-del [nom_f]: supprime une fonction déjà crée"
]
fonction = Commande("fonction", flags, desc)

# commande "intervalle"
flags = {
    "-new": new_intervalle,
    "-add": t.add_fonction_to_intervalle,
    "-del": t.remove_intervalle,
    "-extr": t.get_intervalle_info
}
desc = [
    "commande qui crée et gère les intervalles",
    "-new [nom_i, b_inf, b_sup, pas]: instantie une nouvelle intervalle",
    "-add [nom_i, nom_f]: ajoute la fonction donnée à l'intervalle donnée",
    "-del [nom_i]: supprime une intervalle déjà crée",
    "-extr [nom_i]: donne les extrema des fonctions présentes sur l'intervalle."
]
intervalle = Commande("intervalle", flags, desc)

# commande "echo"
flags = {
    # j'aime bien aussi ce code
    "-text": lambda *args: print("\t", *[e for e in args]),
    "-hex": lambda *args: print("\t", *[str(hex(int(x))) for x in args]),
    "-bin": lambda *args: print("\t", *[str(bin(int(x))) for x in args])
}
desc = [
    "commande qui écrit quelque chose dans la console",
    "-text *args: écrit les arguments (*args) à la console",
    "-hex *args: écrit les nombres données en hexadécimal à la console.\n\t            Il faut que LES ARGUMENTS SOIENT DES NOMBRES sinon le programme casse et les données crées perdus.",
    "-bin *args: même chose que -hex mais en binaire"
]
echo = Commande("echo", flags, desc)

cmds = [
    aide,
    fonction,
    intervalle,
    echo
]
