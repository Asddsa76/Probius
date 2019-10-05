from urllib.request import urlopen
from trimBrackets import *#Trims < from text

def addHotkeys(hero,abilities):
	hotkeys=['D','Q','W','E','R','R']
	if hero=='Abathur':
		hotkeys=['D','Q','QQ','QW','QE','W','R','R']
	elif hero=='Greymane':
		hotkeys=['D','Q','Q','W','E','E','R','R']
	elif hero=='Tracer':#She only has one heroic ability
		hotkeys=['D','Q','W','E','R']
	elif hero in ['Ragnaros','Alexstrasza','Valeera']:
		hotkeys=['D','Q','DQ','W','DW','E','DE','R','R']
	i=0
	for hotkey in hotkeys:
		abilities[i]='***'+hotkey+':*** '+abilities[i]
		i+=1
	return abilities

def heroAbilitiesAndTalents(hero):
	page=''
	try:
		for i in [i.strip().decode('utf-8') for i in urlopen('https://heroesofthestorm.gamepedia.com/index.php?title=Data:'+hero)]:
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