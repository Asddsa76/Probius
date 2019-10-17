from urllib.request import urlopen
from miscFunctions import getHeroes
from aliases import aliases

async def guide(hero,channel):
	hero=hero.lower().replace('_','-').replace('.','').replace("'","")
	with open('elitesparkleBuilds.txt','r') as f:
		for i in f:
			if hero in i:
				await channel.send('<'+i[:-1]+'>')#<> prevents thumbnails. [:-1] removes the \n at end of i
				return
	await channel.send('No hero "'+hero+'"')

def updateBuilds():
	page=[i.strip().decode('utf-8') for i in urlopen('https://elitesparkle.wixsite.com/hots-builds') if "var warmupData = {" in i.strip().decode('utf-8')][0]
	with open('elitesparkleBuilds.txt','w+') as f:
		for hero in getHeroes():
			hero=aliases(hero).lower().replace('_','-').replace('.','').replace("'","")
			heropage=page[page.index('builds\/'+hero):]
			code=heropage[heropage.index('-'):heropage.index('\/"')]
			output='https://psionic-storm.com/en/builds/'+hero+code+'\n'
			print(output)
			f.write(output)

if __name__=='__main__':
	updateBuilds()