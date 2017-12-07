# -*- coding: utf-8 -*-

import os
from multiprocessing.dummy import Pool

import requests

KEYS = ['id', 'owner_id', 'album_id', 'date', 'big', 'small']


def main(root):
    os.makedirs(root, exist_ok=True)
    count = 0

    def _download(url):
        nonlocal count
        count += 1
        if count % 50 == 0:
            print("{}".format(count))
        try:
            download(root, url)
        except Exception as e:
            print(e)

    Pool(50).map(_download, data())


def download(root, d):
    url = d['small']
    fname = url.split('/')[-1]
    name = "{}_{}_{}".format(d['id'], d['date'], fname)
    with open(os.path.join(root, name), 'wb') as file:
        res = requests.get(url)
        file.write(res.content)


def data():
    with open("photos.csv", "r") as fd:
        fd.readline()
        while True:
            line = fd.readline()
            if line is None or len(line) == 0:
                break
            line = line.split('\n')[0].split(',')
            d = {}
            for i in range(len(KEYS)):
                d[KEYS[i]] = line[i]
            yield d


if __name__ == '__main__':
    main("images")
