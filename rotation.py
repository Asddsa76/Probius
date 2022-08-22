from urllib.request import urlopen
from json import loads
from printFunctions import *

async def rotation(channel):
	async with channel.typing():
		with urlopen("https://nexuscompendium.com/api/currently/weekly") as url:
			data=loads(url.read().decode())

		rotationHeroes=[hero['Name'] for hero in data['RotationHero']['Heroes']]
		limitedHeroSkins=[]
		limitedMounts=[]
		goldMounts=[]
		saleKeys=data['Sale'].keys()
		if 'Heroes' in saleKeys:
			salesHeroes=[hero['Name'] for hero in data['Sale']['Heroes']]
			gemPrices=[str(hero['GemPrice']) for hero in data['Sale']['Heroes']]
		if 'Skins' in saleKeys:
			limitedHeroSkins=[skin['Name'] for skin in data['Sale']['Skins']]
		if 'SkinsLimited' in saleKeys:
			limitedHeroSkinsVariations=[skin['Name'] for skin in data['Sale']['SkinsLimited']]
		if 'MountsLimited' in saleKeys:
			limitedMounts=[mount['Name'] for mount in data['Sale']['MountsLimited']]
		if 'MountsGold' in saleKeys:
			goldMounts=[mount['Name'] for mount in data['Sale']['MountsGold']]
		skinsLimited=''
		mountsLimited=''
		boost360=''
		output='**Free rotation '+str(data['RotationHero']['StartDate'])+' to '+str(data['RotationHero']['EndDate']+':**\n')

		if rotationHeroes:
			output+=', '.join(rotationHeroes[:7])+'\n'
			output+=', '.join(rotationHeroes[7:])+'\n'
			await printLarge(channel,output,'\n')
			return#Maintenance mode
			output+='**Sales '+str(data['Sale']['StartDate'])+' to '+str(data['Sale']['EndDate']+':**\n')
			output+='**Sales:** '+', '.join([salesHeroes[i]+' '+gemPrices[i]+'<:nexusGem:697309829051449424>' for i in range(len(salesHeroes))])+'\n'
		if limitedHeroSkins:
			output+='**'+skinsLimited+'Hero Skins:** \n '+'\n '.join(limitedHeroSkins)+'\n'
		if limitedMounts:
			output+='**'+mountsLimited+'Mounts:** '
			output+=', '.join(limitedMounts)
		if goldMounts:
			output+='**Gold mounts:** '+', '.join(goldMounts)
		if boost360:
			output+='**Boosts:** 360 days'+boost360
	await printLarge(channel,output,'\n')#Get long string. Print lines out in 2000 character chunks

async def event(channel):
	async with channel.typing():
		with urlopen("https://nexuscompendium.com/api/currently/event") as url:
			data=loads(url.read().decode())['Event']
	endDate=data['EndDate'] or 'Unknown'
	await channel.send('**'+data['Name']+'**\nFrom '+data['StartDate']+' to '+endDate+'\n'+data['Description']+'\n'+data['URL'])