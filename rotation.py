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
		for line in page:
			if 'Special Free-to-Play Period ' in line:
				line=line.split('">')[1].split('<')[0]
				output='**Free rotation '+line+':** from <https://nexuscompendium.com/>\n'
			elif 'Week of ' in line:
				lineIndex=line.index('Week of ')
				if 'Heroic Deals and Limited-Time Items ' not in line:
					output='**Free rotation w'+line[lineIndex+1:lineIndex+18]+':** from <https://nexuscompendium.com/>\n'
				else:
					saleWeek='**Heroic Deals and Limited-Time Items w'+line[lineIndex+1:lineIndex+18]+':**\n'
			elif '<td valign="top" ' in line:
				if len(rotationHeroes)<14 and 'All Heroes' not in rotationHeroes:
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
				goldMounts.append(line.split('">')[1].split('<img src="/images/icon/gold.png"')[0].replace('</a> -','')+'<:nexusGold:744794020487626837>')

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
	await channel.send(output)