def removeHyperlinks(page):
	try:
		splitPage=page.split('<a href=')
		intermediatePage=splitPage[0]
		splitPage=splitPage[1:]
		asplit=[]
		for i in splitPage:
			asplit.append(i.split('</a>'))
		intermediatePage+=''.join([i[0].split('>')[1]+i[1] for i in asplit])
		return intermediatePage
	except:#No hyperlinks (unlikely)
		return page

def removeColour(page):
	try:
		splitPage=page.split('<span style="color:')
		newPage=splitPage[0]
		for i in splitPage[1:]:
			newPage+=i[i.index('>')+1:]
		return newPage
	except:#No colour
		return page

def italicCooldowns(page):
	splitPage=page.split('Cooldown:')
	newPage=splitPage[0]
	for i in splitPage[1:]:
		j=i.index('seconds')
		newPage+='*Cooldown'+i[:j]+'seconds* '+i[j+7:]
	return newPage

def trim(page):
	#Program searches the text for < to know when to stop
	#and these are < in middle of plain text, stopping early
	page=removeHyperlinks(page)
	page=page.replace('<span style="color:#FD0">❢  Quest:</span>','\n    ***❢ Quest:***')
	page=page.replace('<br /><span style="color:#FD0">❢ Reward:</span>','\n    ***? Reward:***')
	page=page.replace('<span style="color:#D58"><strong>Active: </strong></span>',' ***Active:***')
	page=page.replace('seconds</span><br />','seconds ')
	page=page.replace('<br /><span style="color:#FD0">❢ Repeatable Quest:</span>','\n    ***❢ Repeatable Quest:***')
	page=page.replace('<i>Vector Targeting</i><br />','*Vector Targeting*: ')
	page=page.replace('<br />','')
	page=page.replace('<b>','')
	page=page.replace('</b>','')
	page=page.replace('Passive:','***Passive:***')#Adds a space to start
	page=removeColour(page)
	page=page.replace('</span>','')
	page=italicCooldowns(page)
	return page