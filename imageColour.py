import requests
from PIL import Image
import io
from miscFunctions import getAvatar
import discord

async def avatarColour(client,channel,userMention):
	async with channel.typing():
		URL=await getAvatar(client,channel,userMention)
		r = requests.get(URL, stream=True)
		img = Image.open(r.raw)
		rgb_img = img.convert('RGB')
		size=img.size
		pixels=size[0]*size[1]

		colours={}
		for x in range(size[0]):
			for y in range(size[1]):
				colour=str(rgb_img.getpixel((x,y)))
				if colour in colours:
					colours[colour]+=1
				else:
					colours[colour]=0

		#All pixel RGB values, sorted by descending frequency. Example element: [[12, 28, 44], 1758]
		colours=[[[int(j) for j in i[0][1:-1].split(', ')],i[1]] for i in sorted(list(colours.items()),key=lambda x:-x[1])]
		
		#Mean
		weightedSquaredColours=[[i[1]*i[0][0]**2,i[1]*i[0][1]**2,i[1]*i[0][2]**2] for i in colours]
		mean=[0,0,0]
		for i in range(3):
			mean[i]=round((sum(j[i] for j in weightedSquaredColours)/pixels)**0.5)

		#Output image
		img = Image.new('RGB', (200,200), color = tuple(mean))
	with io.BytesIO() as image_binary:
		img.save(image_binary, 'PNG')
		image_binary.seek(0)
		await channel.send(file=discord.File(fp=image_binary, filename='img.png'))