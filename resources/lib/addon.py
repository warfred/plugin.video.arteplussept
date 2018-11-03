
# coding=utf-8
# -*- coding: utf-8 -*-
#
# plugin.video.arteplussept, Kodi add-on to watch videos from http://www.arte.tv/guide/fr/plus7/
# Copyright (C) 2015  known-as-bmf
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
from xbmcswift2 import Plugin
import xbmc
import os

# global declarations
# plugin stuff
plugin = Plugin()


class PluginInformation:
    name = plugin.name
    version = plugin.addon.getAddonInfo('version')
    profile = plugin.addon.getAddonInfo('profile')
    addonpath = plugin.addon.getAddonInfo('path')
    _use_cache = plugin.get_setting('cache', bool) or False
    _download  = plugin.get_setting('download', bool) or False
    _cache_db_path=xbmc.translatePath(profile)
    _cache_db_store='.storage/'
    _cache_db_name='ARTE_CACHE.db'
    _cache_db_long=_cache_db_path + _cache_db_store + _cache_db_name
    _cache_db_table='arte_cache'
    

# settings stuff
languages = ['fr', 'de', 'en', 'es', 'pl']
qualities = ['SQ', 'EQ', 'HQ']

# defaults to fr
language = languages[plugin.get_setting('lang', int)] or languages[0]
# defaults to SQ
quality = qualities[plugin.get_setting('quality', int)] or qualities[0]
# set download folder
download_folder = plugin.get_setting('download_folder') or None

# my imports
import view
import ostools

@plugin.route('/', name='index')
def index():
    return view.build_categories(language)


@plugin.route('/category/<category_code>', name='category')
def category(category_code):
    return view.build_category(category_code, language)


@plugin.route('/creative', name='creative')
def creative():
    return []


@plugin.route('/weekly', name='weekly')
def weekly():
    plugin.set_content('tvshows')
    return plugin.finish(view.build_weekly(language))


@plugin.route('/magazines', name='magazines')
def magazines():
    plugin.set_content('tvshows')
    return plugin.finish(view.build_magazines(language))


@plugin.route('/newest', name='newest')
def newest():
    plugin.set_content('tvshows')
    return plugin.finish(view.build_newest(language))
 
 
@plugin.route('/most_viewed', name='most_viewed')
def most_viewed():
    plugin.set_content('tvshows')
    return plugin.finish(view.build_most_viewed(language))

 
@plugin.route('/last_chance', name='last_chance')
def last_chance():
    plugin.set_content('tvshows')
    return plugin.finish(view.build_last_chance(language))


@plugin.route('/sub_category/<sub_category_code>', name='sub_category_by_code')
def sub_category_by_code(sub_category_code):
    plugin.set_content('tvshows')
    return plugin.finish(view.build_sub_category_by_code(sub_category_code, language))


@plugin.route('/sub_category/<category_code>/<sub_category_title>', name='sub_category_by_title')
def sub_category_by_title(category_code, sub_category_title):
    plugin.set_content('tvshows')
    return plugin.finish(view.build_sub_category_by_title(category_code, sub_category_title, language))


@plugin.route('/collection/<kind>/<collection_id>', name='collection')
def collection(kind, collection_id):
    plugin.set_content('tvshows')
    return plugin.finish(view.build_mixed_collection(kind, collection_id, language))


@plugin.route('/play/<kind>/<program_id>', name='play')
def play(kind, program_id):
    return plugin.set_resolved_url(view.build_stream_url(kind, program_id, language, quality))


@plugin.route('/cleandb', name='cleandb')
def cleandb():
    ret=ostools.delete(PluginInformation._cache_db_long)
    if ret[0]:
        plugin.notify('Cache-Database deleted', 'Success')
    else:
        plugin.notify(ret[1], 'ERROR' )

    return plugin.finish()


@plugin.route('/download/<kind>/<program_id>/<title>', name='download')
def download_file(kind, program_id, title):
    if download_folder:
        plugin.notify(title, 'Downloading')
        ret=ostools.download_http( download_folder + title + '_' + program_id + os.extsep + 'mp4', view.build_stream_url(kind, program_id, language, quality)['path'] )
        if ret[0]:
            plugin.notify('Download completed', title)
        else:
            xbmc.sleep(10000)
            plugin.notify('Download error', ret[1] )
    else:                                                    
        plugin.notify('Please set a download folder in the settings', 'Configuration ERROR')


"""

@plugin.route('/broadcast', name='broadcast')
def broadcast():
    plugin.set_content('tvshows')
    items = custom.map_broadcast_item(
        custom.past_week_programs(language.get('short', 'fr')))
    return plugin.finish(items)

"""

# plugin bootstrap
if __name__ == '__main__':
    plugin.run()
