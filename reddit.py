import asyncio
import aiohttp
from rotation import *
from printFunctions import printLarge
from discordIDs import *

redditors=['Asddsa76', 'Blackstar_9', 'Spazzo965', 'SomeoneNew666', 'joshguillen', 'SotheBee', 'AnemoneMeer', 'Pscythic', 'Elitesparkle', 'slapperoni', 
'secret3332', 'Carrygan_', 'Archlichofthestorm', 'Gnueless', 'ThatDoomedStudent', 'InfiniteEarth', 'SamiSha_', 'twinklesunnysun', 'Pelaberus', 'KillMeWithMemes',
'MarvellousBee','Naturage','Derenash','Riokaii','Demon_Ryu','hellobgs','Beg_For_Mercy','Russisch','Valamar1732','ArashiNoShad0w','lemindhawk','Goshin26',
'TiredZealot','MasterAblar','SHreddedWInd','MrWilbus','NotBelial','Dark_Polaroid','Mochrie1713','HeroesProfile','nexusschoolhouse','Nightterror0','starcaller_hots',
'WorstMedivhKR']

discordnames={'Pscythic':'Soren Lily', 'SotheBee':'Sothe', 'slapperoni':'slap','secret3332':'SecretChaos','Archlichofthestorm':'Trolldaeron','ThatDoomedStudent':'Carbon','InfiniteEarth':'Flash',
'KillMeWithMemes':'Nick','Demon_Ryu':'Messa','Russisch':'Ekata','ArashiNoShad0w':'LeviathaN','TiredZealot':'Jdelrio','lemindhawk':'MindHawk','Nightterror0':'Deafwing', 'Dark_Polaroid':'Medicake'}

#Posts with these in title gets forwarded regardless of author
keywords={
'Genji':[DiscordUserIDs['SomeoneNew'],DiscordUserIDs['Weebatsu']],
'Samuro':[DiscordUserIDs['Blackstorm'],156616620905725952],
'Maiev':[DiscordUserIDs['SomeoneNew']], 
' Dva':[DiscordUserIDs['Spazzo']], 
'Hanzo':[DiscordUserIDs['Medicake']],
'Lucio':[DiscordUserIDs['Medicake']],
'Zera':[DiscordUserIDs['Derenash'],224975834346291210],
'Valeera':[DiscordUserIDs['MBee']],
'Orphea':[410481791204327424],
'Deathwing':[204893952908853248],
'Tracer':[160087810370568193]}

async def getPostInfo(post):
	title=post.split('", "')[0]
	title=title.replace('\u2019',"'")
	post=post.split('"author": "')[1]
	author=post.split('"')[0]
	post=post.split('"permalink": "')[1]
	urlID='/'.join(post.split('/')[:5])
	url='https://www.reddit.com'+shortUrl
	return [title,author,url]

async def fetch(session, url):
	async with session.get(url) as response:
		return await response.text()

async def titleTrim(title):#Don't remove spaces because of Cho
	a={'\u0f3c':'༼','\u3064':'つ','\u25d5':'◕','\u0f3d':'༽','_':'\_','\u2019':"'",'\u0336':'','\u2013':'-','&amp;':'&'}
	for i in a.keys():
		title=title.replace(i,a[i])
	return title

async def fillPreviousPostTitles(client):#Called on startup
	await client.wait_until_ready()
	async with aiohttp.ClientSession() as session:
		page = await fetch(session, 'https://old.reddit.com/r/heroesofthestorm/new.api?limit=100&sort=new')
		posts=page.replace('"is_gallery": true, ','').split('"clicked": false, "title": "')[1:]
		output=[]
		for post in posts:
			try:#Reddit's .api did some weird stuff recently
				[title,author,url] = await getPostInfo(post)#Newest post that has been checked
			except:
				continue
			output.append(title)
			client.seenPosts.append([title,author,url])
			if author in redditors or sum(1 for i in keywords if i.lower() in title.lower()) or 'Blizz_' in author:
				title=await titleTrim(title)
				client.forwardedPosts.append([title,author,url])
		client.forwardedPosts=client.forwardedPosts[::-1]
		return output

async def redditForwarding(client):#Called every 60 seconds
	async with aiohttp.ClientSession() as session:
		page = await fetch(session, 'https://old.reddit.com/r/heroesofthestorm/new.api')
		posts=page.split('"clicked": false, "title": "')[1:]
		for post in posts:
			[title,author,url] = await getPostInfo(post)
			if title not in client.seenTitles:#This post hasn't been processed before
				client.seenTitles.append(title)
				title=await titleTrim(title)
				url='\n'+url
				client.seenPosts.append([title,author,url])
				if author in redditors or sum(1 for i in keywords if i.lower() in title.lower()) or 'Blizz_' in author:
					print('{} by {}'.format(title,author))
					client.forwardedPosts.append([title,author,url])
					if author=='nexusschoolhouse':
						await client.get_channel(222817241249480704).send('**{}**: '.format(title)+url)
					if author=='Spazzo965' and ('CCL' in title or 'Undocumented' in title):
						await client.get_channel(222817241249480704).send('**{}**: '.format(title)+url)

					toPing=[]
					for i in keywords:
						if i.lower() in title.lower():
							toPing+=keywords[i]
					if toPing:
						toPing=' '.join(['<@'+str(i)+'>' for i in toPing])

					if author in redditors:
						if author in discordnames:
							author=discordnames[author]
						await client.get_channel(DiscordChannelIDs['LoggingChannel']).send('`{} by {}`'.format(title,author))#log
						await client.get_channel(DiscordChannelIDs['RedditPosts']).send('**{}** by {}: {}'.format(title,author,url))#reddit-posts
						if toPing:
							await client.get_channel(DiscordChannelIDs['General']).send('**{}** by {}: {}\n{}'.format(title,author,url,toPing))#general
						else:
							await client.get_channel(DiscordChannelIDs['General']).send('**{}** by {}: {}'.format(title,author,url))#general
						if author=='Gnueless' and 'rotation' in title.lower():
							await rotation(client.get_channel(DiscordChannelIDs['General']))
					else:
						await client.get_channel(DiscordChannelIDs['LoggingChannel']).send('`{} by {}`'.format(title,author))#log
						channel=[DiscordChannelIDs['NormieHeroes'],DiscordChannelIDs['Samuro']]['samuro' in title.lower()]#Normie-heroes or Samuro
						await client.get_channel(channel).send('**{}** {}{}'.format(title,toPing,url))

async def redditSearch(client,message,text):
	output=''
	for i in client.seenPosts:
		author=i[1]
		if author in discordnames:
			author=discordnames[author]
		if text.lower() in i[0].lower():
			output+='**{}** by {}: <{}>\n'.format(i[0], author, i[2])
	await printLarge(message.channel,output)

async def reddit(client,message,text):
	if len(text)==2:
		if not text[1].isnumeric():
			await redditSearch(client,message,text[1])
			return
		cutoff=-int(text[1])
	else:
		cutoff=0
	output='Recent Reddit posts:\n'
	for i in client.forwardedPosts[cutoff:]:
		author=i[1]
		if author in discordnames:
				author=discordnames[author]
		output+='**{}** by {}: <{}> \n'.format(i[0], author, i[2])
	await printLarge(message.channel,output)