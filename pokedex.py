from miscFunctions import *
from aliases import *

pokedexMessageIDs=[657059472950296576,657059477194932264]

async def fillPokedex(client):#Fills internal state with pokedex members
	pokedexChannel=client.get_channel(597140352411107328)
	output=''
	for i in pokedexMessageIDs:
		output+=(await pokedexChannel.fetch_message(i)).content+'\n'
	return output.replace(':','')

async def pokedex(client,channel,hero):
	pokedex=await fillPokedex(client)
	if hero=='Test':
		for hero in getHeroes():
			if hero.replace('_',' ') not in pokedex:
				print(hero.replace('_',' '))
		return
	if hero not in getHeroes():
		await channel.send('No hero "'+hero+'"')
		return
	
	hero=hero.replace('_',' ')
	mains=pokedex.split(hero)[1].split('\n')[0]
	if hero=='Samuro':
		names=[i.name for i in client.get_guild(535256944106012694).get_role(557550150109888513).members]
		message=await channel.send(hero+' discussion! Our mains are the **Illusion masters: '+', '.join(names)+'.** React to ping them.')
	elif mains:
		names=[client.get_user(int(i)).name for i in mains.replace('>','').replace(' ','').replace('!','').split('<@')[1:]]
		message=await channel.send(hero+' discussion! Our mains are **'+', '.join(names)+'.** React to ping them.')
	else:
		message=await channel.send(hero+" discussion! We don't have any mains for this hero, ping <@329447886465138689> if you know any. React to ping Balance team.")
	await message.add_reaction('\U0001f44d')

async def pingPokedex(client,message,member):
	vowels='AEIOU'
	if 'Balance team' in message.content:
		await message.channel.send(member.mention+' wants to start a'+'n'*(message.content[0] in vowels)+' '+message.content.split('We ')[0]+'<@&577935915448795137>')
	elif 'Samuro' in message.content:
		await message.channel.send(member.mention+' wants to start a Samuro discussion! <@&557550150109888513>')
	else:
		pokedex=await fillPokedex(client)
		hero=message.content.split(' discussion!')[0]
		mains=pokedex.split(hero)[1].split('\n')[0]
		await message.channel.send(member.mention+' wants to start a'+'n'*(message.content[0] in vowels)+' '+message.content.split('Our ')[0]+mains)
	await message.delete()

async def pokedexCreationTrim(text):
	return text.replace('<@!460270968879841291>','').replace('  ',' ')

async def updatePokedex(client,text,message):
	if 557521663894224912 not in [role.id for role in message.author.roles]:
		await message.channel.send('You need to be a mod to update the Pokedex!')
		return
	if len(text)!=2:
		await message.channel.send('Syntax is [updatepokedex/hero, ping].')
		return
	heroPing=text[1].split(',')
	if len(heroPing)!=2:
		await message.channel.send('Syntax is [updatepokedex/hero, ping].')
		return

	hero=aliases(heroPing[0])
	if hero not in getHeroes():
		await message.channel.send(hero+' is not a valid hero.')
		return
	user=heroPing[1].replace(' ','')
	if '<@' not in user:
		await message.channel.send('`'+user+'` is not a ping.')
		return
	channel=message.channel
	pokedexChannel=client.get_channel(597140352411107328)
	if hero[0]<'M' or hero=='The_Butcher':
		message=await pokedexChannel.fetch_message(pokedexMessageIDs[0])
	else:
		message=await pokedexChannel.fetch_message(pokedexMessageIDs[1])

	hero=hero.replace('_',' ')
	oldMessage=message.content
	before,after=oldMessage.split(hero)
	afterHeroes=after.split('\n')
	mains,after=afterHeroes[0],afterHeroes[1:]
	
	removal=0
	if user in mains:
		removal=1
		mains=mains.replace(' '+user,'')
	else:
		mains+=' '+user
	await message.edit(content=before+hero+mains+'\n'+'\n'.join(after))
	if removal:
		await channel.send(user+' has been removed from '+hero)
	else:
		await channel.send(user+' has been added to '+hero)

async def removePokedex(client,MemberID): #Removes an user from all pokedex heroes
	pokedexChannel=client.get_channel(597140352411107328)
	for messageID in pokedexMessageIDs:
		message=await pokedexChannel.fetch_message(messageID)
		MemberID=str(MemberID)
		await message.edit(content=message.content.replace(' <@'+MemberID+'>','').replace(' <@!'+MemberID+'>',''))