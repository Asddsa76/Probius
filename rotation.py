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
		goldMounts=[]
		saleWeek=''
		skinsLimited=''
		mountsLimited=''
		boost360=''
		for line in page:
			if 'Special Free-to-Play Period ' in line:
				line=line.split('">')[1].split('<')[0]
				output='**Free rotation '+line+':** from <https://nexuscompendium.com/>\n'
			elif 'A quick overview' in line or '<meta ' in line:
				continue
			elif 'Heroic Deals and Limited-Time Items' in line:
				lineIndex=line.index('">')
				saleWeek='**Heroic Deals and Limited-Time Items '+line[lineIndex+2:lineIndex+25]+':**\n'
			elif 'Free-to-Play Hero Rotation' in line:
				lineIndex=line.index('">')
				output='**Free rotation '+line[lineIndex+2:lineIndex+25]+':** from <https://nexuscompendium.com/>\n'
			elif '<td valign="top" ' in line:
				if 'title="360 Boost' in line:
					boost360=line.split('</s>')[1].split(' <img src="')[0]+'<:nexusGem:697309829051449424>'
					print(boost360)
				elif len(rotationHeroes)<14 and 'All Heroes' not in rotationHeroes:
					rotationHeroes.append(line[line.index('title="')+7:line.index('" alt')])
				else:
					salesHeroes.append(line[line.index('title="')+7:line.index('" alt')])
					gemPriceIndex=line.index(' <img src="/images/icon/gem.png"')
					gemPrices.append(line[gemPriceIndex-3:gemPriceIndex])
			elif '/skins/' in line:
				line=line.split('">')[1]
				if '<ul><li>Added' in line:
					line=line[:line.index('<ul><li>Added')].replace('</a>','')
					skinsLimited='Limited '
				else:
					#line=line[:line.index('</a>')]
					continue

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
				try:
					limitedMounts.append(line[:line.index('<ul><li>Added')].replace('</a>',''))
					mountsLimited='Limited '
				except:
					limitedMounts.append(line[:line.index('</a></li>')])
			elif '<li>Gold Mount -' in line:
				goldMounts.append(line.split('">')[1].split('</a>')[0]+' '+line.split('</a> (')[1].split(' <img')[0]+'<:nexusGold:744794020487626837>\n')

		if rotationHeroes:
			output+=', '.join(rotationHeroes[:7])+'\n'
			output+=', '.join(rotationHeroes[7:])+'\n'
			output+=saleWeek
			output+='**Sales:** '+', '.join([salesHeroes[i]+' '+gemPrices[i]+'<:nexusGem:697309829051449424>' for i in range(len(salesHeroes))])+'\n'
		if limitedHeroSkins:
			#output+='**'+skinsLimited+'Hero Skins:** \n '+'\n '.join([limitedHeroSkins[i]+'('+', '.join(limitedHeroSkinsVariations[i])+')' for i in range(len(limitedHeroSkins))])+'\n'
			output+='**'+skinsLimited+'Hero Skins:** \n '+'\n '.join(limitedHeroSkins)+'\n'
		if limitedMounts:
			output+='**'+mountsLimited+'Mounts:** '
			output+=', '.join(limitedMounts)
		if goldMounts:
			output+='**Gold mounts:** '+', '.join(goldMounts)
		if boost360:
			output+='**Boosts:** 360 days'+boost360
	await channel.send(output)