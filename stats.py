from urllib.request import urlopen
from math import ceil

patch='2.48'
gamemode='qm'
timeFrameType='major'
def shortenName(hero):#Shorten all names with 9+ letters
	if hero=='The Lost Vikings':
		return 'TLV'
	elif hero=='The Butcher':
		return 'Butcher'
	elif hero=='Sgt. Hammer':
		return 'Hammer'
	elif hero=='Lt. Morales':
		return 'Morales'
	elif hero=='Alexstrasza':
		return 'Alex'
	elif hero=='Brightwing':
		return 'BW'
	elif hero=="Kel'thuzad":
		return 'KTZ'
	elif hero=='Malfurion':
		return 'Malf'
	elif hero=='Whitemane':
		return 'WM'
	elif hero=='KelThuzad':
		return 'KTZ'
	else:
		return hero

class Hero(object):
	def __init__(self,heroInfo,gamemode):
		#Name, winrate, popularity, banrate, games played
		self.gamemode=gamemode
		[self.name,heroInfo]=heroInfo.split('win_rate')
		[self.wr,heroInfo]=heroInfo.split('popularity')
		if gamemode=='qm':
			[self.pop,self.games]=heroInfo.split('games_played')
		else:
			[self.pop,heroInfo]=heroInfo.split('ban_rate')
			[self.br,self.games]=heroInfo.split('games_played')
			self.brChange=0
		self.ci=str(round(1.96*(float(self.wr)*(100-float(self.wr))/int(self.games))**0.5,2))
		self.name=shortenName(self.name)
	def heroString(self):
		if len(self.pop)==3:
			self.pop+='0'
		if len(self.ci)==3:
			self.ci+='0'
		if self.gamemode=='qm':
			return(self.name+' '*(10-len(self.name))+self.wr+'  ±'+self.ci+'  '+self.pop)
		else:
			return(self.name+' '*(12-len(self.name))+self.wr+' ±'+self.ci+' '*(4-len(self.br))+self.br+' '*(7-len(self.pop))+self.pop+' '*(9-len(self.games))+self.games)

async def printCode(strings,channel):
	output=strings.pop(0)+'\n```'
	while strings:
		if len(output)+len(strings[0])<1997:
			output+=strings.pop(0)+'\n'
		else:
			await channel.send(output[:-1]+'```')
			output='```'+strings.pop(0)+'\n'
	await channel.send(output[:-1]+'```')

async def printHeroes(heroes,gamemode,totalGames,channel):
	output=['Score results QM patch 2.48, '+str(totalGames)+' games total']
	if gamemode=='qm':
		output.append('Hero      Win%   95%CI  Pop% |Hero      Win%   95%CI  Pop% |Hero      Win%   95%CI  Pop% ')
		output.append('-----------------------------+-----------------------------+-----------------------------')
	else:
		output.append('Hero          Winrate    95%CI   Ban%     Pop%   Games | Hero          Winrate    95%CI   Ban%     Pop%   Games')
		output.append('                                                       |                                                       ')
	m=ceil(len(heroes)/3)
	for i in range(m):
		try:
			output.append(heroes[i].heroString()+' |'+heroes[i+m].heroString()+' |'+heroes[i+2*m].heroString())
		except:
			pass
	if len(heroes)%3==1:
		output.append(heroes[2*m-1].heroString()+' |')
	elif len(heroes)%3==2:
		output.append(heroes[m-1].heroString()+' |'+heroes[2*m-1].heroString())
	await printCode(output,channel)

def getData(patch,gamemode):
	heroes=[]
	record=0#When to start or stop recording text into page
	for i in [i.strip().decode('utf-8') for i in urlopen('https://www.heroesprofile.com/Global/Hero/?timeframe_type='+timeFrameType+'&timeframe='+patch+'&type=win_rate&role=&hero=&game_type='+gamemode)]:
		if '<a alt=' in i:
			record=1
		elif '</table>' in i:
			record=0
		if record and i not in ['','</div','</div>','<div class="popup-trigger">','<div class="hero-picture ">'] and '<a alt=' not in i and '<img alt=' not in i:
			heroInfo=i[i.index('>')+1:i.index("</td><td class='wins")]
			for j in ['</td>','td class=','</a>','</div>','_cell',',','<','>',"'",'hide-column ban_rate']:
				heroInfo=heroInfo.replace(j,'')
			heroes.append(Hero(heroInfo,gamemode))
	totalGames=sum([int(hero.games) for hero in heroes])
	for hero in heroes:
		hero.pop=str(round(100*int(hero.games)/totalGames,2))#Sum from heroesProfile is 984, 10 times larger?
	return [heroes,totalGames]

async def stats(channel):
	[heroes,totalGames]=getData(patch,gamemode)
	await printHeroes(heroes,gamemode,totalGames,channel)