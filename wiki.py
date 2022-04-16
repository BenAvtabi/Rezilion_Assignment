import requests
import re

results = []

response = requests.get('https://en.wikipedia.org/wiki/Beersheba')
pages = re.findall("(/wiki/[a-zA-Z0-9_]+)", response.content.decode())
pages = set(pages)

for page in pages:
	url = "https://en.wikipedia.org" + page
	page_response = requests.get(url)
	if re.search("(/wiki/Beersheba)", page_response.content.decode()):
		results.append(url)
		print("Found!")
print(results)
