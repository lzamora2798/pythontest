import requests
import threading
import time
import datetime
import os

from api.methods import push_to_webhook
from db.connection import db_connection
from db.models import Measure

main_list = []
sleep_time = int(os.environ["SLEEP_TIME"])
number_minutes = int(os.environ["NUMBER_MINUTES"])
URL = os.environ["SERVICE_URL"]


def worker():
    request = requests.get(URL)
    data = request.json()
    info = data["with"][0]["content"]
    temperature = info["temperature"]
    humidity = info["humidity"]
    main_list.append([temperature, humidity])
    with db_connection():
        Measure.objects.create(temperature=temperature, humidity=humidity)


def run(_event, _context):

    num_threads = number_minutes

    # # Create and start the threads in a for loop
    threads = []
    try:
        for i in range(num_threads):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
            time.sleep(sleep_time)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        data = {"data": main_list}
        push_to_webhook(data)
        return {"success": True}
    except Exception as err:
        print(err)
