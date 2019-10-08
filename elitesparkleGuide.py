from urllib.request import urlopen

async def guide(hero,channel):
	hero=hero.lower().replace('_','-').replace('.','').replace("'","")
	
	page=[i for i in urlopen('https://elitesparkle.wixsite.com/hots-builds')][6077].strip().decode('utf-8')
	page=page[page.index(hero):]
	page=page[page.index('builds'):page.index('}}')]
	code=page[page.index('-'):page.index('\/"')]

	await channel.send('https://psionic-storm.com/en/builds/'+hero+code)