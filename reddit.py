import asyncio
import aiohttp
from rotation import *

redditors=['Asddsa76', 'Blackstar_9', 'Spazzo965', 'SomeoneNew666', 'joshguillen', 'SotheBee', 'AnemoneMeer', 'Pscythic', 'Elitesparkle', 'slapperoni', 
'secret3332', 'Carrygan_', 'Archlichofthestorm', 'Gnueless', 'ThatDoomedStudent', 'InfiniteEarth', 'SamiSha_', 'twinklesunnysun', 'Pelaberus', 'KillMeWithMemes', 
'bran76765','MarvellousBee','Naturage','Derenash','Riokaii','Demon_Ryu','hellobgs','Beg_For_Mercy','Russisch','Valamar1732','ArashiNoShad0w',
'lemindhawk','Goshin26','TiredZealot','MasterAblar','SHreddedWInd','MrWilbus','NotBelial','Dark_Polaroid','Mochrie1713']

discordnames={'Pscythic':'Soren Lily', 'SotheBee':'Sothe', 'slapperoni':'slap','secret3332':'SecretChaos','Archlichofthestorm':'Trolldaeron','ThatDoomedStudent':'Carbon','InfiniteEarth':'Flash',
'KillMeWithMemes':'Nick','bran76765':'Parthuin','Demon_Ryu':'Messa','Russisch':'Ekata','ArashiNoShad0w':'LeviathaN','TiredZealot':'Jdelrio','lemindhawk':'MindHawk',
'Dark_Polaroid':'Medicake'}

#Posts with these in title gets forwarded regardless of author
keywords={
'Genji':[183240974347141120,247677408386351105,408114527947980802],
'Samuro':[329447886465138689],
'Maiev':[247677408386351105], 
' Dva:':[84805890837864448], 
'Hanzo':[160743140901388288],
'Lucio':[160743140901388288],
'Zeratul':[191410663292272640],
'Valeera':[364041091693150208]}

mindhawk_keywords=['Kerrigan','Cho ','Gall',"Cho'Gall",'Orphea','Li-Ming','Ragnaros', 'Li Ming', 'chogall']
for i in mindhawk_keywords:
	if i in keywords:
		keywords[i].append(129702871837966336)
	else:
		keywords[i]=[129702871837966336]

async def getPostInfo(post):
	title=post.split('", "')[0]
	title=title.replace('\u2019',"'")
	post=post.split('"author": "')[1]
	author=post.split('"')[0]
	post=post.split('"permalink": "')[1]
	shortUrl=post.split('"')[0]
	url='https://www.reddit.com'+shortUrl
	return [title,author,url]

async def fetch(session, url):
	async with session.get(url) as response:
		return await response.text()

async def titleTrim(title):#Don't remove spaces because of Cho
	return title.replace('&amp;','&').replace('\u2013','-').replace('\u0336','').replace('\u2019',"'")

async def fillPreviousPostTitles(client):#Called on startup
	await client.wait_until_ready()
	async with aiohttp.ClientSession() as session:
		page = await fetch(session, 'https://old.reddit.com/r/heroesofthestorm/new.api?limit=100&sort=new')
		posts=page.split('"clicked": false, "title": "')[1:]
		output=[]
		for post in posts:
			try:#Reddit's .api did some weird stuff recently
				[title,author,url] = await getPostInfo(post)#Newest post that has been checked
			except:
				continue
			output.append(title)
			if author in redditors or sum(1 for i in keywords if i.lower() in title.lower()):
				title=await titleTrim(title)
				client.forwardedPosts.append([title,author,url])
		client.forwardedPosts=client.forwardedPosts[::-1]
		return output

async def redditForwarding(client):#Called every 60 seconds
	async with aiohttp.ClientSession() as session:
		page = await fetch(session, 'https://old.reddit.com/r/heroesofthestorm/new.api')
		posts=page.split('"clicked": false, "title": "')[1:]
		for post in posts:
			try:
				[title,author,url] = await getPostInfo(post)
			except:
				continue
			if author in redditors or sum(1 for i in keywords if i.lower() in title.lower()):
				if title not in client.seenTitles:#This post hasn't been processed before
					client.seenTitles.append(title)
					title=await titleTrim(title)
					client.forwardedPosts.append([title,author,url])
					url='\n'+url
					print(title+' by '+author)

					toPing=[]
					for i in keywords:
						if i.lower() in title.lower():
							toPing+=keywords[i]
					if toPing:
						toPing=' '.join(['<@'+str(i)+'>' for i in toPing])

					if author in redditors:
						if author in discordnames:
							author=discordnames[author]
						await client.get_channel(643231901452337192).send('`'+title+' by '+author+'`')#log
						await client.get_channel(665317972646166538).send('**'+title+'** by '+author+': '+url)#reddit-posts
						if toPing:
							await client.get_channel(557366982471581718).send('**'+title+'** by '+author+': '+url+'\n'+toPing)#general
						else:
							await client.get_channel(557366982471581718).send('**'+title+'** by '+author+': '+url)#general
						if author=='Gnueless' and 'rotation' in title.lower():
							await rotation(client.get_channel(557366982471581718))
					else:
						await client.get_channel(643231901452337192).send('`'+title+' by '+author+'`')#log
						channel=[568058278165348362,564528564196605973]['samuro' in title.lower()]#Normie-heroes or Samuro
						await client.get_channel(channel).send('**'+title+'** '+toPing+url)						