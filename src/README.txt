# Authors
* Meriem AMERAOUI.
* Dounia BELABIOD.
* Bahaa Eddine NIL.

# Langage utilisé
Python.

# Files
Le projet est constitué des fichiers suivant :
* WordGenerator.py : fichier python de notre programme.
* WordGenerator.ipynb notebook de notre programme (même que le 'WordGenerator.pyt').
* rules.txt : fichier texte qui contient les règles.

# Exécution du fichier Python WordGenerator.py 
Pour exécuter le programme qui se trouve dans WordGenerator.py, il faudra se rendre dans le dossier où se trouve ce dernier (le dossier src), puis ouvrir un terminal pour le lancer à l’aide de la commande suivante : python WordGenerator.py <mot> <nature_mot>. Oû mot est le mot que nous souhaitons dériver et nature_mot est la nature du mot (saisir V pour Verbe, N pour Nom, ADJ pour Adjectif et NP pour Nom propre).

# Exécution du notebook WordGenerator.ipynb
Il faut ouvrir le fichier WordGenerator.ipynb, qui est dans le dossier src du projet avec Jupyter, puis exécuter les cellules, arrivé à la troisième cellule il faudra saisir un mot dans le champs qui s’affiche puis saisir sa nature. Après continuer l'exécution des cellules restantes. 

# Explication de la conception
L’objectif du projet est de générer des mots et en appliquant des règles à partir d’un fichier texte 'rules.txtt', les mots générés doivent exister dans le réseau du site JeuxDeMots sous certaines conditions.

Un programme python permettant à partir d'un terme donné par l'utilisateur de produire tous les termes possibles par dérivation morphologique. Les termes produits peuvent exister dans la langue (français) ou ne pas exister. Si un terme produit existe, il peut éventuellement avoir dans la langue, une sémantique différente de celle voulue. 

Le programme interprète des règles stockées dans un fichier à part (rules.txt) et génère toutes les dérivations possibles du mot saisi par l’utilisateur, suivis de leurs nature.

Les mots générés sont ensuite triés en envoyant des requêtes au rezo dump de JeuxDeMots pour générer la liste finale de mots. 

Une recherche de la balise "jdm-warningt' est faite dans un premier temps, pour savoir rapidement si le mot généré existe dans jeuxdemots. Si ce dernier n’existe pas, il n’appartiendra donc pas à la liste finale des mots générés. 

Cette liste est encore filtrée, une requête paramétrée par le mot donné par l’utilisateur est envoyée pour récupérer la balise 'codet', une vérification dans le résultat de celle-ci est faite pour savoir si les mots de la liste ont une quelconque relation avec ce mot (le mot donné par l’utilisateur). Les mots existants dans le rézo dump de JeuxDeMots et qui sont en relation avec le mot donné par l’utilisateur sont stockés dans une nouvelle liste.

L’étape suivante est la vérification de la nature des mots de la liste de mots générés, pour cela, et pour chaque mot de cette liste, de nouvelles requêtes paramétrées par le mot et le numéro de la relation sont envoyés à JeuxDeMots via le rezo dump, la balise 'codet' est récupérée car elle contient des informations sur le mot et ses différentes relations.

Nous cherchons le noeud avec nos mots et leurs nature générées par notre programme, s’il existe dans la balise 'codet'. Puis nous récupérons leurs identifiants et nous cherchons s’il existe une relation qui regroupe les deux identifiants. Dû à la structure particulière des noeuds et les relations du rezo dump de JeuxDeMots, des expressions régulières ont été utilisées pour effectuer les différentes vérifications.
Si à l’issu de la vérification la relation est trouvée, les termes avec leur nature qui correspond aux résultats de JeuxDeMots sont stockés dans une nouvelle liste qui contient nos mots finaux. 



# Exemple avec le mot manger qui est un verbe
-A la saisie du mot 'mangert' et sa nature 'Vt' vu que c’est un verbe, une première liste est affichée contenant tous les termes générés par dérivation morphologique en utilisant les règles du fichier 'rules.txtt'. Les termes produits peuvent exister dans la langue française ou pas.
 Le programme affiche la liste ci-dessous.

Les dérivations du mot  'manger' :
	mangage de nature N
	mangement de nature N
	mangeur de nature N
	mangeuse de nature AGENT
	mangateur de nature AGENT
	mangoire de nature LIEU
	mangoir de nature LIEU
	mangatoire de nature LIEU
	mange de nature V
	manges de nature V
	mangons de nature V
	mangez de nature V
	mangent de nature V
	mangeons de nature V
	mangant de nature N
	mangette de nature N
	mangable de nature N
	mangible de nature ADJ
	mangail de nature N
	mangaille de nature N
	mangation de nature N
	mangeoire de nature LIEU
	mangeriteur de nature N
	mangerateur de nature N

-Après la vérification de l'existence de ces mots dans JeuxDeMots une nouvelle liste est générée.

Les mots existants dans jeux de mots :
	mangement de nature N
	mangeur de nature N
	mangeuse de nature AGENT
	mange de nature V
	manges de nature V
	mangez de nature V
	mangent de nature V
	mangeons de nature V
	mangeoire de nature LIEU

-Les termes mangement, mangeuse et mangeoire ont été supprimés de la liste précédente car même s’ils existent dans JeuxDeMots ces derniers n’ont aucune relation qui les lient à 'mangert'.

Les mots existants dans jeux de mots qui sont en relation (r0) avec le mot 'manger' :
	mangeur de nature N
	mange de nature V
	manges de nature V
	mangez de nature V
	mangent de nature V
	mangeons de nature V

-Dans cette dernière étape, nous allons s’intéresser à la nature de chaque mot restant dans la liste précédente (générée à l’étape d’avant), pour ne garder que les mots avec leur bonne nature, ce qui nous donne le résultat suivant :

Les mots finaux sont :
	mangeur de nature N
	mange de nature V
	manges de nature V
	mangez de nature V
	mangent de nature V
	mangeons de nature V

# Un autre exemple avec le mot 'lait' qui est un nom
-Cette fois nous saisissons N dans le champs de la nature du nom vu que c’est un nom.
Exactement comme le déroulement de l’exemple précedent, nous avons les résultats suivants dans l’ordre :

Les dérivations du mot  'lait' :
	laitaison de nature N
	laitable de nature ADJ
	laitage de nature N
	laitisme de nature N
	laitiste de nature N
	laitir de nature V
	laitaire de nature N
	laitiaire de nature N
	laitale de nature ADJ
	laital de nature ADJ
	laitelle de nature ADJ
	laitacé de nature ADJ
	laitan de nature ADJ
	laitane de nature ADJ
	laitain de nature ADJ
	laitaine de nature ADJ
	laitard de nature N
	laitarde de nature N

Les mots existants dans jeux de mots :
	laitage de nature N

Les mots existants dans jeux de mots qui sont en relation (r0) avec le mot 'lait' :
	laitage de nature N

-A la fin nous avons un seul mot généré.

Les mots finaux sont :
	laitage de nature N