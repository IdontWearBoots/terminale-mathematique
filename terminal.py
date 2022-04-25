from enum import Enum
from fonctions import Fonction, Plot
from inputs import Form, Question

# un Enum pour tous les messages d'erreurs que je dois appeler
# L'Enum était le plus facile pour se retrouver dans le code
class ErrorMessage(Enum):
    MESSAGE_AIDE_COMMANDE = "Appeler 'aide -cmd $NOM_COMMANDE' pour s'informer sur la commande."
    MESSAGE_AIDE_TOUS_COMMANDES = "Appeler 'aide -all' pour s'informer sur les commandes a disposition."
    MESSAGE_AIDE_TOUS_OBJETS = "Appeler 'aide -obj' pour voir les intervalles et fonctions déjà crées."
    MESSAGE_AIDE_EXPRESSION_FONCTION = "Appeler 'aide -exp' pour voir comment bien écrire une fonction."

    FONCTION_EXISTE_MEME_NOM = "Il existe déja une fonction avec ce nom."
    INTERVALLE_EXISTE_MEME_NOM = "Il existe déjà une intervalle avec ce nom."

    FONCTION_NON_EXISTANTE = "Aucune fonction ayant ce nom. " + MESSAGE_AIDE_TOUS_OBJETS
    INTERVALLE_NON_EXISTANTE = "Aucune intervalle ayant ce nom. " + MESSAGE_AIDE_TOUS_OBJETS

    MANQUE_DECORATEUR = "Il faut un décorateur. " + MESSAGE_AIDE_COMMANDE
    DECORATEUR_NON_EXISTANT = "Le décorateur utilisé n'éxiste pas. " + MESSAGE_AIDE_COMMANDE

    COMMANDE_NON_EXISTANT = "La commande appelé n'existe pas. " + MESSAGE_AIDE_TOUS_COMMANDES
    MAUVAISE_UTLISATION_COMMANDE = "Mauvaise utilisation de la commande. " + MESSAGE_AIDE_COMMANDE

    EXPRESSION_FONCTION_NON_VALIDE = "Expression non valide. " + MESSAGE_AIDE_EXPRESSION_FONCTION

    VALEUR_PAS_ENTIER = "Valeure donnée n'est pas un entier."
    VALEUR_PAS_ENTIER_NATUREL = "Valeure donnée n'est pas un entier naturel."

class Commande:
    def __init__(self, trig:str, flags:dict, desc:list) -> None:
        self.trigger = trig
        self.flags = flags
        # l'idée générale pour la desciption est d'avoir une liste.
        # le premier element est la description de la fonction (truc fait cela)
        # puis les autres sont par rapport au décorateurs et comment les utiliser (-x [4 args] crée un noveau truc)
        self.description = desc

    # TODO: complete the .to_string method => include flags + desc of flags potentialy
    # ^ still not to sure if should just add one large description of everything at the beegining or
    def to_string(self) -> str:
        return f"{self.trigger} : {self.description[0]}"

    def exec(self, line:list) -> str:
        # si il y a un décorateur
        if len(line) == 1:
            return "\t" + ErrorMessage.MANQUE_DECORATEUR.value
        # si le décorateur utilisé existe
        if not line[1] in self.flags:
            return "\t" +  ErrorMessage.DECORATEUR_NON_EXISTANT.value

        # deuxième partie la plus importante de tout le programme
        action = self.flags[line[1]]
        return action(*line[2:len(line)])

