from miscFunctions import *
from urllib.request import urlopen
from aliases import *
from itertools import repeat
from json import loads
import asyncio
import aiohttp
import nest_asyncio
nest_asyncio.apply()

def trimForHeroesTalents(hero):
	hero=hero.replace('The','').lower()
	remove=".' -_"
	for i in remove:
		hero=hero.replace(i,'')
	hero=hero.replace('butcher','thebutcher').replace('ú','u').replace('cho','chogall')
	return hero

async def fetch(session, url):
	async with session.get(url) as response:
		return await response.text()

async def downloadHero(hero,client,patch):
	async with aiohttp.ClientSession() as session:
		#page = await fetch(session, 'https://raw.githubusercontent.com/heroespatchnotes/heroes-talents/master/hero/'+hero+'.json')
		page = await fetch(session, 'https://raw.githubusercontent.com/MGatner/heroes-talents/2.49.1.77662/hero/'+hero+'.json')
		#client.heroPages={...'genji':[abilities,talents], ...}
		#newTalent='**['+str(i*3+1+int(i==6)-2*int(hero=='Chromie' and i!=0))+']** '#Level
		#Quest: ❢
		page=loads(page)
		abilities=[]
		for i in page['abilities'].keys():
			for ability in page['abilities'][i]:
				if 'hotkey' in ability:
					output='**['+ability['hotkey']+'] '
				else:
					output='**[D] '
				output+=ability['name']+':** '
				if 'cooldown' in ability:
					output+='*'+str(ability['cooldown'])+' seconds;* '
				output+=ability['description']
				abilities.append(output)

		talents=[]
		for tier in page['talents']:
			talentTier=[]
			for talent in page['talents'][tier]:
				output=output='**['+str(tier)+'] '
				output+=talent['name']+':** '
				if 'cooldown' in talent:
					output+='*'+str(talent['cooldown'])+' seconds;* '
				output+=talent['description']
				talentTier.append(output)
			talents.append(talentTier)
		client.heroPages[aliases(hero)]=(abilities,talents)

async def loopFunction(client,heroes,patch):
	for future in asyncio.as_completed(map(downloadHero, heroes,repeat(client),repeat(patch))):
		await future

async def downloadAll(client,patch=''):
	heroes=getHeroes()
	heroes=list(map(trimForHeroesTalents,heroes))
	loop = asyncio.get_event_loop()#running instead of event when calling from a coroutine. But running is for python3.7+
	loop.run_until_complete(loopFunction(client,heroes,patch))

async def heroStats(hero,channel):
	async with aiohttp.ClientSession() as session:
		page = await fetch(session, 'https://heroesofthestorm.gamepedia.com/index.php?title=Data:'+hero)
		page=''.join([i for i in page])
		page=page.split('<td><code>skills</code>')[0]

		output=[]
		usefulStats=['date', 'health', 'resource', 'attack speed', 'attack range', 'attack damage', 'unit radius']
		for i in usefulStats:
			page=page.split('<td>'+i+'\n')[1]
			page=page[page.index('<td>')+4:]
			output.append('**'+i.replace('attack','aa').replace('unit ','').replace('health','hp').capitalize()+'**: '+str(page[:page.index('</td>')]).replace('\n',''))
		await channel.send(', '.join(output))