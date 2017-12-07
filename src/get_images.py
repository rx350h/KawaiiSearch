from vk_api import VkApi
from vk_api import VkTools

import sys
import config

KEYS = ['id', 'owner_id', 'album_id', 'date', 'big', 'small']


def main(cfg, owner_id):
    session = VkApi(token=cfg.token, app_id=cfg.app_id, client_secret=cfg.client_secret, api_version='5.69')
    limit = get_limit(session, owner_id)
    iter_ = photos_iter(session, owner_id, limit)
    save(cfg.info_path(owner_id), iter_, limit)

def get_limit(session, owner_id):
    # TODO: load photos count in the album
    return 50000

def save(path, iter, limit):
    done = 0.0
    with open(path, "a") as fd:
        fd.write(','.join(KEYS) + "\n")
        for i in iter:
            done += 1
            fd.write(','.join(line(i)) + "\n")
            if done % 100 == 0:
                print("{}. Done: {}% of {}".format(done, round(100 * done / limit), limit))


def photos_iter(session, owner_id, limit):
    tools = VkTools(session)
    photos = tools.get_all_slow_iter('photos.get', 100,
                                     values={'owner_id': owner_id, 'photo_sizes': 1, 'rev': 1, 'album_id': 'wall'},
                                     limit=limit)
    for photo in photos:
        src = extract_photos(photo)
        if src is None:
            continue
        yield {'big': src['big'],
               'small': src['small'],
               'date': photo['date'],
               'id': photo['id'],
               'owner_id': photo['owner_id'],
               'album_id': photo['album_id']
               }


def line(data):
    # just to preserve order
    return [str(data[k]) for k in KEYS]


def extract_photos(photo):
    d = {}
    for s in photo['sizes']:
        d[s['type']] = s
    small = d.get('r', d.get('q', d.get('p',{}))).get('src', None)
    big = d.get('w', d.get('z', d.get('y', d.get('x', {})))).get('src', None)

    if (small is None) or (big is None):
        return None

    return {'big': big, 'small': small}


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("Should be `python3 src/download_images.py GROUP_ID`")
    main(config, sys.argv[1])