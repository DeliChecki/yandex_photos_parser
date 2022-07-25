import json
import os

import bs4
import requests
from tqdm import tqdm
import logging
from urllib.parse import urlparse
from threading import Thread

import numpy as np


# #############################################################################
WORKER_NUMBERS = 5
FILENAME = "1.html"
# #############################################################################


# load html from file
def get_html(resource_url):
    with open(resource_url, "r") as file:
        html = file.read()
    return html


# get images
def get_images(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    images = soup.find_all("div", class_="serp-item")
    return images


class Worker(Thread):
    def __init__(self, worker_number, images, bar):
        super().__init__()

        self.name = "Worker {0}".format(worker_number)
        self.worker_number = worker_number

        self.images = images
        self.bar = bar

    def run(self):
        return self.save_images(self.images)

    # save images with cycling name (1.jpg, 2.jpg, 3.jpg, ...)
    def save_images(self, images):
        for i in range(len(images)):
            link = json.loads(images[i]["data-bem"])["serp-item"]["img_href"]

            try:
                content = requests.get(link, timeout=2)

            except Exception as e:
                print(e)
                self.bar.update(1)
                continue

            # with open(f"images/{str(i).zfill(4)}.jpg", "wb") as file:
            #     file.write(content.content)

            path = urlparse(link).path
            ext = os.path.splitext(path)[1] or ".png"
            ext = ext.lower()

            with open(f"images/{str(self.worker_number) + '_' + str(i).zfill(4)}{ext}", "wb") as file:
                file.write(content.content)

            self.bar.update(1)


# run program
def run():
    html = get_html(FILENAME)
    images = get_images(html)

    print(len(images), images[:10])

    numbers = np.arange(len(images))
    numbers_slices = [len(x) for x in np.array_split(numbers, WORKER_NUMBERS)]
    numbers_slices = [sum(numbers_slices[:i]) for i in range(len(numbers_slices))] + [sum(numbers_slices) - 1]

    # make pairs with i and i + 1 element from numbers_slices
    pairs = [(numbers_slices[i], numbers_slices[i + 1]) for i in range(len(numbers_slices) - 1)]

    images_ = []

    for pair in pairs:
        images_.append(images[pair[0]:pair[1]])

    bar = tqdm(total=len(images))

    workers = []

    for i in range(len(images_)):
        worker = Worker(i, images_[i], bar)
        workers.append(worker)
        worker.start()


if __name__ == "__main__":
    run()
