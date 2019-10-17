from trimBrackets import *#Trims < from text
from miscFunctions import *

def heroAbilitiesAndTalents(hero):
	try:
		page=open('HeroPages/'+hero.capitalize()+'.html','rb').read().decode('utf-8')
	except:
		return [404,404]

	page.replace('!','❢')
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