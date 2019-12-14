async def sort(text,message,client):
	text=text.split(',')
	guild=client.get_guild(535256944106012694)#Wind Striders
	if 557521663894224912 not in [role.id for role in message.author.roles]:
		await message.channel.send('You need to be a mod to sort users!')
		return
	if len(text)!=4:
		await message.channel.send('Need ping and 3 roles')
		return
	#Colours between bestBot and IM
	bestBot=guild.get_role(635187043676323842)
	IM=guild.get_role(557550150109888513)
	#Ranks and regions between bots and unsorted
	bots=guild.get_role(574138911409045504)
	unsorted=guild.get_role(560435022427848705)

	member=guild.get_member(int(text.pop(0).replace(' ','')[2:-1].replace('!','')))
	if unsorted not in member.roles:
		await message.channel.send('**'+member.name+'** is not unsorted')
		return
	text=list(set(text))
	if len(text)!=3:
		await message.channel.send('Need 3 *different* roles')
		return
	rolesToAdd=[]
	for role in text:
		for i in guild.roles:
			if (i<bestBot and i>IM) or (i<bots and i>unsorted):
				if i.name.lower().replace(' ','').replace('#','')==role.lower().replace(' ','').replace('#',''):
					rolesToAdd.append(i)
	if len(rolesToAdd)!=3:
		await message.channel.send('At least one role was wrong or inaccessible')
		return
	memberRole=guild.get_role(557522023190888468)
	rolesToAdd.append(memberRole)
	await member.add_roles(*rolesToAdd)
	await member.remove_roles(unsorted)
	await message.channel.send('**'+member.name+'** has been sorted!')