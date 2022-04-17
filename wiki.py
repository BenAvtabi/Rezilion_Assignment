import requests
import re
import threading

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
	try:
		response = requests.get(article_url)
	except requests.exceptions.RequestException as e:
		print(f"Encountered a problem when trying to fetch {article_url}:")
		raise SystemExit(e)

	relative_urls = re.findall(LINKED_ARTICLE_PATTERN, response.text)
	if not relative_urls:
		raise SystemExit("Could not find any linked articles")

	return set([make_proper_URL(relative_url) for relative_url in relative_urls])

def does_have_link(article_url, expected_url):
	try:
		page_response = requests.get(article_url)
	except requests.exceptions.RequestException as e:
		print(f"Encountered a problem when trying to fetch {article_url}:")
		raise SystemExit(e)

	return True if re.search(expected_url, page_response.text) else False

def append_if_reverse_link(results, article_url, target_relative_path):
	print(f"Fetching {article_url}")
	if does_have_link(article_url, target_relative_path):
		print(f"Found reverse link from {article_url}")
		results.append(article_url)

def find_reverse_link_multithreading(linked_articles, target_relative_path):
	results = []
	threads = []
	for article_url in linked_articles:
		thread = threading.Thread(target=append_if_reverse_link, args=(results, article_url, target_relative_path))
		threads.append(thread)
		thread.start()
	for thread in threads:
		thread.join()
	return results

if __name__ == "__main__":
	target_url = input("Please enter a URL to an article in the English Wikipedia: ")
	target_relative_path = get_relative_path(target_url)

	print("Finding linked wiki articles...")
	linked_articles = get_linked_articles_unique(target_url)

	results = find_reverse_link_multithreading(linked_articles, target_relative_path)
	print(results)
