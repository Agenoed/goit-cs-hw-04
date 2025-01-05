import threading
import time
import os

def search_in_file(filename, keywords, results):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                for keyword in keywords:
                    if keyword in line.lower():
                        results.setdefault(keyword, []).append(filename)
    except FileNotFoundError:
        print(f"Помилка: Файл {filename} не знайдено.")
    except Exception as e:
        print(f"Помилка при обробці файлу {filename}: {e}")


def threaded_search(files, keywords):
    results = {}
    threads = []
    
    for file in files:
            thread = threading.Thread(target=search_in_file, args=(file, keywords, results))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    return results


if __name__ == "__main__":
    keywords = ["python", "програмування", "алгоритм", "дані", "комп'ютер"]
    directory = "test_files"
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    start_time = time.time()
    results = threaded_search(files, keywords)
    end_time = time.time()

    print("Результати пошуку (багатопотоковий):")
    for keyword, found_files in results.items():
        print(f"{keyword}: {found_files}")

    print(f"Час виконання: {end_time - start_time:.4f} секунд")