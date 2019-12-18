import asyncio
import aiohttp
from rotation import *

redditors=['Asddsa76', 'Blackstar_9', 'Spazzo965', 'SomeoneNew666', 'joshguillen', 'SotheBee', 'AnemoneMeer', 'jdelrioc', 'Pscythic', 'Elitesparkle', 'slapperoni', 
'secret3332', 'Carrygan_', 'Archlichofthestorm', 'Gnueless', 'ThatDoomedStudent', 'InfiniteEarth', 'SamiSha_', 'twinklesunnysun', 'zanehyde', 'Pelaberus', 'KillMeWithMemes', 
'ridleyfire','bran76765','MarvellousBee','Naturage','Derenash','Riokaii','D0ctorLogan','Demon_Ryu','hellobgs','Beg_For_Mercy','Russisch']

discordnames={'Pscythic':'Soren Ily', 'SotheBee':'Sothe', 'slapperoni':'slap','secret3332':'SecretChaos','Archlichofthestorm':'Trolldareon','ThatDoomedStudent':'Carbon','InfiniteEarth':'Flash',
'KillMeWithMemes':'Nick','ridleyfire':'HailFall','bran76765':'Parthuin','Demon_Ryu':'Messa','Russisch':'Ekata'}

keywords=['genji','samuro']#Posts with these in title gets forwarded regardless of author

async def getPostInfo(post):
	title=post.split('", "')[0]
	post=post.split('"author": "')[1]
	author=post.split('"')[0]
	post=post.split('"permalink": "')[1]
	shortUrl=post.split('"')[0]
	url='https://old.reddit.com'+shortUrl
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
			[title,author,url] = await getPostInfo(post)#Newest post that has been checked
			output.append(title)
			if author in redditors or sum(1 for i in keywords if i in title.lower()):
				title=title.replace('&amp;','&').replace('\u2013','-').replace('\u0336','')
				client.forwardedPosts.append([title,author,url])
		client.forwardedPosts=client.forwardedPosts[::-1]
		return output

async def redditForwarding(client):#Called every 60 seconds
	try:
		async with aiohttp.ClientSession() as session:
			page = await fetch(session, 'https://old.reddit.com/r/heroesofthestorm/new.api')
			posts=page.split('"clicked": false, "title": "')[1:]
			for post in posts:
				[title,author,url] = await getPostInfo(post)
				if author in redditors or sum(1 for i in keywords if i in title.lower()):
					if title not in client.seenTitles:#This post hasn't been processed before
						client.seenTitles.append(title)
						title=title.replace('&amp;','&').replace('\u2013','-').replace('\u0336','')
						client.forwardedPosts.append([title,author,url])
						if 'genji' in title.lower():
							await client.get_channel(568058278165348362).send('**'+title+'** <@183240974347141120> <@247677408386351105> <@408114527947980802> '+url)#Normie heroes
						elif 'samuro' in title.lower():
							await client.get_channel(564528564196605973).send('**'+title+'** <@329447886465138689> '+url)#Samuro-general
						else:
							if author in discordnames:
								author=discordnames[author]
							await client.get_channel(557366982471581718).send('**'+title+'** by '+author+': '+url)#General
						await client.get_channel(643231901452337192).send('`'+title+' by '+author+'`')#log
						print(title+' by '+author)
						if author=='Gnueless':
							await rotation(client.get_channel(557366982471581718))
	except:
		await client.get_channel(643231901452337192).send('Something went wrong with subreddit forwarding')
		print('Something went wrong with subreddit forwarding')