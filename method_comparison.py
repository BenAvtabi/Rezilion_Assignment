import time
import the_duality_of_parallelism

METHODS = {
	"Sync": the_duality_of_parallelism.ExecutionMethod.sync,
	"Multithreading Raw": the_duality_of_parallelism.ExecutionMethod.multithreading_raw,
	"Thread Pool Executor": the_duality_of_parallelism.ExecutionMethod.thread_pool_executor,
	"Multiprocessing Raw": the_duality_of_parallelism.ExecutionMethod.multiprocessing_raw,
	"Process Pool": the_duality_of_parallelism.ExecutionMethod.process_pool
}

def compare_methods(target_url):
	results = {}
	for method_name, method in METHODS.items():
		start = time.time()
		result = the_duality_of_parallelism.get_reverse_links(target_url, method)
		elapsed_time = time.time() - start
		print(result)
		print(f"{method_name} took: {elapsed_time}\n")
		results[method_name] = elapsed_time
	print(results)