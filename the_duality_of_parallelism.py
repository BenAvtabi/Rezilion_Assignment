from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Process, Manager, Pool
from requests.exceptions import RequestException
from wikileaks import does_have_link, get_linked_articles_unique, get_relative_path

# TODO: Find a more suitable name, as there are now *5* methods and not just 2,
#	and one of them is "execute synchronically"

# *Notice* that creating threads/processes uncotrollably may cause wikipedia to stop responding.
# 	For medium-large sized articles, I highly recommend using a more subtle approach than an attempted DOS.
class ExecutionMethod:
	sync = 0 					# Completely synchronous
	multithreading_raw = 1		# Keep making threads like it's nobody's business
	thread_pool_executor = 2 	# Use a thread pool to limit the number of created thread (5x # of cpu cores)
	multiprocessing_raw = 3 	# Keep making processes like it's nobody's business
	process_pool = 4 			# Use a fixed process pool to limit the number created process (# of cpu cores)

def append_if_reverse_link(results, article_url, target_relative_path):
	try:
		if does_have_link(article_url, target_relative_path):
			print(f"Found reverse link from {article_url}")
			results.append(article_url)
	except RequestException as e:
		print(f"Encountered a problem when trying to fetch {article_url}.")

def get_reverse_links(target_url, execution_method):
	target_relative_path = get_relative_path(target_url)

	print("Finding linked wiki articles...")
	linked_articles = get_linked_articles_unique(target_url)
	print(f"Found {len(linked_articles)} linked articles")

	print("Finding reverse links...")
	match execution_method:
		case ExecutionMethod.sync:
			return get_reverse_links_sync(linked_articles, target_url)
		case ExecutionMethod.multithreading_raw:
			return get_reverse_links_multithreading(linked_articles, target_url)
		case ExecutionMethod.thread_pool_executor:
			return get_reverse_links_thread_pool_executor(linked_articles, target_url)
		case ExecutionMethod.multiprocessing_raw:
			return get_reverse_links_multiprocessing(linked_articles, target_url)
		case ExecutionMethod.process_pool:
			return get_reverse_links_process_pool(linked_articles, target_url)
		case _:
			raise SystemExit("Invalid execution method")

def get_reverse_links_multithreading(linked_articles, target_relative_path):
	results = []
	threads = []
	for article_url in linked_articles:
		thread = Thread(target=append_if_reverse_link, args=(results, article_url, target_relative_path))
		threads.append(thread)
		thread.start()
	for thread in threads:
		thread.join()
	return results

def get_reverse_links_thread_pool_executor(linked_articles, target_relative_path):
	results = []
	threads = []
	with ThreadPoolExecutor() as executor:
		running_tasks = [executor.submit(append_if_reverse_link, results, article_url, target_relative_path) for article_url in linked_articles]
		for running_task in as_completed(running_tasks):
			running_task.result()
	return results

def get_reverse_links_multiprocessing(linked_articles, target_relative_path):
	with Manager() as manager:
		results = manager.list()
		processes = []
		for article_url in linked_articles:
			process = Process(target=append_if_reverse_link, args=(results, article_url, target_relative_path))
			processes.append(process)
			process.start()
		for process in processes:
			process.join()
		return list(results)

def get_reverse_links_process_pool(linked_articles, target_relative_path):
	with Pool() as pool:
		with Manager() as manager:
			results = manager.list()
			multiple_processes = [pool.apply_async(append_if_reverse_link, (results, article_url, target_relative_path)) for article_url in linked_articles]
			for process in multiple_processes:
				process.get()
			return list(results)

def get_reverse_links_sync(linked_articles, target_relative_path):
	results = []
	for article_url in linked_articles:
		append_if_reverse_link(results, article_url, target_relative_path)

	return results
