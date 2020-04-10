from aliases import *
from miscFunctions import *

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
		ability=ability.split(':')[0]
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
	for i in namelist:
		ability=ability.replace(i,'__'+i+'__').replace(i.capitalize(),'__'+i.capitalize()+'__').replace(i.title(),'__'+i.title()+'__')
	return ability+'\n'

async def printSearch(abilities, talents, name, hero, deep=False):#Prints abilities and talents with the name of the identifier
	name=abilityAliases(hero,name)
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
	while strings:
		if len(output)+len(strings[0])<2000:
			output+=strings.pop(0)
		else:
			await channel.send(output)
			output=strings.pop(0)
	await channel.send(output)

async def printAll(client,message,keyword, deep=False):#When someone calls [all/keyword]
	async with message.channel.typing():
		if len(keyword)<4 and message.author.id!=183240974347141120:
			await message.channel.send('Please use a keyword with at least 4 letters minimum')
			return
		toPrint=''
		for hero in getHeroes():
			(abilities,talents)=client.heroPages[hero]
			output=await printSearch(abilities,talents,keyword,hero,deep)
			if output=='':
				continue
			toPrint+='`'+hero.replace('_',' ')+':` '+output
		if toPrint=='':
			return
		botChannels={'Wind Striders':571531013558239238,'The Hydeout':638160998305497089,'De Schuifpui Schavuiten':687351660502057021}
		if toPrint.count('\n')>5 and message.channel.guild.name in botChannels:#If the results is more lines than this, it gets dumped in specified bot channel
			channel=message.channel.guild.get_channel(botChannels[message.channel.guild.name])
			introText=message.author.mention+", Here's all heroes' "+'"'+keyword+'":\n'
			toPrint=introText+toPrint
		else:
			channel=message.channel
	await printLarge(channel,toPrint)

if __name__ == '__main__':
	from miscFunctions import *
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