from method_comparison import compare_methods


if __name__ == "__main__":
	target_url = input("Please enter a URL to an article in the English Wikipedia: ")

	compare_methods(target_url)
	"""Final results: {'Sync': 156.205952167511,
						'Multithreading Raw': 22.243486642837524,
						'Thread Pool Executor': 26.372727155685425,
						'Multiprocessing Raw': 36.10838603973389,
						'Process Pool': 23.64469861984253}
		Please read the doc for `ExecutionMethod` to see why using "Multithreading Raw",
			and especially "Multiprocessing Raw" is bad for medium+ sized articles."""
