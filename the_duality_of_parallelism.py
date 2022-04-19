import threading
import concurrent.futures
import multiprocessing
import requests.exceptions
import wikileaks

# TODO: Find a more suitable name, as there are now *5* methods and not just 2,
#	and one of them is "execute synchronically"

class ReverseLinkFinder:
	# *Notice* that creating threads/processes uncotrollably may cause wikipedia to stop responding.
	# 	For medium-large sized articles, I highly recommend using a more subtle approach than an attempted DOS.
	class ExecutionMethod:
		sync = 0 					# Completely synchronous
		multithreading_raw = 1		# Keep making threads like it's nobody's business
		thread_pool_executor = 2 	# Use a thread pool to limit the number of created thread (5x # of cpu cores)
		multiprocessing_raw = 3 	# Keep making processes like it's nobody's business
		process_pool = 4 			# Use a fixed process pool to limit the number created process (# of cpu cores)

	@staticmethod
	def get_reverse_links(target_url, execution_method):
		target_relative_path = wikileaks.Wikileaks.get_relative_path(target_url)

		print("Finding linked wiki articles...")
		linked_articles = wikileaks.Wikileaks.get_linked_articles_unique(target_url)
		print(f"Found {len(linked_articles)} linked articles")

		print("Finding reverse links...")
		match execution_method:
			case ReverseLinkFinder.ExecutionMethod.sync:
				return ReverseLinkFinder._get_reverse_links_sync(linked_articles, target_url)
			case ReverseLinkFinder.ExecutionMethod.multithreading_raw:
				return ReverseLinkFinder._get_reverse_links_multithreading(linked_articles, target_url)
			case ReverseLinkFinder.ExecutionMethod.thread_pool_executor:
				return ReverseLinkFinder._get_reverse_links_thread_pool_executor(linked_articles, target_url)
			case ReverseLinkFinder.ExecutionMethod.multiprocessing_raw:
				return ReverseLinkFinder._get_reverse_links_multiprocessing(linked_articles, target_url)
			case ReverseLinkFinder.ExecutionMethod.process_pool:
				return ReverseLinkFinder._get_reverse_links_process_pool(linked_articles, target_url)
			case _:
				raise Exception("Invalid execution method was used.")

	@staticmethod
	def _append_if_reverse_link(results, article_url, target_relative_path):
		try:
			if wikileaks.Wikileaks.does_have_link(article_url, target_relative_path):
				print(f"Found reverse link from {article_url}")
				results.append(article_url)
		except requests.exceptions.RequestException as e:
			print(f"Encountered a problem when trying to fetch {article_url}.")

	@staticmethod
	def _get_reverse_links_multithreading(linked_articles, target_relative_path):
		results = []
		threads = []
		for article_url in linked_articles:
			thread = threading.Thread(target=ReverseLinkFinder._append_if_reverse_link,
				args=(results, article_url, target_relative_path))
			threads.append(thread)
			thread.start()
		for thread in threads:
			thread.join()
		return results

	@staticmethod
	def _get_reverse_links_thread_pool_executor(linked_articles, target_relative_path):
		results = []
		threads = []
		with concurrent.futures.ThreadPoolExecutor() as executor:
			running_tasks = [executor.submit(
				ReverseLinkFinder._append_if_reverse_link, results, article_url, target_relative_path)
					for article_url in linked_articles]
			for running_task in concurrent.futures.as_completed(running_tasks):
				running_task.result()
		return results

	@staticmethod
	def _get_reverse_links_multiprocessing(linked_articles, target_relative_path):
		with multiprocessing.Manager() as manager:
			results = manager.list()
			processes = []
			for article_url in linked_articles:
				process = multiprocessing.Process(target=ReverseLinkFinder._append_if_reverse_link,
					args=(results, article_url, target_relative_path))
				processes.append(process)
				process.start()
			for process in processes:
				process.join()
			return list(results)

	@staticmethod
	def _get_reverse_links_process_pool(linked_articles, target_relative_path):
		with multiprocessing.Pool() as pool:
			with multiprocessing.Manager() as manager:
				results = manager.list()
				multiple_processes = [pool.apply_async(
					ReverseLinkFinder._append_if_reverse_link, (results, article_url, target_relative_path))
						for article_url in linked_articles]
				for process in multiple_processes:
					process.get()
				return list(results)

	@staticmethod
	def _get_reverse_links_sync(linked_articles, target_relative_path):
		results = []
		for article_url in linked_articles:
			ReverseLinkFinder._append_if_reverse_link(results, article_url, target_relative_path)

		return results
