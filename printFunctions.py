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

def printAbility(abilities,hotkey,hero):#Print a single ability
	hero=aliases(hero)
	output=''
	abilityIndex='dqwe'.index(hotkey)
	if hero.lower()=='Abathur':
		abilityIndex=[0,1,5,4][abilityIndex]
		output+=abilities[abilityIndex]+'\n'
		if abilityIndex==1:
			output+=abilities[2]+'\n'
		elif abilityIndex==5:
			output+=abilities[3]+'\n'
	elif hero.lower()=='Greymane':#Extra Q and E, but not extra W
		abilityIndex=[0,1,3,4][abilityIndex]
		output+=abilities[abilityIndex]+'\n'
		if hotkey!='d' and hotkey!='w':
			output+=abilities[abilityIndex+1]+'\n'
	elif hero.lower()=='Leoric':#Extra Q and W
		abilityIndex=[0,1,3,5][abilityIndex]
		output+=abilities[abilityIndex]+'\n'
		if hotkey in 'qw':
			output+=abilities[abilityIndex+1]+'\n'
	elif hero.lower()=='D.Va':#Mech and pilot mode, extra D
		abilityIndex=[0,2,3,4][abilityIndex]
		output+=abilities[abilityIndex]+'\n'
		if hotkey in 'de':
			output+=abilities[abilityIndex+1]+'\n'
	elif hero.lower() in ['Fenix','Chen']:#Extra W
		abilityIndex=[0,1,2,4][abilityIndex]
		output+=abilities[abilityIndex]+'\n'
		if hotkey=='w':
			output+=abilities[abilityIndex+1]+'\n'
	elif hero.lower() in ['Stitches','Lt._Morales','Uther']:#Extra Q
		abilityIndex=[0,1,3,4][abilityIndex]
		output+=abilities[abilityIndex]+'\n'
		if hotkey=='q':
			output+=abilities[abilityIndex+1]+'\n'
	elif hero.lower()=='Lunara':#Extra E
		abilityIndex=[0,1,2,3][abilityIndex]
		output+=abilities[abilityIndex]+'\n'
		if hotkey=='e':
			output+=abilities[abilityIndex+1]+'\n'
	elif hero.lower()=='Tychus':
		abilityIndex=[0,1,3,5][abilityIndex]
		output+=abilities[abilityIndex]+'\n'
	else:
		special=hero.lower() in ['Ragnaros','Alexstrasza','Valeera']#2 abilites per hotkey
		if special:
			abilityIndex=[0,1,3,5][abilityIndex]
		output+=abilities[abilityIndex]+'\n'
		if special and hotkey!='d':
			output+=abilities[abilityIndex+1]+'\n'
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