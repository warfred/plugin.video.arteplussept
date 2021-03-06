
import api
import mapper
import hof
import utils

_weekly_useless = { 'CLIP', 'MANUAL_CLIP', 'TRAILER' }

def build_categories(lang):
    categories = []
    categories.append(mapper.create_weekly_item())
    categories.append(mapper.create_newest_item())
    categories.append(mapper.create_most_viewed_item())
    categories.append(mapper.create_last_chance_item())
    categories.extend([mapper.map_categories_item(item) for item in api.categories(lang)])
    categories.append(mapper.create_creative_item())
    categories.append(mapper.create_magazines_item())

    return categories


def build_newest(lang):
    return [mapper.map_generic_item(item) for item in api.special_categories('MOST_RECENT', lang)]


def build_most_viewed(lang):
    return [mapper.map_generic_item(item) for item in api.special_categories('MOST_VIEWED', lang)]


def build_last_chance(lang):
    return [mapper.map_generic_item(item) for item in api.special_categories('LAST_CHANCE', lang)]


def build_magazines(lang):
    return [ mapper.map_generic_item(item) for item in api.magazines(lang) ]


def build_weekly(lang):
    # get video-list w/o useless entries
    weekly_map = [ mapper.map_weekly_item(item) for item in api.get_weekly_list(lang) if item.get('video') is not None if not _weekly_useless.issuperset( { str(item.get('video').get('kind')) } ) ]
    # remove dublicate entries
    weekly_map_list = {v['rucksack']['programId']:v for v in weekly_map}.values()
    # sort list by airdate
    weekly_map_list.sort(key=lambda item: item['info']['aired'], reverse=True)    
    # cleanup rucksack attributes from list for kodi types
    [ utils.eraseElement(item,'rucksack') for item in weekly_map_list ]
    return weekly_map_list


def build_category(category_code, lang):
    category = [mapper.map_category_item(
        item, category_code) for item in api.category(category_code, lang)]

    return category


def build_sub_category_by_code(sub_category_code, lang):
    return [mapper.map_generic_item(item) for item in api.subcategory(sub_category_code, lang)]


def build_sub_category_by_title(category_code, sub_category_title, lang):
    category = api.category(category_code, lang)
    sub_category = hof.find(lambda i: utils.sanitize_string(
        i.get('title')) == sub_category_title, category)

    return [mapper.map_generic_item(item) for item in sub_category.get('teasers')]


def build_mixed_collection(kind, collection_id, lang):
    return [mapper.map_generic_item(item) for item in api.collection(kind, collection_id, lang)]


def build_stream_url(kind, program_id, lang, quality):
    return mapper.map_playable(api.streams(kind, program_id, lang), quality)
