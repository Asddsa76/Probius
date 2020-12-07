from urllib.request import urlopen
from aliases import *
from printFunctions import getHeroes

def getQuote(hero):
	with open('quotes.txt','r') as f:
		for line in f:
			if hero.replace('ú','u') in line:
				return '**'+hero.replace('_',' ')+':** '+line[line.index('; ')+2:]
		return ''

def downloadQuotes():
	noQuoteOnPage=['Anduin','Imperius','Mephisto','Murky','Probius','Qhira','The_Butcher','Whitemane']
	theirQuote=['For the Alliance above all!','I yearn for battle.','*(Hisses)*','Mrrgll','*(Probe sounds)*',"I'm in.",'Fresh meat!','Let the inquisition commence!']
	with open('quotes.txt','w+') as f:
		for hero in getHeroes():
			hero=aliases(hero)
			print(hero)
			if hero in noQuoteOnPage:
				quote=theirQuote[noQuoteOnPage.index(hero)]
			else:
				page=''.join([i.strip().decode('utf-8') for i in urlopen('https://heroesofthestorm.gamepedia.com/'+hero)])
				page=page[page.index('<p><i>"')+7:]
				quote=page[:page.index('"')]
			output=hero+'; '+quote
			f.write(output+'\n')

if __name__=='__main__':
	downloadQuotes()