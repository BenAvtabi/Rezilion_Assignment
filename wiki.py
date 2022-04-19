import sys
import method_comparison

if __name__ == "__main__":
	if not (2 == len(sys.argv)):
		raise SystemExit("Usage: wiki.py wiki_url")
	target_url = sys.argv[1]

	method_comparison.compare_methods(target_url)
	"""Final results: {'Sync': 160.0629403591156,
						'Multithreading Raw': 22.139481782913208,
						'Thread Pool Executor': 24.32761859893799,
						'Multiprocessing Raw': 38.31907296180725,
						'Process Pool': 22.66799545288086}
		Notice that despite "Multithreading Raw" being very short,
			this is only because it made so many requests that wiki stopped responding and the requests died out.
		Please read the doc for `ExecutionMethod` to see why using "Multithreading Raw",
			and especially "Multiprocessing Raw" is bad for medium+ sized articles."""