# CommandeAide diffère juste un peu d'une commande normale
class CommandeAide(Commande):
    def __init__(self, trig:str, flags:dict, desc:list) -> None:
        super().__init__(trig, flags, desc)

    def exec(self, line:str, lst:list = []) -> str:
        if not line[1] in self.flags:
            return "\t" + ErrorMessage.DECORATEUR_NON_EXISTANT.value

        action = self.flags[line[1]]
        return action(lst, *line[2:len(line)])

    @staticmethod
    def aide_toutes(lst:list):
        out = "\t"
        for cmd in lst:
            # pourrait être "yield" pour retourner mais problematique plus tard
            out += cmd.to_string() + "\n\t"
        # même si ce n'est pas une erreur
        out += ErrorMessage.MESSAGE_AIDE_COMMANDE.value
        return out

    @staticmethod
    def aide_nom(lst:list, nom:str=None):
        # on doit fournir un nom pour que ça fonctionne
        if nom == None:
            return "\t" + ErrorMessage.MAUVAISE_UTLISATION_COMMANDE.value

        # comment sont appelés [] ?
        print("\tLes mots entre [] sont des paramètres optionels, vous n'êtes pas obligées de les mettre pour exécuter la fonction.")
        print("\tCeux qui sont en majuscules avec $ devant sont obligés, il faut les mettre pour exécuter la commande.")
        print("\t*args signifie que tu peut mettre autant de paramètres que vous voulez.\n")

        # filter ne marche pas (erreur si l'objet n'existe pas) => je pourais utiliser un try/catch mais ça marche comme ça
        for cmd in lst:
            if cmd.trigger == nom:
                debut = f"\tLa commande {cmd.trigger} est une {cmd.description[0]}. Elle à {len(cmd.description) - 1} décorateurs: \n\t\t"
                return debut + "\n\t\t".join(cmd.description[1:len(cmd.description)]) + "\n"
        return "\t" + ErrorMessage.COMMANDE_NON_EXISTANT.value


