from discordIDs import *
from lfg import roleAliases

async def trim(text):
	toRemove=[' ','#','<@&{}>'.format(DiscordRoleIDs['Olympian']),'*','\n','league',' and']
	text=text.lower()
	for i in toRemove:
		text=text.replace(i,'')
	if '<@' in text:
		text=text[:text.index('<')]+text[1+text.index('>'):]#Remove pings
	return text

async def sort(roles,member,olympian,client):
	guild=client.get_guild(DiscordGuildIDs['WindStriders'])#Wind Striders
	channel=guild.get_channel(DiscordChannelIDs['General'])#general
	if DiscordRoleIDs['Olympian'] not in [role.id for role in olympian.roles]:
		#await channel.send('You need to be a mod to sort users!')
		return
	if len(roles)!=3:
		#await channel.send('Need ping and 3 roles')
		return
	#Colours
	blue1=guild.get_role(577565172357398530)
	magenta=guild.get_role(653065647563210792)
	#Ranks and regions
	gm=guild.get_role(559024554144694303)
	sea=guild.get_role(562624527020982293)

	unsorted=guild.get_role(DiscordRoleIDs['Unsorted'])

	if unsorted not in member.roles:
		#await channel.send('**'+member.name+'** is not unsorted')
		return
	roles=list(set(roles))
	if len(roles)!=3:
		#await channel.send('Need 3 *different* roles')
		return
	rolesToAdd=[]
	for role in roles:
		try:
			role=roleAliases(role)
			for i in sorted(guild.roles):
				if (i<=blue1 and i>=magenta) or (i<=gm and i>=sea):
					if await trim(i.name)==await trim(role):
						rolesToAdd.append(i)
					elif await trim(i.name)==await trim(''.join([i for i in role if not i.isdigit()])):#Rank numbers
						rolesToAdd.append(i)
					elif await trim(i.name)==await trim(role+'1'):#Add colour #1
						rolesToAdd.append(i)
					else:
						continue
					raise Exception('Role done!')
		except:
			pass
	if len(rolesToAdd)!=3:
		#await channel.send('At least one role was wrong or inaccessible. Valid roles: '+', '.join([i.name for i in rolesToAdd]))
		return
	memberRole=guild.get_role(DiscordRoleIDs['Member'])
	rolesToAdd.append(memberRole)
	await member.add_roles(*rolesToAdd)
	await member.remove_roles(unsorted)
	await channel.send('**'+member.name+'** has been sorted!')
	await giveLfgRoles(member,client)

async def sortFromMessage(text,message,client):
	unsortedMember,text=text.split('>')
	unsortedMember+='>'
	text=await trim(text)
	guild=client.get_guild(DiscordGuildIDs['WindStriders'])#Wind Striders
	unsortedMember=guild.get_member(int(unsortedMember.replace(' ','')[2:-1].replace('!','')))

	roles=text.split(',')
	if roles[0]=='':
		roles.pop(0)
	await sort(roles,unsortedMember,message.author,client)

async def sortFromReaction(message,reacterID,client):
	roles=await trim(message.content)
	if '/' in roles:
		roles=roles.split('/')
	else:
		roles=roles.split(',')
	unsortedMember=message.author
	guild=client.get_guild(DiscordGuildIDs['WindStriders'])
	olympian=guild.get_member(int(reacterID))
	await sort(roles,unsortedMember,olympian,client)

async def giveLfgRoles(member,client):
	reaction=[i for i in (await (await client.fetch_channel(634012658625937408)).fetch_message(693380327413907487)).reactions if i.emoji=='🇱'][0]
	users=await reaction.users().flatten()
	if member.id not in (i.id for i in users):
		return
	for i in [i.id for i in member.roles]:
		if i in client.wsLfgRoles:
			await member.add_roles(client.get_guild(DiscordGuildIDs['WindStriders']).get_role(client.wsLfgRoles[i]))

async def removeLfgRoles(member,client):
	invertedDict={v: k for k, v in client.wsLfgRoles.items()}
	for i in [i.id for i in member.roles]:
		if i in invertedDict:
			await member.remove_roles(client.get_guild(DiscordGuildIDs['WindStriders']).get_role(i))