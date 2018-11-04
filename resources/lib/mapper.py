from addon import plugin
from addon import PluginInformation
from xbmcswift2 import actions
from HTMLParser import HTMLParser

import hof
import utils
import xbmc

def map_categories_item(item):
    return {
        'label': utils.colorize(item.get('title'), item.get('color')),
        'path': plugin.url_for('category', category_code=item.get('code'))
    }


def create_creative_item():
    return {
        'label': 'Creative I18N',
        'path': plugin.url_for('creative')
    }


def create_magazines_item():
    return {
        'label': 'Emissions I18N',
        'path': plugin.url_for('magazines')
    }


def create_weekly_item():
    return {
	'label':'Weekly Program',
	'path': plugin.url_for('weekly')
    }


def create_newest_item():
    return {
        'label': 'Most recent',
        'path': plugin.url_for('newest')
    }


def create_most_viewed_item():
    return {
        'label': 'Most viewed',
        'path': plugin.url_for('most_viewed')
    }


def create_last_chance_item():
    return {
        'label': 'Last Chance',
        'path': plugin.url_for('last_chance')
    }


def map_category_item(item, category_code):
    code = item.get('code')
    title = item.get('title')

    if code:
        path = plugin.url_for('sub_category_by_code', sub_category_code=code)
    else:
        path = plugin.url_for('sub_category_by_title', category_code=category_code,
                              sub_category_title=utils.sanitize_string(title))

    return {
        'label': title,
        'path': path
    }


def map_weekly_item(data):
    data = data.get('video')
    programId = data.get('programId')
    return hof.merge_dicts( map_video(data), {'rucksack': {'programId': programId}} )


def map_generic_item(config):
    programId = config.get('programId')

    is_playlist = programId.startswith('RC-') or programId.startswith('PL-')
    if not is_playlist:
        return map_video(config)
    else:
        return map_playlist(config)


def map_video(config):
    programId = config.get('programId')
    kind = config.get('kind')

    duration = int(config.get('duration') or 0) * \
        60 or config.get('durationSeconds')
    airdate = config.get('broadcastBegin')
    if airdate is not None:
        airdate = str(utils.parse_date(airdate))

    # Some content is not playable
    # json msg : You don't have the sufficient rights to access this kind

    path = plugin.url_for('play', kind=kind, program_id=programId)
    if path is not None:
        is_playable = True
    else:
        xbmc.log('Content for ' + str(kind) + ':' + str(programId) + ' filtered due insufficient rights', 2)
        is_playable = False

    ret_map = {
        'label': utils.format_title_and_subtitle(config.get('title'), config.get('subtitle')),
        'path': path,
        'thumbnail': config.get('imageUrl'),
        'is_playable': is_playable,
        'info_type': 'video',
        'info': {
            'title': config.get('title'),
            'duration': duration,
            'genre': config.get('genrePresse'),
            'plot': config.get('shortDescription'),
            'plotoutline': config.get('teaserText'),
            # year is not correctly used by kodi :(
            # the aired year will be used by kodi for production year :(
            #'year': int(config.get('productionYear')),
            'country': [country.get('label') for country in config.get('productionCountries', [])],
            'director': config.get('director'),
            'aired': airdate
        },
        'properties': {
            'fanart_image': config.get('imageUrl'),
        }
    }

    # Prepare filename for download

    label = config.get('title')
    subtitle = config.get('subtitle')
    if subtitle:
       label += ' - ' + subtitle

    label = u'{label}'.format(label=HTMLParser().unescape(label))

    down_map = { 'context_menu': [ ('Download video', actions.background(plugin.url_for('download', kind=kind, program_id=programId, title=label.encode('UTF-8')))) ] }

    # Extend ret_map with download option if selected

    if PluginInformation._download:
        return hof.merge_dicts( ret_map, down_map )
    else:
        return ret_map
 

def map_playlist(config):
    programId = config.get('programId')
    kind = config.get('kind')

    return {
        'label': utils.format_title_and_subtitle(config.get('title'), config.get('subtitle')),
        'path': plugin.url_for('collection', kind=kind, collection_id=programId),
        'thumbnail': config.get('imageUrl'),
        'info': {
            'title': config.get('title'),
            'plotoutline': config.get('teaserText')
        }
    }


def map_playable(streams, quality):
    stream = None
    for q in [quality] + [i for i in ['SQ', 'EQ', 'HQ', 'MQ'] if i is not quality]:
        stream = hof.find(lambda s: match(s, q), streams)
        if stream:
            break
    return {
        'path': stream.get('url')
    }


def match(item, quality):
    return item.get('quality') == quality and item.get('audioSlot') == 1
