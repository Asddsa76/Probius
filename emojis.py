from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import re
from aliases import *#Spellcheck and alternate names for heroes
import discord
import io
import aiohttp

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

async def emoji(text,channel):
	hero=aliases(text[0])#Emoji pages are case sensitive. Sadly, capitalizing also ruins non-hero emojis (Nexus pack etc).
	if hero=='Carbot':
		await carbotSpray(text[1],channel)
		return
	emojiCode=text[1].replace('lol','rofl').replace('wow','surprised')

	emojiPackCode='2_'
	if hero in ['Nexus','Chomp']:
		emojiPackCode=''
	elif emojiCode in ['happy','rofl','sad','silly','meh']:
		emojiPackCode='1_'

	emojiCode=emojiCode.capitalize()
	if emojiCode=='Rofl':
		emojiCode='ROFL'

	imageFormat='.png'
	if hero in ['Chomp']:
		imageFormat='.gif'

	emojiPage='https://heroesofthestorm.gamepedia.com/File:Emoji_'+hero+'_Pack_'+emojiPackCode+hero+'_'+emojiCode+imageFormat

	html = urlopen(emojiPage)
	bs = BeautifulSoup(html, 'html.parser')
	images = bs.find_all('img', {'src':re.compile(imageFormat)})
	emojiImagePage=images[0]['src']

	async with aiohttp.ClientSession() as session:
		async with session.get(emojiImagePage) as resp:
			if resp.status != 200:
				pass
			data = io.BytesIO(await resp.read())
			await channel.send(file=discord.File(data, 'cool_image'+imageFormat))

def downloadEmojis():
	urlretrieve('https://gamepedia.cursecdn.com/allstars_gamepedia/2/23/Emoji_E.T.C._Pack_1_E.T.C._Sad.png?version=e4cbec81ce39e6767306519916ee6b48','etcsad.png')

if __name__ == '__main__':
	downloadEmojis()