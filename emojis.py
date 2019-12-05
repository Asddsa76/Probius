from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import re
from aliases import *#Spellcheck and alternate names for heroes
import discord
import io
import aiohttp

def getProxyEmojis(guild):#From PythonTest guild
	proxyEmojis={}
	for emoji in guild.emojis:
		proxyEmojis[emoji.name]='<'+'a'*emoji.animated+':'+emoji.name+':'+str(emoji.id)+'>'
	return proxyEmojis

async def sendEmoji(file,channel):
	try:
		await channel.send(file=discord.File(file+'.png'))
	except:
		try:
			await channel.send(file=discord.File(file+'.gif'))
		except:
			pass

async def carbotSpray(hero,channel):
	hero=aliases(hero)
	if hero in ['Deflect','Parry','Evade','Haha','Sleep']:
		imageFormat='.gif'
		if hero=='Deflect':
			hero='Ninja_Skills'
		elif hero=='Parry':
			hero="Paryin'_with_Varian"
		elif hero=='Evade':
			hero='Evade_This...'
		elif hero=='Haha':
			hero='Ha_HA_ha_HA!'
		elif hero=='Sleep':
			hero='Sleeping_Dragon'
	else:
		hero='Carbot_'+hero
		imageFormat='.png'
	emojiPage='https://heroesofthestorm.gamepedia.com/File:'+hero+'_Spray'+imageFormat

	html = urlopen(emojiPage)
	bs = BeautifulSoup(html, 'html.parser')
	images = bs.find_all('img', {'src':re.compile(imageFormat)})

	emojiImagePage=images[1 if imageFormat=='.gif' else 2]['src']

	async with aiohttp.ClientSession() as session:
		async with session.get(emojiImagePage) as resp:
			if resp.status != 200:
				pass
			data = io.BytesIO(await resp.read())
			await channel.send(file=discord.File(data, 'cool_image'+imageFormat))

async def emoji(client,text,channel):
	text[0]=text[0].replace(':','')
	if text[0]=='carbot':
		await carbotSpray(text[1],channel)
		return
	if text[0]=='proxy':
		await channel.send(''.join([i[1] for i in client.proxyEmojis.items()]))
		return
	if text[0] in client.proxyEmojis:
		await channel.send(client.proxyEmojis[text[0]])
		return

	if len(text)==2:
		hero=aliases(text[0]).replace('_',' ').replace('The Butcher','Butcher')
		emojiCode=text[1].replace('lol','rofl').replace('wow','surprised').replace('smile','happy')
		file=hero+' '+emojiCode
	else:
		file=text[0]
	
	await sendEmoji('Emojis/'+file.capitalize(),channel)


def downloadEmojis():
	EmojiListPage='https://heroesofthestorm.gamepedia.com/Emoji'
	page=[i.strip().decode('utf-8').split('" class="image"><img alt="Emoji ')[1].split('" width=')[0] for i in urlopen(EmojiListPage) if '<td align="center"><a href="/File:Emoji' in i.strip().decode('utf-8')]
	for i in page:
		[name,url]=i.split('" src="')
		if 'Pack' in name:
			name=name.split('Pack ')[1]
			if name[1]==' ':
				name=name[2:]
		name=name.replace('&#39;',"'").capitalize()
		print(name)
		urlretrieve(url,'Emojis/'+name)

if __name__ == '__main__':
	downloadEmojis()