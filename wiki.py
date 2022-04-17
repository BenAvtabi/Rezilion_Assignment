import requests
import re

ARTICLE_RELATIVE_PATH_PATTERN = "/wiki/[^\"]+"

def make_proper_URL(relative_url):
	return f"https://en.wikipedia.org{relative_url}"

def get_relative_path(target_url):
	target_relative_path = re.search(ARTICLE_RELATIVE_PATH_PATTERN, target_url)
	if target_relative_path:
		target_relative_path = target_relative_path.group()
	else:
		raise SystemExit("Could not extract relative path from given URL")
	return target_relative_path

def get_linked_articles_unique(article_url):
	try:
		response = requests.get(article_url)
	except requests.exceptions.RequestException as e:
		print(f"Encountered a problem when trying to fetch {article_url}:")
		raise SystemExit(e)

	relative_urls = re.findall(ARTICLE_RELATIVE_PATH_PATTERN, response.text)
	return set([make_proper_URL(relative_url) for relative_url in relative_urls])

def does_have_link(article_url, expected_url):
	try:
		page_response = requests.get(article_url)
	except requests.exceptions.RequestException as e:
		print(f"Encountered a problem when trying to fetch {article_url}:")
		raise SystemExit(e)

	return True if re.search(target_relative_path, page_response.text) else False

target_url = input("Please enter a URL to an article in the English Wikipedia: ")
target_relative_path = get_relative_path(target_url)

print("Finding linked wiki articles...")
linked_articles = get_linked_articles_unique(target_url)
if not linked_articles:
	raise SystemExit("Could not find any linked articles")

print("Iterating over linked articles...")
results = []
for index, article_url in enumerate(linked_articles):
	print("Fetching {} ({}/{})".format(article_url, index+1, len(linked_articles)))
	if does_have_link(article_url, target_relative_path):
		print("Found reverse link!")
		results.append(article_url)

print(results)
