import requests
import re

results = []

print("Fetching target article...")
response = requests.get('https://en.wikipedia.org/wiki/Beersheba')

print("Finding linked wiki articles...")
relative_urls = set(re.findall("/wiki/[a-zA-Z0-9_]+", response.content.decode()))

print("Iterating over linked articles...")
for index, relative_url in enumerate(relative_urls):
	full_url = f"https://en.wikipedia.org{relative_url}"
	print("Fetching {} ({}/{})".format(full_url, index+1, len(relative_urls)))
	page_response = requests.get(full_url)

	if re.search("/wiki/Beersheba", page_response.content.decode()):
		print("Found reverse link!")
		results.append(full_url)

print(results)
