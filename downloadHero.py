from urllib.request import urlopen
from aliases import aliases
from miscFunctions import getHeroes
from sys import argv
from trimBrackets import *#Trims < from text

hero=argv[1]
if hero=='all':
	heroes=getHeroes()
else:
	heroes=[aliases(hero)]

for hero in heroes:
	print(hero)
	page=''.join([i.strip().decode('utf-8') for i in urlopen('https://heroesofthestorm.gamepedia.com/index.php?title=Data:'+hero)])
	page=trim(page)
	abilityIndex=page.index('Skills')+8
	endIndex=page.index('NewPP')
	try:
		endIndex=page.index('Scaling at key levels')
	except:
		pass
	page=page[abilityIndex:endIndex]

	f=open('HeroPages/'+hero+'.html','w+')
	f.write(page)
	f.close()