import asyncio
import aiohttp
from rotation import *

redditors=['Asddsa76', 'Blackstar_9', 'Spazzo965', 'SomeoneNew666', 'joshguillen', 'SotheBee', 'AnemoneMeer', 'Pscythic', 'Elitesparkle', 'slapperoni', 
'secret3332', 'Carrygan_', 'Archlichofthestorm', 'Gnueless', 'ThatDoomedStudent', 'InfiniteEarth', 'SamiSha_', 'twinklesunnysun', 'Pelaberus', 'KillMeWithMemes', 
'ridleyfire','bran76765','MarvellousBee','Naturage','Derenash','Riokaii','D0ctorLogan','Demon_Ryu','hellobgs','Beg_For_Mercy','Russisch','Valamar1732','ArashiNoShad0w',
'Mochrie1713','lemindhawk','Goshin26','TiredZealot','MasterAblar','SHreddedWInd','MrWilbus']

discordnames={'Pscythic':'Soren Lily', 'SotheBee':'Sothe', 'slapperoni':'slap','secret3332':'SecretChaos','Archlichofthestorm':'Trolldaeron','ThatDoomedStudent':'Carbon','InfiniteEarth':'Flash',
'KillMeWithMemes':'Nick','ridleyfire':'HailFall','bran76765':'Parthuin','Demon_Ryu':'Messa','Russisch':'Ekata','ArashiNoShad0w':'LeviathaN','TiredZealot':'Jdelrio','lemindhawk':'MindHawk'}

keywords=['Genji','Samuro','Maiev', 'Dva']#Posts with these in title gets forwarded regardless of author

mindhawk_keywords=['Kerrigan','Cho ','Gall',"Cho'Gall",'Orphea','Li-Ming','Ragnaros', 'Li Ming', 'chogall']

total_keywords=keywords + mindhawk_keywords

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
				title=title.replace('&amp;','&').replace('\u2013','-').replace('\u0336','').replace('\u2019',"'")
				client.forwardedPosts.append([title,author,url])
		client.forwardedPosts=client.forwardedPosts[::-1]
		return output

async def redditForwarding(client):#Called every 60 seconds
	try:
		async with aiohttp.ClientSession() as session:
			page = await fetch(session, 'https://old.reddit.com/r/heroesofthestorm/new.api')
			posts=page.split('"clicked": false, "title": "')[1:]
			for post in posts:
				try:
					[title,author,url] = await getPostInfo(post)
				except:
					continue
				if author in redditors or sum(1 for i in total_keywords if i.lower() in title.lower()):
					if title not in client.seenTitles:#This post hasn't been processed before
						client.seenTitles.append(title)
						title=title.replace('&amp;','&').replace('\u2013','-').replace('\u0336','').replace('\u2019',"'")
						client.forwardedPosts.append([title,author,url])
						if 'genji' in title.lower():
							await client.get_channel(568058278165348362).send('**'+title+'** <@183240974347141120> <@247677408386351105> <@408114527947980802> '+url)#Normie heroes
						elif 'maiev' in title.lower():
							await client.get_channel(568058278165348362).send('**'+title+'** <@247677408386351105> '+url)#Normie heroes
						elif any(x.lower() in title.lower() for x in mindhawk_keywords):
							await client.get_channel(568058278165348362).send('**'+title+'** <@129702871837966336> '+url)#Normie heroes
						elif 'dva' in title.lower().replace('.',''):
							await client.get_channel(568058278165348362).send('**'+title+'** <@84805890837864448> '+url)#Normie heroes
						elif 'Free-to-Play Hero Rotation & Heroic Deals' in title:
							await client.get_channel(557366982471581718).send('**'+title+'** by '+author+': '+url)#general
						elif 'samuro' in title.lower():
							await client.get_channel(564528564196605973).send('**'+title+'** <@329447886465138689> '+url)#Samuro-general
						else:
							if author in discordnames:
								author=discordnames[author]
							await client.get_channel(665317972646166538).send('**'+title+'** by '+author+': '+url)#reddit-posts
							await client.get_channel(557366982471581718).send('**'+title+'** by '+author+': '+url)#general
						await client.get_channel(643231901452337192).send('`'+title+' by '+author+'`')#log
						print(title+' by '+author)
						if author=='Gnueless' and 'rotation' in title.lower():
							await rotation(client.get_channel(557366982471581718))
	except:
		await client.get_channel(643231901452337192).send('Something went wrong with subreddit forwarding')
		print('Something went wrong with subreddit forwarding')
