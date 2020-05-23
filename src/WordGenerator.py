import sys
import re
import requests

from bs4 import BeautifulSoup

# Enlever une certains caractères dans une chaine de caractère
def rchop(thestring, ending):
    if thestring.endswith(ending):
        return thestring[:-len(ending)]
    return thestring

# Fonction d'affichage
def info(*args, **kwargs):
    rulesArg = kwargs.get("rulesArg", False)
    wordArg = kwargs.get("wordArg", True)
    resultArg = kwargs.get("resultArg", True)
    
    if(rulesArg):
        print(f'\nLes règles :')
        pprint(rules)

    if(wordArg):
        print(f'\nLe mot : {testWord}')

    if(resultArg):
        print(f'\nLes dérivations :')
        for n in result.items():
            print(str(n).replace(',', ' ->'))

def usage():
	print(f'Set arguments')
	sys.exit()

if(len(sys.argv) != 3):
	usage()

# Déclarations des variables
rules = []
result = {}
testWord = sys.argv[1]
natureWord = sys.argv[2]

# Ouverture du fichier
file = open("rules.txt", "r")

# Lecture du fichier & enregistrement des règles
if file.mode == 'r':
    lines = file.readlines()
    for line in lines:
        rules.append(line.rstrip("\n").split("==>"))

# Fermeture du fichier
file.close()

# Génération des mots et leur nature
for rule in rules:
    ruleG = rule[0].split(":")
    ruleD = rule[1].split(":")
    match = re.match(".*" + ruleG[1], testWord)
    if match and ruleG[0] == natureWord:
        if ruleG[1] != "":
            generatedWord = rchop(testWord, ruleG[1]) + ruleD[1]
            result[generatedWord] = ruleD[0]
        else:
            generatedWord = testWord + ruleD[1]
            result[generatedWord] = ruleD[0]

# Fonction d'affichage (avec possibilité d'afficher que ce qui nous intéresse)
info(rulesArg = False, wordArg = False, resultArg = False)

# Partie jdm
final = []
for word in result:
    # Envoie de la requete à jdm
    url = "http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + str(word) + "&rel="
    
    # Reponse de la requete
    response = requests.get(url)
    
    # bs4
    soup = BeautifulSoup(response.text, features = 'lxml')
    
    # Chercher la balise "jdm-warning"
    mydivs = soup.findAll("div", {"class": "jdm-warning"})
    
    if(mydivs): # if jdm-warning existe (mot invalide)
        print(f'le mot {word} n\'existe pas\n')
    else: # else (mot valide)
        print(f'le mot {word} existe\n')    
        final.append(word)
    
if(final):
    print('Les mots valides sont :')
    for f in final:
        print(f'\t{f} : {result[f]}')
else:
    print('Aucun mot n\'est valide')