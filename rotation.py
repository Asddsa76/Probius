from urllib.request import urlopen

async def rotation(channel):
	async with channel.typing():
		page=[i.strip().decode('utf-8') for i in urlopen('https://nexuscompendium.com/currently.php')]
		rotationHeroes=[]
		salesHeroes=[]
		gemPrices=[]
		limitedHeroSkins=[]
		limitedHeroSkinsVariations=[]
		limitedMounts=[]
		for line in page:
			if 'Week of ' in line:
				lineIndex=line.index('Week of ')
				output='**Free rotation w'+line[lineIndex+1:lineIndex+18]+':** from <https://nexuscompendium.com/>\n'
			if '<td valign="top" ' in line:
				if len(rotationHeroes)<14 and 'All Heroes' not in rotationHeroes:
					rotationHeroes.append(line[line.index('title="')+7:line.index('" alt')])
					print(rotationHeroes[0])
				else:
					salesHeroes.append(line[line.index('title="')+7:line.index('" alt')])
					gemPrices.append(line[line.index('Gems: ')+6:line.index('Gems: ')+9])
			elif '#skins">' in line:
				line=line.split('#skins">')[1]
				line=line[:line.index('<ul><li>Added')].replace('</a>','')

				if '(' in line:
					[hero,variant]=line.split('(')
				else:
					hero=line+' '
					variant='Base)'
				variant=variant[:-1]
				if hero not in limitedHeroSkins:
					limitedHeroSkins.append(hero)
					limitedHeroSkinsVariations.append([variant])
				else:
					limitedHeroSkinsVariations[limitedHeroSkins.index(hero)].append(variant)
			elif '#mounts">' in line:
				line=line.split('#mounts">')[1]
				limitedMounts.append(line[:line.index(' - Added')].replace('</a>',''))
		if rotationHeroes:
			output+=', '.join(rotationHeroes[:7])+'\n'
			output+=', '.join(rotationHeroes[8:])+'\n'
			output+='**Sales:** '+', '.join([salesHeroes[i]+' '+gemPrices[i]+' Gems' for i in range(len(salesHeroes))])
		if limitedHeroSkins:
			output+='\n**Limited Hero Skins:** \n '+'\n '.join([limitedHeroSkins[i]+'('+', '.join(limitedHeroSkinsVariations[i])+')' for i in range(len(limitedHeroSkins))])
		if limitedMounts:
			output+='\n**Limited Mounts:** '
			output+=', '.join(limitedMounts)
	await channel.send(output)