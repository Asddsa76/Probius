from codecs import open
from trimBrackets import *#Trims < from text

def addHotkeys(hero,abilities):
	
	if hero=='Abathur':
		hotkeys=['D','Q','QQ','QW','QE','W','R','R','Mount']
	elif hero=='Greymane':
		hotkeys=['D','Q','Q','W','E','E','R','R']
	elif hero=='Tracer':#She only has one heroic ability
		hotkeys=['D','Q','W','E','R']
	elif hero in ['Ragnaros','Alexstrasza','Valeera']:
		hotkeys=['D','Q','DQ','W','DW','E','DE','R','R']
	elif hero=='The_Lost_Vikings':
		hotkeys=['D','1','2','3','4','R','R','Mount']
	elif hero=='Gall':
		hotkeys=['D','Q','W','E','R','R','R','1','Mount']
	elif len(abilities)==7:
		if hero in ['Medivh','Rehgar','Sgt._Hammer','Probius','Lunara','Brightwing','Dehaka','Falstad','Lucio','D.Va']:#Mount
			hotkeys=['D','Q','W','E','R','R','Mount']
		elif hero in ['Zeratul']:#Wiki lists Vorpal last
			hotkeys=['D','Q','W','E','R','R','1']
		else:
			hotkeys=['D','1','Q','W','E','R','R']#Extra button
	else:
		hotkeys=['D','Q','W','E','R','R']#Normal hero
	i=0
	for hotkey in hotkeys:
		abilities[i]='***'+hotkey+':*** '+abilities[i]
		i+=1
	return abilities

def heroAbilitiesAndTalents(hero):
	page=''
	try:
		for i in open('HeroPages/'+hero+'.html', 'r', 'utf-8'):
			page+=i
	except:
		return [404,404]

	page=trim(page)
	abilityIndex=page.index('Skills')+8
	talentIndex=page.index('"Talents"')#Quote marks because Talents are mentioned in Alarak's sadism text
	abilityPage=page[abilityIndex:talentIndex]
	talentPage=page[talentIndex:]

	abilities=abilityPage.split('<span class="skill-name">')[1:]
	newAbilities=[]
	for ability in abilities:
		newAbility='**'
		newAbility+=ability[0:ability.index('<')]+':** '#Name
		try:
			ability=ability.split('"skill-cooldown">')[1]
			newAbility+=ability[0:ability.index(' <')]#Cooldown. Some trais have no cooldown
		except:
			pass
		ability=ability.split('"skill-description">')[1]
		newAbility+=ability[0:ability.index('<')]+' '#Description
		newAbilities.append(newAbility)

	talentTiers=talentPage.split('"talent-tier-label">')[1:]
	newTalentTiers=[]
	for talentTier in talentTiers:
		newTalentTier=[]
		talents=talentTier.split('"talent-name">')[1:]
		for talent in talents:
			newTalent='**'+talent[0:talent.index('<')]+':** '#Name
			talent=talent.split('"talent-description">')[1]
			newTalent+=talent[0:talent.index('<')]+' '#Description
			newTalentTier.append(newTalent)
		newTalentTiers.append(newTalentTier)

	abilities=addHotkeys(hero,newAbilities)
	talents=newTalentTiers
	return [abilities,talents]