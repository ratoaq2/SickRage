# coding=utf-8

from tvdb_api.tvdb_api import Tvdb
#from tvrage_api.tvrage_api import TVRage
from pytvmaze.pytvmaze_api import TVmaze
from sickbeard import helpers

initConfig = {
    'valid_languages': [
        "da", "fi", "nl", "de", "it", "es", "fr", "pl", "hu", "el", "tr",
        "ru", "he", "ja", "pt", "zh", "cs", "sl", "hr", "ko", "en", "sv", "no"
    ],
    'langabbv_to_id': {
        'el': 20, 'en': 7, 'zh': 27,
        'it': 15, 'cs': 28, 'es': 16, 'ru': 22, 'nl': 13, 'pt': 26, 'no': 9,
        'tr': 21, 'pl': 18, 'fr': 17, 'hr': 31, 'de': 14, 'da': 10, 'fi': 11,
        'hu': 19, 'ja': 25, 'he': 24, 'ko': 32, 'sv': 8, 'sl': 30
    }
}

INDEXER_TVDB = 1
INDEXER_TVRAGE = 2  # Must keep
INDEXER_TVMAZE = 3

indexerConfig = {
    INDEXER_TVDB: {
        'enabled': True,
        'id': INDEXER_TVDB,
        'name': 'theTVDB',
        'module': Tvdb,
        'api_params': {
            'apikey': 'F9C450E78D99172E',
            'language': 'en',
            'useZip': True,
            'session': helpers.make_session(cache_etags=False),
        },
        'trakt_id': 'tvdb_id',
        'xem_origin': 'tvdb',
        'icon': 'thetvdb16.png',
        'scene_loc': 'https://cdn.pymedusa.com/scene_exceptions/scene_exceptions.json',
        'show_url': 'http://thetvdb.com/?tab=series&id=',
        'base_url': 'http://thetvdb.com/api/%(apikey)s/series/',
        'mapped_to': 'tvdbid'  # The attribute to which other indexers can map there thetvdb id to
    },
#     INDEXER_TVRAGE: {
#         'enabled': False,
#         'id': INDEXER_TVRAGE,
#         'name': 'TVRage',
#         'module': TVRage,
#         'api_params': {'apikey': 'Uhewg1Rr0o62fvZvUIZt',
#                        'language': 'en',
#         },
#         'session': helpers.make_session()
#     },
    INDEXER_TVMAZE: {
        'enabled': True,
        'id': INDEXER_TVMAZE,
        'name': 'TVmaze',
        'module': TVmaze,
        'trakt_id': 'tvdb_id',
        'xem_origin': 'tvdb',
        'api_params': {
            'language': 'en',
            'useZip': True,
            'session': helpers.make_session(cache_etags=False),
        },
        'trakt_id': 'tvdb_id',
        'xem_origin': 'tvdb',
        'icon': 'tvmaze16.png',
        'scene_loc': 'https://api.pymedusa.com/scene_exceptions.json',
        'show_url': 'http://www.tvmaze.com/shows/',
        'base_url': 'http://api.tvmaze.com/',
        'mapped_to': 'tvmazeid'  # The attribute to which other indexers can map there tvmaze id to
    }
}

indexerConfig[INDEXER_TVDB]['base_url'] %= indexerConfig[INDEXER_TVDB]['api_params']  # insert API key into base url
