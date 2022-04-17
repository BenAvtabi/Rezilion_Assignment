from the_duality_of_parallelism import ExecutionMethod, get_reverse_links
import time

METHODS = {
	"Sync": ExecutionMethod.sync,
	"Multithreading Raw": ExecutionMethod.multithreading_raw,
	"Thread Pool Executor": ExecutionMethod.thread_pool_executor,
	"Multiprocessing Raw": ExecutionMethod.multiprocessing_raw,
	"Process Pool": ExecutionMethod.process_pool
}

def compare_methods(target_url):
	results = {}
	for method_name, method in METHODS.items():
		start = time.time()
		result = get_reverse_links(target_url, method)
		elapsed_time = time.time() - start
		print(result)
		print(f"{method_name} took: {elapsed_time}\n")
		results[method_name] = elapsed_time
	print(results)