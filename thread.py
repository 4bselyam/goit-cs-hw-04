import threading
import os


def search_keywords_in_file(file_path, keywords, results, lock):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        for keyword in keywords:
            if keyword in content:
                with lock:
                    results.append((file_path, keyword))


def worker(files, keywords, results, lock):
    for file in files:
        search_keywords_in_file(file, keywords, results, lock)


def main_threading(files, keywords, num_threads=4):
    threads = []
    results = []
    lock = threading.Lock()

    # Divide files between threads
    chunk_size = len(files) // num_threads
    for i in range(num_threads):
        chunk = files[i * chunk_size : (i + 1) * chunk_size]
        if i == num_threads - 1:  # Ensure last thread gets remaining files
            chunk = files[i * chunk_size :]
        thread = threading.Thread(target=worker, args=(chunk, keywords, results, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results


if __name__ == "__main__":
    files = [
        "file1.txt",
        "file2.txt",
        "file3.txt",
        "file4.txt",
    ]  # Replace with your file paths
    keywords = ["justo", "Lorem"]
    results = main_threading(files, keywords)
    for result in results:
        print(f'Found keyword "{result[1]}" in file {result[0]}')
