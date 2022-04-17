from the_duality_of_parallelism import get_reverse_links_parallel

if __name__ == "__main__":
	target_url = input("Please enter a URL to an article in the English Wikipedia: ")

	results = get_reverse_links_parallel(target_url, True)
	print(results)
