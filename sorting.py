async def trim(text):
	return text.lower().replace(' ','').replace('#','').replace('<@&557521663894224912>','')

async def sort(roles,member,olympian,client):
	guild=client.get_guild(535256944106012694)#Wind Striders
	channel=guild.get_channel(557366982471581718)#general
	if 557521663894224912 not in [role.id for role in olympian.roles]:
		await channel.send('You need to be a mod to sort users!')
		return
	if len(roles)!=3:
		await channel.send('Need ping and 3 roles')
		return
	#Colours between bestBot and IM
	bestBot=guild.get_role(635187043676323842)
	IM=guild.get_role(557550150109888513)
	#Ranks and regions between bots and unsorted
	bots=guild.get_role(574138911409045504)
	unsorted=guild.get_role(560435022427848705)

	if unsorted not in member.roles:
		await channel.send('**'+member.name+'** is not unsorted')
		return
	roles=list(set(roles))
	if len(roles)!=3:
		await channel.send('Need 3 *different* roles')
		return
	rolesToAdd=[]
	for role in roles:
		role='platinum' if role=='plat' else role
		role='diamond' if role=='dia' else role
		role='eu' if role=='europe' else role
		role='na' if role=='northamerica' else role
		role='na' if role=='us' else role
		role='unranked' if role=='ur' else role
		role='grandmaster' if role=='gm' else role
		for i in guild.roles:
			if (i<bestBot and i>IM) or (i<bots and i>unsorted):
				if await trim(i.name)==role:
					rolesToAdd.append(i)
	if len(rolesToAdd)!=3:
		await channel.send('At least one role was wrong or inaccessible')
		return
	memberRole=guild.get_role(557522023190888468)
	rolesToAdd.append(memberRole)
	await member.add_roles(*rolesToAdd)
	await member.remove_roles(unsorted)
	await channel.send('**'+member.name+'** has been sorted!')

async def sortFromMessage(text,message,client):
	roles=(await trim(text)).split(',')
	unsortedMember=roles.pop(0)
	guild=client.get_guild(535256944106012694)#Wind Striders
	unsortedMember=guild.get_member(int(unsortedMember.replace(' ','')[2:-1].replace('!','')))
	await sort(roles,unsortedMember,message.author,client)

async def sortFromReaction(message,reacterID,client):
	roles=(await trim(message.content)).split(',')
	unsortedMember=message.author
	guild=client.get_guild(535256944106012694)
	olympian=guild.get_member(int(reacterID))
	await sort(roles,unsortedMember,olympian,client)