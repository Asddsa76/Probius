from printFunctions import *
from aliases import *
from discordIDs import *

async def fillPokedex(client):#Fills internal state with pokedex members
	pokedexChannel=client.get_channel(DiscordChannelIDs['Pokedex'])
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
	if '@' in hero:#Find all heroes the user is listed in
		user=hero.replace(' ','').replace('!','').replace('@','@!')
		heroes=pokedex.split('\n')
		output=sorted([i.split(' <')[0] for i in heroes if user in i])
		if output:
			await channel.send(', '.join(output))
			return
		await channel.send('This user is not in the pokedex.')
		return
	if hero not in getHeroes():
		await channel.send('Invalid hero!')
		return
	
	hero=hero.replace('_',' ')
	mains=pokedex.split(hero)[1].split('\n')[0]
	if hero=='Samuro':
		names=[i.name for i in client.get_guild(DiscordGuildIDs['WindStriders']).get_role(DiscordRoleIDs['IllusionMaster']).members]
		message=await channel.send(hero+' discussion! Our mains are the **Illusion masters: '+', '.join(names)+'.** React to ping them.')
	elif mains:
		names=[client.get_user(int(i)).name for i in mains.replace('>','').replace(' ','').replace('!','').split('<@')[1:]]
		message=await channel.send(hero+' discussion! Our mains are **'+', '.join(names)+'.** React to ping them.')
	else:
		message=await channel.send(hero+" discussion! We don't have any mains for this hero, ping <@{}> if you know any. React to ping Balance team.".format(DiscordUserIDs['Blackstorm']))
	await message.add_reaction('\U0001f44d')

async def pingPokedex(client,message,member):
	vowels='AEIOU'
	if 'Balance team' in message.content:
		await message.channel.send(member.mention+' wants to start a'+'n'*(message.content[0] in vowels)+' '+message.content.split('We ')[0]+'<@&{}}>'.format(DiscordRoleIDs['BalanceTeam']))
	elif 'Samuro' in message.content:
		await message.channel.send(member.mention+' wants to start a Samuro discussion! <@&{}>'.format(DiscordRoleIDs['IllusionMaster']))
	else:
		pokedex=await fillPokedex(client)
		hero=message.content.split(' discussion!')[0]
		mains=pokedex.split(hero)[1].split('\n')[0]
		await message.channel.send(member.mention+' wants to start a'+'n'*(message.content[0] in vowels)+' '+message.content.split('Our ')[0]+mains)
	await message.delete()

async def pokedexCreationTrim(text):
	return text.replace('<@!460270968879841291>','').replace('  ',' ')

async def updatePokedex(client,text,message):
	if DiscordRoleIDs['Olympian'] not in [role.id for role in message.author.roles]:
		await message.channel.send('You need to be a mod to update the Pokedex!')
		return
	if len(text)!=2:
		await message.channel.send('Syntax is [updatepokedex/hero, ping].')
		return
	heroPing=text[1].split(',')
	if len(heroPing)!=2:
		await message.channel.send('Syntax is [updatepokedex/hero, ping].')
		return

	if heroPing[0] in ['remove','delete','all']:
		await removePokedex(client,heroPing[1].replace(' ','').replace('!','')[2:-1])
		await message.channel.send(heroPing[1]+' has been removed from all pokedex entries.')
		return
	hero=aliases(heroPing[0])
	if hero not in getHeroes():
		await message.channel.send('Invalid hero!')
		return
	user=heroPing[1].replace(' ','')
	if '<@' not in user:
		await message.channel.send('Invalid ping!')
		return

	pokedex_channel=client.get_channel(DiscordChannelIDs['Pokedex'])

	pokedex_messages=[]
	# We're unlikely to ever go above 50 messages in the pokedex.
	async for pokedex_message in pokedex_channel.history(limit=50):
		pokedex_messages.append(pokedex_message.content)

	pokedex_as_string = ''
	for pokedex_message in pokedex_messages:
		# Prepend the strings
		pokedex_as_string = pokedex_message + '\n' + pokedex_as_string
	
	# Let's update the message before splitting it
	hero=hero.replace('_',' ')

	pokedex_as_individual_hero_strings=pokedex_as_string.split('\n')
	pokedex_as_individual_hero_strings_new=[]

	for hero_mains_string in pokedex_as_individual_hero_strings:
		if hero in hero_mains_string:
			removal=False
			if user in hero_mains_string:
				removal=True
				pokedex_as_individual_hero_strings_new.append(hero_mains_string.replace(' '+user,''))
			else:
				pokedex_as_individual_hero_strings_new.append(hero_mains_string+' '+user)
		else:
			pokedex_as_individual_hero_strings_new.append(hero_mains_string)

	# Sort the string array alphabetically. Makes sure we're always in the right order.
	pokedex_as_individual_hero_strings_new.sort()

	pokedex_as_string_array=[]
	i = 0
	pokedex_as_string_array.append('\n')
	for hero_mains_string in pokedex_as_individual_hero_strings_new:
		if (len(pokedex_as_string_array[i] + hero_mains_string + '\n') < 2000):
			pokedex_as_string_array[i] += (hero_mains_string + '\n')
		else:
			i += 1
			pokedex_as_string_array.append(hero_mains_string + '\n')

	i = (len(pokedex_as_string_array) - 1)
	async for pokedex_message in pokedex_channel.history(limit=50):
		await pokedex_message.edit(content=pokedex_as_string_array[i])
		i -= 1

	# We've run out of messages, do we have content left?
	# We're never going to add two messages from 1 edit call, no need to worry about that.
	if i == 0:
		message_to_edit = await pokedex_channel.send('This will be edited soon.')
		await message_to_edit.edit(content=pokedex_as_string_array[i])
	
	if removal:
		await message.channel.send(user+' has been removed from '+hero)
	else:
		await message.channel.send(user+' has been added to '+hero)

async def removePokedex(client,MemberID): #Removes an user from all pokedex heroes
	pokedexChannel=client.get_channel(DiscordChannelIDs['Pokedex'])
	async for message in pokedexChannel.history(limit=50):
		MemberID=str(MemberID)
		await message.edit(content=message.content.replace(' <@'+MemberID+'>','').replace(' <@!'+MemberID+'>',''))