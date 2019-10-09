from urllib.request import urlretrieve
from aliases import aliases
from miscFunctions import getHeroes
from sys import argv

hero=argv[1]
if hero=='all':
	heroes=getHeroes()
else:
	heroes=[aliases(hero)]

for hero in heroes:
	print(hero)
	urlretrieve('https://heroesofthestorm.gamepedia.com/index.php?title=Data:'+hero,'HeroPages/'+hero+'.html')