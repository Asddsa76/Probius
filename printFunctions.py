from aliases import *
from miscFunctions import *

def printAbilities(abilities):#No identifier, print all abilities
	if len(abilities)<8:
		output=''
		for i in abilities:
			output+=i+'\n'
		return output
	else:
		output1=''
		output2=''
		for i in abilities[0:4]:
			output1+=i+'\n'
		for i in abilities[4:]:
			output2+=i+'\n'
		return[output1,output2]
		

def printTier(talents,tier):#Print a talent tier
	output=''
	for i in talents[tier]:
		output+=i+'\n'
	return output

def printAbility(abilities,hotkey):#Prints abilities with matching hotkey
	output=''
	for ability in abilities:
		if hotkey.upper() in ability[3:5]:
			output+=ability+'\n'
	return output

def printSearch(abilities, talents, name, hero):#Prints abilities and talents with the name of the identifier
	output=''
	for ability in abilities:
		if name.lower() in ability.lower():
			output+=ability+'\n'
	levelTiers=[0,1,2,3,4,5,6]
	if hero=='varian':
		del levelTiers[1]
	else:
		del levelTiers[3]
	for i in levelTiers:
		talentTier=talents[i]
		for talent in talentTier:
			if name in talent.lower():
				output+='***'+str(i*3+1+int(i==6)-2*int(hero=='chromie' and i!=0))+':*** '+talent+'\n'
	return output

async def printAll(message,keyword):#When someone calls [all/keyword]
	if message.channel.guild.name == 'Wind Striders':
		channel=message.channel.guild.get_channel(571531013558239238)#Probius
		await channel.send(message.author.mention+", Here's all heroes' "+keyword+':')
	else:
		channel=message.channel
	if len(keyword)<4:
		await channel.send('Please use a keyword with at least 4 letters minimum')
		return
	from heroPage import heroAbilitiesAndTalents
	for hero in getHeroes():
		[abilities,talents]=heroAbilitiesAndTalents(hero)
		abilities=extraD(abilities,hero)
		output=printSearch(abilities,talents,keyword,hero)
		if output=='':
			continue
		await channel.send('**'+hero.replace('_',' ')+':** '+output)