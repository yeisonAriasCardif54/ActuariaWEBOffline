
import time
import logging
import requests


class WebsiteDownException(Exception):
    pass


def ping_website(address, timeout=20):
    """
    Check if a website is down. A website is considered down
    if either the status_code >= 400 or if the timeout expires

    Throw a WebsiteDownException if any of the website down conditions are met
    """
    try:
        response = requests.head(address, timeout=timeout)
        if response.status_code >= 400:
            logging.warning("Website %s returned status_code=%s" % (address, response.status_code))
            raise WebsiteDownException()
    except requests.exceptions.RequestException:
        logging.warning("Timeout expired for website %s" % address)
        raise WebsiteDownException()


def notify_owner(address):
    """
    Send the owner of the address a notification that their website is down

    For now, we're just going to sleep for 0.5 seconds but this is where
    you would send an email, push notification or text-message
    """
    logging.info("Notifying the owner of %s website" % address)
    time.sleep(0.5)


def check_website(address):
    """
    Utility function: check if a website is down, if so, notify the user
    """
    try:
        ping_website(address)
    except WebsiteDownException:
        notify_owner(address)


# websites.py

WEBSITE_LIST = [
    'http://envato.com',
    'http://amazon.co.uk',
    'http://amazon.com',
    'http://facebook.com',
    'http://google.com',
    'http://google.fr',
    'http://google.es',
    'http://google.co.uk',
    'http://internet.org',
    'http://gmail.com',
    'http://stackoverflow.com',
    'http://github.com',
    'http://heroku.com',
    'http://really-cool-available-domain.com',
    'http://djangoproject.com',
    'http://rubyonrails.org',
    'http://basecamp.com',
    'http://trello.com',
    'http://yiiframework.com',
    'http://shopify.com',
    'http://another-really-interesting-domain.co',
    'http://airbnb.com',
    'http://instagram.com',
    'http://snapchat.com',
    'http://youtube.com',
    'http://baidu.com',
    'http://yahoo.com',
    'http://live.com',
    'http://linkedin.com',
    'http://yandex.ru',
    'http://netflix.com',
    'http://wordpress.com',
    'http://bing.com',
]

######
###### Enfoque Serial
######

# serial_squirrel.py
'''
import time
start_time = time.time()
for address in WEBSITE_LIST:
    check_website(address)
end_time = time.time()
print("Time for SerialSquirrel: %ssecs" % (end_time - start_time))

print('-----------------------------------------------------------------------------------------------------')
'''

######
###### Enfoque de Rosca
######
'''
import time
from queue import Queue
from threading import Thread
NUM_WORKERS = 4
task_queue = Queue()

def worker():
    # Constantly check the queue for addresses
    while True:
        address = task_queue.get()
        check_website(address)
        # Mark the processed task as done
        task_queue.task_done()


start_time = time.time()
# Create the worker threads
threads = [Thread(target=worker) for _ in range(NUM_WORKERS)]
# Add the websites to the task queue
[task_queue.put(item) for item in WEBSITE_LIST]
# Start all the workers
[thread.start() for thread in threads]
# Wait for all the tasks in the queue to be processed
task_queue.join()
end_time = time.time()
print("Time for ThreadedSquirrel: %ssecs" % (end_time - start_time))
'''



######
###### concurrent.futures
######

# future_squirrel.py
'''
import time
import concurrent.futures

NUM_WORKERS = 4
start_time = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    futures = {executor.submit(check_website, address) for address in WEBSITE_LIST}
    concurrent.futures.wait(futures)
end_time = time.time()
print("Time for FutureSquirrel: %ssecs" % (end_time - start_time))
'''


######
###### El enfoque Multiprocessing OK
######

import time
import socket
import multiprocessing
NUM_WORKERS = 8
if __name__ == '__main__':
    start_time = time.time()
    with multiprocessing.Pool(processes=NUM_WORKERS) as pool:
        results = pool.map_async(check_website, WEBSITE_LIST)
        results.wait()
    end_time = time.time()
    print("Time for MultiProcessingSquirrel: %ssecs" % (end_time - start_time))


######
###### Gevent NO
######
'''
# green_squirrel.py
import time
from gevent.pool import Pool
from gevent import monkey
# Note that you can spawn many workers with gevent since the cost of creating and switching is very low
NUM_WORKERS = 8
if __name__ == '__main__':
    # Monkey-Patch socket module for HTTP requests
    monkey.patch_socket()
    start_time = time.time()
    pool = Pool(NUM_WORKERS)
    for address in WEBSITE_LIST:
        pool.spawn(check_website, address)
    # Wait for stuff to finish
    pool.join()
    end_time = time.time()
    print("Time for GreenSquirrel: %ssecs" % (end_time - start_time))
'''


######
###### celery NO
######

# celery_squirrel.py
'''
import time
from utils import check_website
from data import WEBSITE_LIST
from celery import Celery
from celery.result import ResultSet

app = Celery('celery_squirrel',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

@app.task
def check_website_task(address):
    return check_website(address)

if __name__ == "__main__":
    start_time = time.time()
    # Using `delay` runs the task async
    rs = ResultSet([check_website_task.delay(address) for address in WEBSITE_LIST])
    # Wait for the tasks to finish
    rs.get()
    end_time = time.time()
    print("CelerySquirrel:", end_time - start_time)
    # CelerySquirrel: 2.4979639053344727

'''