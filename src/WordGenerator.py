import re
import requests
import io
import itertools
import random
import sys

from IPython.display import clear_output
from bs4 import BeautifulSoup

# Enlever une certains caractères dans une chaine de caractère
def rchop(thestring, ending):
    if thestring.endswith(ending):
        return thestring[:-len(ending)]
    return thestring

# Fonction d'affichage de règles
def print_rules(bla):
    for rule in bla:
        print(str(rule).replace(', ', '==>'))

# Fonction d'affichage de mots
def print_results(bla):
    if(bla):
        for n in bla.items():
            temp = str(n).replace(", [", " de nature ").replace("[", "").replace("]", "").replace("'", "").replace("(", "").replace(")", "")
            print(f'\t{temp}')
    else:
        print('\tAucun')

# Génération des dictionnaires
def generate_dict(key, value):
    dicot = {}
    flag = False
    dicot.setdefault(key, [])
    if(len(dicot[key]) != 0):
        for n in dicot[key]:
            if(n == value):
                flag = True
        if(not flag):
            dicot[key].append(value)
    else:
        dicot[key].append(value)
    return dicot

# Type de natures
nature = {'Verbe': 'V', 'Nom': 'N', 'Adjectif': 'ADJ', 'Nom propre': 'NP'}

# L'utilisation du fichier en ligne de commande
def usage():
    print(f'python sys.argv[1] <mot> <nature_mot>')
    print(f'Veuillez choisir la nature du mot dans la liste ci-dessous :')
    for (key, value) in nature.items():
        print(f'\t{value} pour {key}')
    sys.exit()

if(len(sys.argv) != 3):
    usage()

# Déclarations des variables
rules = []
words_list1 = {}
testWord = sys.argv[1]
natureWord = sys.argv[2]

if(natureWord not in nature.values()):
    usage()

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
    flag = False
    ruleG = rule[0].split(":")
    ruleD = rule[1].split(":")
    match = re.match(".*" + ruleG[1], testWord)
    if match and ruleG[0] == natureWord:
        if ruleG[1] != "":
            generatedWord = rchop(testWord, ruleG[1]) + ruleD[1]
        else:
            generatedWord = testWord + ruleD[1]
        words_list1.update(generate_dict(generatedWord, ruleD[0]))

# Affichage des mots
print(f'\nLes dérivations du mot \'{testWord}\' :')
print_results(words_list1)

# Affichage des règles
#print_rules(rules)

# Mots existants dans jeux de mots
words_list2 = {}

for word in words_list1:
    # Envoie de la requete à jdm
    url = "http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + str(word) + "&rel="
    
    # Reponse de la requete
    response = requests.get(url)
    
    # bs4
    soup = BeautifulSoup(response.text, features = 'lxml')
    
    # Chercher la balise "jdm-warning"
    mydivs = soup.findAll("div", {"class": "jdm-warning"})
    
    # On ajoute le mot si jdm-warning n'existe pas
    if(not mydivs):
        words_list2.update(generate_dict(word, words_list1[word]))

# Affichage des mots
print('\nLes mots existants dans jeux de mots :')
print_results(words_list2)

# Mots en relation avec le mot de base
words_list3 = {}

for word in words_list2:
    a1 = ''
    # Envoie de la requete à jdm
    url = "http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + str(testWord) + "&rel=0"
    
    # Reponse de la requete
    response = requests.get(url)

    # bs4
    soup = BeautifulSoup(response.text, features = 'lxml')

    # Chercher la balise CODE
    mycode = soup.find('code')

    # Parcourir la balise CODE
    s = io.StringIO(str(mycode))
    for line in s:        
        if(re.match('e;.*;\'' + word + '\';.*;.*', line)):
            a1 = line.split(';')[1]
    
        if(a1):
            words_list3.update(generate_dict(word, words_list1[word]))

# Affichage des mots
print(f'\nLes mots existants dans jeux de mots qui sont en relation (r0) avec le mot \'{testWord}\' :')
print_results(words_list3)

relation_map = {'AGENT': '13', 'LIEU' : '15', 'N': '4', 'V': '4', 'ADJ': '4', 'ADV': '4'}
type_map = {'N': 'Nom:', 'V' : 'Ver:', 'ADJ' : 'Adj:', 'ADV' : 'Adv:'}
words_list4 = {}

for f in words_list3:   
    for k in itertools.chain.from_iterable(words_list3[f]):
        a1 = ''
        a2 = ''
        if(int(relation_map[k]) == 4):
            url = "http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + str(f) + "&rel=" + str(relation_map[k])

            # Reponse de la requete
            response = requests.get(url)

            # bs4
            soup = BeautifulSoup(response.text, features = 'lxml')
            
            # Chercher la balise CODE
            mycode = soup.find('code')

            # Parcourir la balise CODE
            s = io.StringIO(str(mycode))
            for line in s:                
                if(re.match('e;.*;\'' + f + '\';.*;.*', line)):
                    a1 = line.split(';')[1]
                if(re.match('e;.*;\'' + str(type_map[k]) + '\';.*;.*', line)):
                    a2 = line.split(';')[1]
                if(re.match('r;.*;' + a1 + ';' + a2 + ';4;.*', line)):
                    if(int(line.split(';')[5]) > 0):
                        words_list4.update(generate_dict(f, k))
                        break
        else:
            url = "http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + str(testWord) + "&rel=" + str(relation_map[k])

            # Reponse de la requete
            response = requests.get(url)

            # bs4
            soup = BeautifulSoup(response.text, features = 'lxml')

            # Chercher la balise CODE
            mycode = soup.find('code')

            # Parcourir la balise CODE
            s = io.StringIO(str(mycode))
            for line in s:
                if(re.match('e;.*;\'' + testWord + '\';.*;.*', line)):
                    a1 = line.split(';')[1]
                if(re.match('e;.*;\'' + f + '\';.*;.*', line)):
                    a2 = line.split(';')[1]
                if(re.match('r;.*;' + a1 + ';' + a2 + ';' + relation_map[k] + ';.*', line)):
                    if(int(line.split(';')[5]) > 0):
                        words_list4.update(generate_dict(f, k))
                        break

# Affichage des mots
print('\tLes mots finaux sont :')
print_results(words_list4)