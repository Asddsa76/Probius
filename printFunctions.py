from aliases import *
import asyncio
import re
from discordIDs import *

allHeroes={
	'bruiser':['Artanis', 'Chen', 'D.Va', 'Deathwing', 'Dehaka', 'Gazlowe', 'Hogger','Imperius', 'Leoric', 'Malthael', 'Ragnaros', 'Rexxar', 'Sonya', 'Thrall', 'Varian', 'Xul', 'Yrel'],
	'healer':['Alexstrasza', 'Ana', 'Anduin', 'Auriel', 'Brightwing', 'Deckard', 'Kharazim', 'Li_Li', 'Lt._Morales', 'Lúcio', 'Malfurion', 'Rehgar', 'Stukov', 'Tyrande', 'Uther', 'Whitemane'],
	'mage':['Azmodan', 'Chromie', 'Gall', "Gul'dan", 'Jaina', "Kael'thas", "Kel'Thuzad", 'Li-Ming', 'Mephisto', 'Nazeebo', 'Orphea', 'Probius', 'Tassadar'],
	'marksman':['Cassia', 'Falstad', 'Fenix', 'Genji', 'Greymane', 'Hanzo', 'Junkrat', 'Lunara', 'Nova', 'Raynor', 'Sgt._Hammer', 'Sylvanas', 'Tracer', 'Tychus', 'Valla', 'Zagara',"Zul'jin"],
	'melee':['Alarak', 'Illidan', 'Kerrigan', 'Maiev', 'Murky', 'Qhira', 'Samuro', 'The_Butcher', 'Valeera', 'Zeratul'],
	'support':['Abathur', 'Medivh', 'The_Lost_Vikings', 'Zarya'],
	'tank':["Anub'arak", 'Arthas', 'Blaze', 'Cho', 'Diablo', 'E.T.C.', 'Garrosh', 'Johanna', "Mal'Ganis", 'Mei', 'Muradin', 'Stitches', 'Tyrael']
}

def getHeroes():#Returns an alphabetically sorted list of all allHeroes.
	return sorted([j for i in allHeroes.values() for j in i])

async def getRoleHeroes(role):
	if role=='ranged':
		return allHeroes['mage']+allHeroes['marksman']
	elif role=='assassin':
		return (await getRoleHeroes('ranged'))+allHeroes['melee']
	else:
		return allHeroes[role]

async def heroes(message,text,channel,client):
	#['hero', 'heroes', 'bruiser', 'healer', 'support', 'ranged', 'melee', 'assassin', 'mage', 'marksman', 'tank']
	role=text[0].replace('marksmen','marksman')
	if role[-1]=='s':role=role[:-1]
	if len(text)==1:
		if role in ['hero', 'heroe']:
			await channel.send('\n'.join(['**'+i.capitalize()+':** '+', '.join(allHeroes[i]).replace('_',' ') for i in allHeroes]))
		elif role=='assassin':
			await channel.send('\n'.join(['**'+i.capitalize()+':** '+', '.join(allHeroes[i]).replace('_',' ') for i in ['mage', 'marksman', 'melee']]))
		elif role=='ranged':
			await channel.send('\n'.join(['**'+i.capitalize()+':** '+', '.join(allHeroes[i]).replace('_',' ') for i in ['mage', 'marksman']]))
		else:
			await channel.send('**'+role.capitalize()+':** '+', '.join(allHeroes[role]).replace('_',' '))
	else:
		if role in ['hero', 'heroe']:
			await printAll(client,message,text[1])
		else:
			await printAll(client,message,text[1], 1, await getRoleHeroes(role))
def printTier(talents,tier):#Print a talent tier
	output=''
	for i in talents[tier]:
		output+=i+'\n'
	return output

def printAbility(abilities,hotkey):#Prints abilities with matching hotkey
	output=''
	for ability in abilities:
		if '**['+hotkey.upper()+']' in ability:
			output+=ability+'\n'
	return output

def deepAndShallowSearchFoundBool(ability,string,deep):#Python3.5 doesn't allow async functions inside list comprehension :(
	if not deep:
		ability=ability.split(':**')[0]
	return 1 if string in ability.lower() else 0

