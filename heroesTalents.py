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

async def additionalInfo(hero,name,description):
	addDict={#Adds text to the end of descriptions
	'cassia':{'War Traveler':'The bonus is not lost when stutterstepping.'},
	'valla':{'Strafe':'The duration of Hatred is paused when channeling, and reset to full when Strafe ends.'},
	'alexstrasza':{
		'Cleansing Flame':'Dragonqueen: Cleansing Flame is cast instantly, and its cooldown is reduced by 10s. The duration of Dragonqueen is paused, while basic abilities continue to cool down while in flight.',
		'Dragon Scales':'Getting Stunned, Rooted, or Silenced while Dragon Scales is active refreshes its duration to 2 seconds.',
		'Life-Binder':'Dragonqueen: The cast range of Life-Binder is increased from 6 to 9.'},
	'maiev':{'Spirit of Vengeance':'Reactivate to teleport to the spirit.'},
	'sylvanas':{'Haunting Wave':'Sylvanas is unstoppable while flying to the banshee.'},
	'lunara':{'Leaping Strike':'Lunara is unstoppable while leaping.'},
	'chen':{'Storm, Earth, Fire':'Using Storm, Earth, Fire removes most negative effects from Chen.'},
	'guldan':{'Life Tap':'Costs 222 (+4% per level) Health.'},
	'johanna':{"Heaven's Fury":'4 bolts per second per enemy, up to 2 enemies.'},
	'tyrande':{"Huntress' Fury":"Splashes do not trigger any of Tyrande's Basic Attack related effects."},
	'tracer':{'Ricochet':'Ricochet shots do not interact with Bullet Time or Focus Fire.'},
	'imperius':{'Impaling Light':'The damage bonus is per brand and stacks to 375%'},
	'malfurion':{'Moonfire':'The area itself stays revealed for 2 seconds.',
		'Celestial Alignment':'Also extends the reveal of located area to 5 seconds.'},
	'tassadar':{'Psychic Shock':'Psionic Storm deals 2 additional ticks of damage.',
		'Shock Ray':'0.375 second wind up before beam starts, additional 0.75 second channel while beam is moving. If the channel is interrupted, beam instantly disappears.'},
	'zarya':{'Energy':'The damage bonus is multiplicative.'},
	'orphea':{'Overflowing Chaos':'The damage bonus is multiplicative.'},
	'tychus':{'Focusing Diodes':'The damage bonus is multiplicative.'},
	'mephisto':{'Spite':'Also extends mana regeneration from the healing globe.'}
	}
	if hero in addDict:
		if name in addDict[hero]:
			description+=' ***'+addDict[hero][name]+'***'
	return description

async def fixTooltips(hero,name,description):
	fixDict={#Replaces text using strikethrough
	'tracer':{'Sleight of Hand':['20%','24.5%'],
		'Reload':['0.75','0.8125']},
	'cassia':{'War Traveler':['8%','4%','1 second','0.5 seconds']},
	'sylvanas':{'Haunting Wave':['teleport','fly']},
	'tyrande':{'Light of Elune':['damages an enemy','Auto Attacks an enemy, or deals spell damage to an enemy hero']},
	'malfurion':{"Nature's Balance":['area','radius']},
	'auriel':{"Swift Sweep":['50%','100%']}
	}
	if hero in fixDict:
		if name in fixDict[hero]:
			for i in range(len(fixDict[hero][name])//2):
				description=description.replace(fixDict[hero][name][2*i],'~~'+fixDict[hero][name][2*i]+'~~ '+'***'+fixDict[hero][name][2*i+1]+'***')
	return await additionalInfo(hero,name,description)

async def descriptionFortmatting(description):
	if 'Repeatable Quest' in description:
		description=description.replace('Repeatable Quest:','\n    **❢ Repeatable Quest:**')
	else:
		description=description.replace('Quest:','\n    **❢ Quest:**')
	description=description.replace('Reward:','\n    **? Reward:**')
	return description

async def fetch(session, url):
	async with session.get(url) as response:
		return await response.text()

async def downloadHero(hero,client,patch):
	async with aiohttp.ClientSession() as session:
		if patch=='':
			page = await fetch(session, 'https://raw.githubusercontent.com/heroespatchnotes/heroes-talents/master/hero/'+hero+'.json')
		else:
			page = await fetch(session, 'https://raw.githubusercontent.com/MGatner/heroes-talents/'+patch+'/hero/'+hero+'.json')
		#client.heroPages={...'genji':[abilities,talents], ...}
		page=loads(page)
		abilities=[]
		if hero in ['ltmorales', 'valeera', 'deathwing', 'zarya']:
			resource='energy'
		elif hero=='chen':
			resource='brew'
		elif hero=='sonya':
			resource='fury'
		else:
			resource='mana'

		for i in page['abilities'].keys():
			for ability in page['abilities'][i]:
				if 'hotkey' in ability:
					output='**['+ability['hotkey']+'] '
				else:
					output='**[D] '
				output+=ability['name']+':** '
				if 'cooldown' in ability or 'manaCost' in ability:
					output+='*'
					if 'cooldown' in ability:
						output+=str(ability['cooldown'])+' seconds'
						if 'manaCost' in ability:
							output+=', '
					if 'manaCost' in ability:
						output+=str(ability['manaCost'])+' '+resource
					output+=';* '
				output+=await descriptionFortmatting(ability['description'])
				output=await fixTooltips(hero,ability['name'],output)
				abilities.append(output)
		if hero=='samuro':
			abilities.append("**[D] Image Transmission:** *14 seconds;* Activate to switch places with a target Mirror Image, removing most negative effects from Samuro and the Mirror Image.\n**Advancing Strikes:** Basic Attacks against enemy Heroes increase Samuro's Movement Speed by 25% for 2 seconds.")

		talents=[]
		keys=sorted(list(page['talents'].keys()),key=lambda x:int(x))
		for key in keys:
			tier=page['talents'][key]
			talentTier=[]
			for talent in tier:
				output='**['+str(int(key)-2*int(hero=='chromie' and key!='1'))+'] '
				output+=talent['name']+':** '
				if 'cooldown' in talent:
					output+='*'+str(talent['cooldown'])+' seconds;* '
				output+=await descriptionFortmatting(talent['description'])
				output=await fixTooltips(hero,talent['name'],output)
				talentTier.append(output)
			talents.append(talentTier)
		client.heroPages[aliases(hero)]=(abilities,talents)

async def loopFunction(client,heroes,patch):
	for future in asyncio.as_completed(map(downloadHero, heroes,repeat(client),repeat(patch))):
		await future

async def downloadAll(client,argv):
	if len(argv)==2:
		patch=argv[1]
	else:
		patch=''
	heroes=getHeroes()
	heroes=list(map(trimForHeroesTalents,heroes))
	loop = asyncio.get_event_loop()#running instead of event when calling from a coroutine. But running is for python3.7+
	loop.run_until_complete(loopFunction(client,heroes,patch))

async def heroStats(hero,channel,allowRecursion=True):
	if hero=='The_Lost_Vikings':
		for i in ['Olaf','Baleog','Erik']:
			await heroStats(i,channel)
	elif hero=='Rexxar' and allowRecursion:
		for i in ['Rexxar','Misha']:
			await heroStats(i,channel,False)# :spaghetti:
	elif hero=='Gall':
		await heroStats('Cho',channel)
	else:
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
			await channel.send('``'+hero+':`` '+', '.join(output))