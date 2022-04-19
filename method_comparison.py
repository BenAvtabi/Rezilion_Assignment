import time
import the_duality_of_parallelism

class ReverseLinkMethodComparison:
	_METHODS = {
		"Sync": the_duality_of_parallelism.ReverseLinkFinder.ExecutionMethod.sync,
		"Multithreading Raw": the_duality_of_parallelism.ReverseLinkFinder.ExecutionMethod.multithreading_raw,
		"Thread Pool Executor": the_duality_of_parallelism.ReverseLinkFinder.ExecutionMethod.thread_pool_executor,
		"Multiprocessing Raw": the_duality_of_parallelism.ReverseLinkFinder.ExecutionMethod.multiprocessing_raw,
		"Process Pool": the_duality_of_parallelism.ReverseLinkFinder.ExecutionMethod.process_pool
	}

	@staticmethod
	def compare_methods(target_url):
		time_results = {}
		for method_name, method in ReverseLinkMethodComparison._METHODS.items():
			print(f"About to get reverse link using method {method_name}...")
			try:
				start = time.time()
				reverse_links = the_duality_of_parallelism.ReverseLinkFinder.get_reverse_links(target_url, method)
				elapsed_time = time.time() - start
				print(f"Reverse links found: {reverse_links}")
				print(f"{method_name} took: {elapsed_time}\n")
				time_results[method_name] = elapsed_time
			except Exception as e:
				print(f"Failed to get reverse links: {e}")
				time_results[method_name] = None
		print(time_results)
