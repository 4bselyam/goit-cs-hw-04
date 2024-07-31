import multiprocessing
import os


def search_keywords_in_file(file_path, keywords, queue):
    results = []
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        for keyword in keywords:
            if keyword in content:
                results.append((file_path, keyword))
    queue.put(results)


def worker(files, keywords, queue):
    for file in files:
        search_keywords_in_file(file, keywords, queue)


def main_multiprocessing(files, keywords, num_processes=4):
    processes = []
    queue = multiprocessing.Queue()

    # Divide files between processes
    chunk_size = len(files) // num_processes
    for i in range(num_processes):
        chunk = files[i * chunk_size : (i + 1) * chunk_size]
        if i == num_processes - 1:  # Ensure last process gets remaining files
            chunk = files[i * chunk_size :]
        process = multiprocessing.Process(target=worker, args=(chunk, keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Collect results
    results = []
    while not queue.empty():
        results.extend(queue.get())

    return results


if __name__ == "__main__":
    files = [
        "file1.txt",
        "file2.txt",
        "file3.txt",
        "file4.txt",
    ]  # Replace with your file paths
    keywords = ["justo", "Lorem"]
    results = main_multiprocessing(files, keywords)
    for result in results:
        print(f'Found keyword "{result[1]}" in file {result[0]}')
