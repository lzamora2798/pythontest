import requests
import threading
import time
import datetime


def run(_event, _context):

    main_list = []

    def worker(thread_num):
        request = requests.get("https://dweet.io/get/latest/dweet/for/thecore")
        data = request.json()
        info = data["with"][0]["content"]
        temperature = info["temperature"]
        humidity = info["humidity"]
        now = datetime.datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        main_list.append([str(temperature), str(humidity), date_time])

    # Number of threads to create
    num_threads = 15

    # # Create and start the threads in a for loop
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
        time.sleep(30)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    for data in main_list:
        print(",".join(data) + "\n")

    print("All threads have finished")