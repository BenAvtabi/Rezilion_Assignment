import requests
import re

RELATIVE_PATH_PATTERN = '/wiki/[\w\(\) ,]+'
LINKED_ARTICLE_PATTERN = f'\"({RELATIVE_PATH_PATTERN})\"'

def make_proper_URL(relative_url):
	return f"https://en.wikipedia.org{relative_url}"

def get_relative_path(target_url):
	target_relative_path = re.search(RELATIVE_PATH_PATTERN, target_url)
	if not target_relative_path:
		raise SystemExit("Could not extract relative path from given URL")
	return target_relative_path.group()

def get_linked_articles_unique(article_url):
	response = requests.get(article_url)

	relative_urls = re.findall(LINKED_ARTICLE_PATTERN, response.text)
	if not relative_urls:
		raise SystemExit("Could not find any linked articles")

	return set([make_proper_URL(relative_url) for relative_url in relative_urls])

def does_have_link(article_url, expected_url):
	try:
		page_response = requests.get(article_url)
	except requests.exceptions.RequestException as e:
		print(f"Encountered a problem when trying to fetch {article_url}.")
		raise e

	return True if re.search(expected_url, page_response.text) else False

