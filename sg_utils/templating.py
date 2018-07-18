def openHTML(fileName, **kwargs):
	with open(fileName, 'r') as f:
		htmlFile = f.read()
	return fillTemplate(htmlFile, **kwargs)

def fillTemplate(htmlFile, **kwargs):
	for arg in kwargs:
		htmlFile = htmlFile.replace("{{ "+arg+" }}", kwargs[arg])
	return htmlFile
