from aliases import *

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