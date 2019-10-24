from urllib.request import urlopen

def rotation():
	page=[i.strip().decode('utf-8') for i in urlopen('https://nexuscompendium.com/currently.php')]
	rotationHeroes=[]
	salesHeroes=[]
	gemPrices=[]
	for line in page:
		if 'Week of ' in line:
			lineIndex=line.index('Week of ')
			output='**Free rotation w'+line[lineIndex+1:lineIndex+18]+':** from <https://nexuscompendium.com/>\n'
		if '<td valign="top" ' in line:
			if len(rotationHeroes)<14:
				rotationHeroes.append(line[line.index('title="')+7:line.index('" alt')])
			else:
				salesHeroes.append(line[line.index('title="')+7:line.index('" alt')])
				gemPrices.append(line[line.index('Gems: ')+6:line.index('Gems: ')+9])
	output+=', '.join(rotationHeroes[:7])+'\n'
	output+=', '.join(rotationHeroes[8:])+'\n'
	output+='**Sales:** '+', '.join([salesHeroes[i]+' '+gemPrices[i]+' Gems' for i in range(len(salesHeroes))])
	return output

if __name__=='__main__':
	print(rotation())