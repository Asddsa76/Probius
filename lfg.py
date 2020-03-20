def roleAliases(role):
	role='grandmaster' if role=='gm' else role
	role='master' if role=='masters' else role
	role='diamond' if role=='dia' else role
	role='platinum' if role=='plat' else role
	role='unranked' if role in ['ur','none','qm'] else role

	role='eu' if role=='europe' else role
	role='na' if role in ['northamerica','us','america','americas'] else role

	return role

async def lfg(channel,text,client):
	inputRoles=[roleAliases(j) for j in text.replace(' ','').split(',')]
	roles=[i for i in channel.guild.roles if i.name.lower().replace(' ','') in inputRoles]
	people=[i for i in channel.guild.members if len(roles)==sum(1 for j in roles if j in i.roles)]

	if len(roles)!=len(inputRoles):
		await channel.send('Invalid roles!')
	elif people:
		await channel.send(', '.join([i.name for i in people]))
	else:
		await channel.send('No people found!')