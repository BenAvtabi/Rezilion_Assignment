import requests
import re

target_url = input("Please enter a URL to an article in the English Wikipedia: ")

print("Fetching target article...")
try:
	response = requests.get(target_url)#'https://en.wikipedia.org/wiki/Beersheba')
except requests.exceptions.RequestException as e:
	print(f"Encountered a problem when trying to fetch {target_url}:")
	raise SystemExit(e)

print("Finding linked wiki articles...")
relative_urls = set(re.findall("/wiki/[a-zA-Z0-9_]+", response.text))

print("Iterating over linked articles...")
results = []
for index, relative_url in enumerate(relative_urls):
	full_url = f"https://en.wikipedia.org{relative_url}"
	print("Fetching {} ({}/{})".format(full_url, index+1, len(relative_urls)))

	try:
		page_response = requests.get(full_url)
	except requests.exceptions.RequestException as e:
		print(f"Encountered a problem when trying to fetch {full_url}:")
		raise SystemExit(e)

	if re.search("/wiki/Beersheba", page_response.text):
		print("Found reverse link!")
		results.append(full_url)

print(results)
