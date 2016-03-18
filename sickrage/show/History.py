# coding=utf-8
# This file is part of SickRage.
#

# Git: https://github.com/PyMedusa/SickRage.git
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage. If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from datetime import timedelta
from sickbeard.common import Quality
from sickbeard.db import DBConnection
from sickrage.helper.common import try_int


class History(object):
    date_format = '%Y%m%d%H%M%S'

    def __init__(self):
        self.db = DBConnection()

    def clear(self):
        """
        Clear all the history
        """
        self.db.action(
            'DELETE '
            'FROM history '
            'WHERE 1 = 1'
        )

    def get(self, limit=100, action=None):
        """
        :param limit: The maximum number of elements to return
        :param action: The type of action to filter in the history. Either 'downloaded' or 'snatched'. Anything else or
                        no value will return everything (up to ``limit``)
        :return: The last ``limit`` elements of type ``action`` in the history
        """

        actions = History._get_actions(action)
        limit = History._get_limit(limit)

        common_sql = 'SELECT action, date, episode, provider, h.quality, resource, season, show_name, showid ' \
                     'FROM history h, tv_shows s ' \
                     'WHERE h.showid = s.indexer_id '
        filter_sql = 'AND action in (' + ','.join(['?'] * len(actions)) + ') '
        order_sql = 'ORDER BY date DESC '

        if actions:
            results = self.db.select(common_sql + filter_sql + order_sql, actions)
        else:
            results = self.db.select(common_sql + order_sql)

        data = compact = []
        for result in results:
            data.append({
                'action': result['action'],
                'date': result['date'],
                'episode': result['episode'],
                'provider': result['provider'],
                'quality': result['quality'],
                'resource': result['resource'],
                'season': result['season'],
                'show_id': result['showid'],
                'show_name': result['show_name']
            })

        for row in data:
            action = {
                'action': row['action'],
                'provider': row['provider'],
                'resource': row['resource'],
                'time': row['date']
            }

            if not any((history['show_id'] == row['show_id'] and
                        history['season'] == row['season'] and
                        history['episode'] == row['episode'] and
                        history['quality'] == row['quality']) for history in compact):
                history = {
                    'actions': [action],
                    'episode': row['episode'],
                    'quality': row['quality'],
                    'resource': row['resource'],
                    'season': row['season'],
                    'show_id': row['show_id'],
                    'show_name': row['show_name']
                }

                compact.append(history)
            else:
                index = [i for i, item in enumerate(compact)
                         if item['show_id'] == row['show_id'] and
                         item['season'] == row['season'] and
                         item['episode'] == row['episode'] and
                         item['quality'] == row['quality']][0]
                history = compact[index]
                history['actions'].append(action)
                history['actions'].sort(key=lambda x: x['time'], reverse=True)

        return data[:limit]

    def trim(self):
        """
        Remove all elements older than 30 days from the history
        """

        self.db.action(
            'DELETE '
            'FROM history '
            'WHERE date < ?',
            [(datetime.today() - timedelta(days=30)).strftime(History.date_format)]
        )

    @staticmethod
    def _get_actions(action):
        action = action.lower() if isinstance(action, (str, unicode)) else ''

        if action == 'downloaded':
            return Quality.DOWNLOADED

        if action == 'snatched':
            return Quality.SNATCHED

        return []

 
    @staticmethod
    def _get_limit(limit):
        limit = try_int(limit, 0)

        return max(limit, 0)
