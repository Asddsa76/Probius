import discord
async def colours(channel,text):
	if len(text)==1:
		await channel.send('Choose one of the following colours: black, blue, brown, cyan, fuchsia, green, grey, light blue, orange, pink, purple, red, teal, white, yellow.')
		return
	colour=text[1]
	try:
		await channel.send(file=discord.File('Colours/'+colour+'.PNG'))
	except:
		await channel.send(colour.capitalize()+' is not a valid colour.')