class Terminal:
    def __init__(self, nl:str, aide:CommandeAide, cmds:list):
        self.newline = nl
        self.aide = aide
        self.commandes = cmds

        self.fonctions = []
        self.intervalles = []

        # en gros ce qui va être écrit a la console a chaque fois qu'on veut connaitre les objets crées
        self.fonctions_info = []
        self.intervalles_info = []

        # command_triggs est une list de tous les noms de commandes, c'est donc un problème quand commandes est None
        if cmds != None:
            self.command_triggs = list(map(lambda f: f.trigger, cmds))

    # seulment parce qu'au final dans le main.py j'instantie les commandes après la terminale
    def set_cmds(self, lst:list) -> None:
        self.commandes = lst
        self.command_triggs = list(map(lambda f: f.trigger, lst))

    # creation de fonction et d'intervalle
    def add_fonction(self, f:Fonction) -> None:
        self.fonctions.append(f)
        self.fonctions_info.append(f.exp)
    def add_intervalle(self, p:Plot) -> None:
        self.intervalles.append(p)
        self.intervalles_info.append(p.to_string())

    # intervalle -add => ajouter une fonction a une intervalle
    def add_fonction_to_intervalle(self, np=None, nf=None) -> str:
        toutes_nom_intervalles = list(map(lambda plot: plot.nom, self.intervalles))
        toutes_nom_fonctions = list(map(lambda f: f.nom[0:f.nom.index("(")], self.fonctions))

        if not (np == None and nf == None):
            # très moche mais bon
            self.intervalles[toutes_nom_intervalles.index(np)].add_fonction(self.fonctions[toutes_nom_fonctions.index(nf)])
            return f"\t{nf} à été ajouté à l'intervalle {np}."

        print(self.info(None))

        q1 = Question(*[
            "\tDonnez le nom de l'intervalle sur laquelle vous voulez ajouter une fonction: ",
            lambda n, tn: n in tn,
            "\t" + ErrorMessage.INTERVALLE_NON_EXISTANTE.value
        ])
        q2 = Question(*[
            "\tDonnez le nom de la fonction que vous voulez ajouter a l'intervalle: ",
            lambda n, tn: n in tn,
            "\t" + ErrorMessage.FONCTION_NON_EXISTANTE.value
        ])

        form = Form([q1])
        nom_plot = "".join(form.ask(toutes_nom_intervalles))
        if nom_plot == "None":
            return "\n"

        form = Form([q2])
        nom_fonc = "".join(form.ask(toutes_nom_fonctions))
        if nom_fonc == "None":
            return "\n"

        index_plot = toutes_nom_intervalles.index(nom_plot)
        index_fonc = toutes_nom_fonctions.index(nom_fonc)

        plot = self.intervalles[index_plot]
        plot.add_fonction(self.fonctions[index_fonc])
        self.intervalles_info[index_plot] = plot.to_string()

        return f"\t{nom_fonc} à été ajouté à l'intervalle {nom_plot}."

    # pour enlever une fonction au cas ou
    def remove_fonction(self, nom:str=None) -> str:
        i = 0
        noms_fonc = list(map(lambda f: f.nom[0:f.nom.index("(")], self.fonctions))

        if nom == None:
            q = Question(*[
                "\tDonnez le nom de la fonction à supprimer (sans (x)): ",
                lambda n, tn: n in tn,
                "\t" + ErrorMessage.FONCTION_NON_EXISTANTE.value
            ])
            form = Form([q])
            nom = "".join(form.ask(noms_fonc))

        if nom == "None":
            return "\n"

        if len(nom) == 1:
            nom += "(x)"
        for func in self.fonctions:
            if func.nom == nom:
                self.fonctions.pop(i)
                self.fonctions_info.pop(i)
                return f"\tFonction {nom} à été supprimé."
            i += 1

        return "\t" + ErrorMessage.FONCTION_NON_EXISTANTE.value

    def remove_intervalle(self, nom:str=None) -> str:
        i = 0
        noms_plot = list(map(lambda p: p.nom, self.intervalles))
        if nom == None:
            q = Question(*[
                "\tDonnez le nom de l'intervalle à supprimer: ",
                lambda n, tn: n in tn,
                "\t" + ErrorMessage.INTERVALLE_NON_EXISTANTE.value
            ])
            form = Form([q])
            nom = "".join(form.ask(noms_plot))

        if nom == "None":
            return "\n"

        for plot in self.intervalles:
            if plot.nom == nom:
                self.intervalles.pop(i)
                self.intervalles_info.pop(i)
                return f"\tIntervalle {nom} à été supprimé."
            i += 1

        return "\t" + ErrorMessage.INTERVALLE_NON_EXISTANTE.value

    def get_intervalle_info(self, nom:str=None) -> str:

        if nom == None:
            q = Question(*[
                "\tDonnez le nom de l'intervalle dont vous voulez connaître les extrema: ",
                lambda n, tn: n in tn,
                "\t" + ErrorMessage.INTERVALLE_NON_EXISTANTE.value
            ])
            form = Form([q])
            nom = "".join(form.ask(list(map(lambda p: p.nom, self.intervalles))))

        if nom == "None":
            return "\n"

        for p in self.intervalles:
            if p.nom == nom:
                return p.extrema()
        return "\t" + ErrorMessage.INTERVALLE_NON_EXISTANTE.value

    # 'lst' est juste la parceque je passe automatiquement la liste de tous les commandes
    # à chaque fonction 'aide' (voir l.194)
    def info(self, lst) -> str:
        out = "\tFonctions crées: \n"
        for func in self.fonctions_info:
            out += f"\t\t{func}\n"

        out += "\tIntervalles crées: \n"
        for plot in self.intervalles_info:
            out += f"\t\t{plot}\n"

        return out


    def run(self) -> None:

        print("")

        while True:
            # verifie que chaque element dans la liste est truthy (pas de "" qui causent des problemes)
            line = list(filter(bool, input(self.newline + " ").split(" ")))

            if not line:
                continue

            cmd = line[0]

            # verifie si l'on veut sortir de la terminal
            if cmd == "exit":
                return

            # verifie si la commande est la commande 'aide'
            if cmd == self.aide.trigger:
                print(self.aide.exec(line, self.commandes))
                continue

            # verifie que la commande existe
            if not cmd in self.command_triggs:
                print("\t" + ErrorMessage.COMMANDE_NON_EXISTANT.value)
                continue

            index = self.command_triggs.index(cmd)

            # ! cmd passe d'un string a un objet !
            cmd = self.commandes[index]

            # tout se passe ici
            ret = cmd.exec(line)
            print("" if ret == None else ret)
