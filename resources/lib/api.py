from collections import OrderedDict
import requests
import hof
import utils
import cache
import xbmc

from addon import PluginInformation

_base_api_url = 'http://www.arte.tv/hbbtvv2/services/web/index.php'
_base_headers = {
    'user-agent': PluginInformation.name + '/' + PluginInformation.version
}
_endpoints = {
    'categories': '/EMAC/teasers/categories/v2/{lang}',
    'category': '/EMAC/teasers/category/v2/{category_code}/{lang}',
    'subcategory': '/OPA/v3/videos/subcategory/{sub_category_code}/page/1/limit/100/{lang}',
    'magazines': '/OPA/v3/magazines/{lang}',
    'collection': '/OPA/v3/videos/collection/{kind}/{collection_id}/{lang}',
    'streams': '/OPA/v3/streams/{program_id}/{kind}/{lang}',
    'daily': '/OPA/v3/programs/{date}/{lang}'
}

_cache_db_path=PluginInformation._cache_db_path
_cache_db_store=PluginInformation._cache_db_store
_cache_db_name=PluginInformation._cache_db_name
_cache_db_table=PluginInformation._cache_db_table


def categories(lang):
    url = _endpoints['categories'].format(lang=lang)
    return _load_json(url).get('categories', {})


def special_categories(name, lang):
    url = _endpoints['category'].format(category_code=name, lang=lang)
    cat = _load_json(url).get('category', [])
    if cat:
        return cat[0].get('teasers', [])
    return []


def magazines(lang):
    url = _endpoints['magazines'].format(lang=lang)
    return _load_json(url).get('magazines', {})


def get_weekly_list(lang):
    return hof.flatten([dayly(date,lang) for (date, _) in utils.past_week()])


def dayly(date, lang):
    if PluginInformation._use_cache:
        _cache_db=cache.open_cache_db(_cache_db_path + _cache_db_store + _cache_db_name)
        _cache_conn=cache.open_cache_db_conn(_cache_db)
        if cache.check_cache_table( _cache_conn, _cache_db_table ):
            xbmc.log('create database table ' + _cache_db_table, 2)                         
            if cache.create_cache_db( _cache_db, _cache_conn, 'CREATE table '+_cache_db_table+' ( date, dict )' ):
                xmbc.log ('table ' + _cache_db_table + ' in database ' + _cache_db_name + ' could not created', 2)  
            else:                                           
                xbmc.log ('table ' + _cache_db_table + ' in database ' + _cache_db_name + ' successfully created', 2)
 
        url_ret = cache.get_cache_db(_cache_db, _cache_conn, _cache_db_table, date )
        if url_ret is None:                                 
            url_ret = _load_json(_endpoints['daily'].format(date=date, lang=lang)).get('programs', { } )
            if date != utils.past_week()[0][0]:
                cache.store_cache_db(_cache_db, _cache_conn, _cache_db_table, date, url_ret )
                xbmc.log('data cached for date ' + date, 2)
            else:
                xbmc.log('data is today (' + date + ') not written in cache', 2 )
        else:                                       
            xbmc.log('data successfully read from cache for date : ' + date, 2 )

        return url_ret
                                   
    else:                                                             
        url = _endpoints['daily'].format(date=date, lang=lang)
        return _load_json(url).get('programs', { } )


def category(category_code, lang):
    url = _endpoints['category'].format(category_code=category_code, lang=lang)
    return _load_json(url).get('category', {})


def subcategory(sub_category_code, lang):
    url = _endpoints['subcategory'].format(
        sub_category_code=sub_category_code, lang=lang)
    return _load_json(url).get('videos', {})


def collection(kind, collection_id, lang):
    url = _endpoints['collection'].format(kind=kind,
                                          collection_id=collection_id, lang=lang)
    return _load_json(url).get('videos', [])


def streams(kind, program_id, lang):
    url = _endpoints['streams'] .format(
        kind=kind, program_id=program_id, lang=lang)
    return _load_json(url).get('videoStreams', [])


def _load_json(url, params=None, headers=_base_headers):
    r = requests.get(_base_api_url + url, params=params, headers=headers)
    return r.json(object_pairs_hook=OrderedDict) 
