from trimBrackets import *#Trims < from text
from miscFunctions import *
from urllib.request import urlopen
from aliases import *
from sys import argv
import asyncio
import aiohttp

def heroAbilitiesAndTalents(hero):
	try:
		page=open('HeroPages/'+hero.capitalize()+'.html','rb').read().decode('utf-8')
	except:
		return [404,404]

	page=page.replace('!','❢')
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
			cooldown=ability[0:ability.index(' <')]
			if cooldown[-1]==' ':
				cooldown=cooldown[:-1]
			cooldown+='; '
			newAbility+=cooldown#Cooldown. Some trais have no cooldown
		except:
			pass
		ability=ability.split('"skill-description">')[1]
		newAbility+=ability[0:ability.index('<')]+' '#Description
		newAbilities.append(newAbility)

	talentTiers=talentPage.split('"talent-tier-label">')[1:]
	newTalentTiers=[]
	for i in range(7):
		newTalentTier=[]
		talents=talentTiers[i].split('"talent-name">')[1:]
		for talent in talents:
			newTalent='**['+str(i*3+1+int(i==6)-2*int(hero=='Chromie' and i!=0))+']** '#Level
			newTalent+='**'+talent[0:talent.index('<')]+':** '#Name
			talent=talent.split('"talent-description">')[1]
			newTalent+=talent[0:talent.index('<')]+' '#Description
			newTalentTier.append(newTalent)
		newTalentTiers.append(newTalentTier)

	abilities=addHotkeys(hero,newAbilities)
	talents=newTalentTiers
	return [abilities,talents]

async def fetch(session, url):
	async with session.get(url) as response:
		return await response.text()

async def downloadHero(hero):
	print(hero)
	async with aiohttp.ClientSession() as session:
		page = await fetch(session, 'https://heroesofthestorm.gamepedia.com/index.php?title=Data:'+hero)
		page=''.join([i for i in page])
		page=trim(page)
		abilityIndex=page.index('Skills')+8
		endIndex=page.index('NewPP')
		try:
			endIndex=page.index('Scaling at key levels')
		except:
			pass
		page=page[abilityIndex:endIndex]

		with open('HeroPages/'+hero.capitalize()+'.html','w+b') as f:
			f.write(page.encode())

async def loopFunction(heroes):
	for future in asyncio.as_completed(map(downloadHero, heroes)):
		await future

if __name__=='__main__':
	hero=argv[1]
	if hero=='all':
		heroes=getHeroes()
	else:
		heroes=[aliases(hero)]

	loop = asyncio.get_event_loop()
	loop.run_until_complete(loopFunction(heroes))
	loop.close()