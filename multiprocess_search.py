import multiprocessing
import time
import os

def search_in_file(filename, keywords, queue):
    results = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                for keyword in keywords:
                    if keyword in line.lower():
                        results.setdefault(keyword, []).append(filename)
        queue.put(results)
    except FileNotFoundError:
        print(f"Помилка: Файл {filename} не знайдено.")
    except Exception as e:
        print(f"Помилка при обробці файлу {filename}: {e}")


def multiprocess_search(files, keywords):
    results = {}
    processes = []
    queue = multiprocessing.Queue()

    for file in files:
            process = multiprocessing.Process(target=search_in_file, args=(file, keywords, queue))
            processes.append(process)
            process.start()

    for process in processes:
        process.join()

    while not queue.empty():
        partial_results = queue.get()
        for keyword, found_files in partial_results.items():
            results.setdefault(keyword, []).extend(found_files)

    return results


if __name__ == "__main__":
    keywords = ["python", "програмування", "алгоритм", "дані", "комп'ютер"]
    directory = "test_files"
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    start_time = time.time()
    results = multiprocess_search(files, keywords)
    end_time = time.time()

    print("Результати пошуку (багатопроцесорний):")
    for keyword, found_files in results.items():
        print(f"{keyword}: {found_files}")

    print(f"Час виконання: {end_time - start_time:.4f} секунд")