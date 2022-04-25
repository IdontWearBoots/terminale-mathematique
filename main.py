from terminal import *
from inputs import Question, Form, is_decimal
from fonctions import Plot, Fonction
from init import *

t.set_cmds(cmds)
t.aide = aide
if __name__ == "__main__":
	print("Appeler 'aide -all' pour voir tous les commandes disponibles.")
	print("Si jamais vous devez sortir du programme, écrivez exit, cela vous sortirait de n'importe quel dialogue et mettra fin au programme si il est utilisé comme commande.")
	print("\n")

	t.run()