async def printBuild(client,channel,text):
	build,hero=text.split(',')#Example: T0230303,DVa
	hero=aliases(hero)
	(abilities,talents)=client.heroPages[hero]
	build=build.replace('q','1').replace('w','2').replace('e','3').replace('r','4').replace('t','5')
	output=[]
	for j,i in enumerate(build[1:]):
		if i=='0':continue
		output.append(talents[j][int(i)-1])
	await printLarge(channel,'\n'.join(output))

async def addUnderscoresAndNewline(namelist,ability):
	indices=[]
	for i in namelist:
		#ability=ability.replace(i,'__'+i+'__').replace(i.capitalize(),'__'+i.capitalize()+'__').replace(i.title(),'__'+i.title()+'__')
		indicesA=[m.start() for m in re.finditer(i,ability.lower())]
		indices+=[j+len(i) for j in indicesA]+indicesA
	indices.sort(key=lambda x:-x)#Sort in descending order
	for i in indices:
		ability=ability[:i]+'__'+ability[i:]
	return ability+'\n'

async def printSearch(abilities, talents, name, hero, deep=False):#Prints abilities and talents with the name of the identifier
	name=abilityAliases(hero,name)
	if not name:
		return
	if '--' in name:
		[name,exclude]=name.split('--')
	else:
		exclude='this string is not in any abilities or talents'
	namelist=name.split('&')
	output=''
	for ability in abilities:
		if sum([1 for i in namelist if deepAndShallowSearchFoundBool(ability,i,deep)])==len(namelist) and exclude not in ability.lower():
			output+=await addUnderscoresAndNewline(namelist,ability)
	levelTiers=[0,1,2,3,4,5,6]
	if hero=='Varian':
		del levelTiers[1]
	elif hero in ['Tracer','Deathwing']:
		pass
	else:
		del levelTiers[3]
	for i in levelTiers:
		talentTier=talents[i]
		for talent in talentTier:
			if sum([1 for i in namelist if deepAndShallowSearchFoundBool(talent,i,deep)])==len(namelist) and exclude not in talent.lower():
				output+=await addUnderscoresAndNewline(namelist,talent)
	return output

async def printLarge(channel,inputstring,separator='\n'):#Get long string. Print lines out in 2000 character chunks
	strings=[i+separator for i in inputstring.split(separator)]
	output=strings.pop(0)
	i=0
	while strings:
		if i==4:#Don't make a long call in #probius hog all the bandwidth
			i=0
			await asyncio.sleep(5)
		if len(output)+len(strings[0])<2000:
			output+=strings.pop(0)
		else:
			i+=1
			await channel.send(output)
			output=strings.pop(0)
	await channel.send(output)

async def printAll(client,message,keyword, deep=False, heroList=getHeroes()):#When someone calls [all/keyword]
	'''if len(keyword)<4 and message.author.id!=DiscordUserIDs['Asddsa']:
		await message.channel.send('Please use a keyword with at least 4 letters minimum')
		return'''
	toPrint=''
	for hero in heroList:
		(abilities,talents)=client.heroPages[hero]
		output=await printSearch(abilities,talents,keyword,hero,deep)
		if output=='':
			continue
		toPrint+='`'+hero.replace('_',' ')+':` '+output
	if toPrint=='':
		return
	botChannels={'Wind Striders':DiscordChannelIDs['Probius'],'De Schuifpui Schavuiten':687351660502057021}
	if len(toPrint)>2000 and message.channel.guild.name in botChannels:#If the results is over one message, it gets dumped in specified bot channel
		channel=message.channel.guild.get_channel(botChannels[message.channel.guild.name])
		introText=message.author.mention+", Here's all heroes' "+'"'+keyword+'":\n'
		toPrint=introText+toPrint
	else:
		channel=message.channel
	await printLarge(channel,toPrint)

if __name__ == '__main__':
	from heroPage import heroAbilitiesAndTalents

	output=[]
	for hero in getHeroes():
		[abilities,talents]=heroAbilitiesAndTalents(hero)
		abilities=extraD(abilities,hero)
		for ability in abilities:
			if 'Quest' in ability:
				output.append(ability.split(':** ')[0])
	for i in output:
		print(i)