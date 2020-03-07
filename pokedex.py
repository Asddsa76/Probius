from miscFunctions import *
from aliases import *

async def fillPokedex(client):#Fills internal state with pokedex members
	pokedexChannel=client.get_channel(597140352411107328)
	output=''
	async for message in pokedexChannel.history(limit=50):
		output+=message.content+'\n'
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

	pokedex_channel=client.get_channel(597140352411107328)

	pokedex_messages=[]
	# We're unlikely to ever go above 50 messages in the pokedex.
	async for pokedex_message in pokedex_channel.history(limit=50):
		pokedex_messages.append(pokedex_message.content)

	pokedex_as_string = ''
	for pokedex_message in pokedex_messages:
		# Prepend the strings
		pokedex_as_string = pokedex_message + pokedex_as_string
	
	# Let's update the message before splitting it
	hero=hero.replace('_',' ')

	pokedex_as_individual_hero_strings=pokedex_as_string.split('\n')

	for hero_mains_string in pokedex_as_individual_hero_strings:
		if hero in hero_mains_string:
			removal=False
			if user in hero_mains_string:
				removal=True
				hero_mains_string=hero_mains_string.replace(' '+user,'')
			else:
				hero_mains_string+=' '+user

	pokedex_as_string_array=[]
	i = 0
	pokedex_as_string_array.append('')
	for hero_mains_string in pokedex_as_individual_hero_strings:
		if (len(pokedex_as_string_array[i] + hero_mains_string) < 2000):
			pokedex_as_string_array[i] += hero_mains_string + '\n'
		else:
			i += 1
			pokedex_as_string_array.append(hero_mains_string + '\n')
	
	i = 0
	async for pokedex_message in pokedex_channel.history(limit=50):
		await pokedex_message.edit(content=pokedex_as_string_array[i])
		i += 1

	# We've run out of messages, do we have content left?
	# We're never going to add two messages from 1 edit call, no need to worry about that.
	if len(pokedex_as_string_array)<1:
		message_to_edit = await pokedex_channel.send('This will be edited soon.')
		await message_to_edit.edit(content=pokedex_as_string_array[i])
	
	if removal:
		await message.channel.send(user+' has been removed from '+hero)
	else:
		await message.channel.send(user+' has been added to '+hero)

async def removePokedex(client,MemberID): #Removes an user from all pokedex heroes
	pokedexChannel=client.get_channel(597140352411107328)
	async for message in pokedexChannel.history(limit=50):
		MemberID=str(MemberID)
		await message.edit(content=message.content.replace(' <@'+MemberID+'>','').replace(' <@!'+MemberID+'>',''))