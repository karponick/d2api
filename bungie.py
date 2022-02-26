'''Wrapper module for Bungie API'''
import requests
import json

from config import API_KEY

# AUTH_PATH = "https://www.bungie.net/en/OAuth/Authorize"
ROOT_PATH = "https://www.bungie.net/Platform"
BASIC_PATH = "https://www.bungie.net"
HEADERS = {"X-API-Key": API_KEY}

def api_get(path, params):
    '''Basic GET call
    Args:
        path (String): path for API call
    Returns:
        (JSON) from response'''
    try:
        if params:
            r = requests.get(ROOT_PATH + path, headers=HEADERS, params=params)
        else:
            r = requests.get(ROOT_PATH + path, headers=HEADERS)
        return r.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

def api_post(path, body):
    '''Basic POST call
    Args:
        path (String): path for API call
        body (Dictionary): Extra daya in body required for API call
    Returns:
        (JSON) from response
    '''
    try:
        r = requests.post(ROOT_PATH + path, headers=HEADERS, data=body)
        return r.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

def get_manifest_links():
    '''Gets urls for manifests'''
    path = "/Destiny2/Manifest"
    return api_get(path, None)

def get_manifest():
    '''Get actual manifest - parse with definitions'''
    path = get_manifest_links()["Response"]["jsonWorldContentPaths"]["en"]
    try:
        r = requests.get(BASIC_PATH + path)
        return r.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

def get_image(path):
    '''Get image from Bungie's website using manifest data'''
    try:
        r = requests.get(BASIC_PATH + path, stream=True)
        return r.raw
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

def search_name(name, page):
    '''Search for player by name'''
    path = f"/User/Search/GlobalName/{page}"
    body = {"displayNamePrefix": name}
    return api_post(path, json.dumps(body))

def search_player_name(bungie_name):
    '''Get Destiny Player using Bungie Name
    Returned info contains Membership Type and ID
    '''
    bn = bungie_name.split("#") # 0 = name, 1 = code
    path = "/Destiny2/SearchDestinyPlayerByBungieName/All/"
    body = {"displayName": bn[0], "displayNameCode": int(bn[1])}
    return api_post(path, json.dumps(body))

def get_profile(membershipType, destinyMembershipId, components):
    '''Get Destiny Profile using Membership Type and Id'''
    path = f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/"
    params = {"components": components}
    return api_get(path, params)

def get_player(bungie_name, components):
    '''Combination of search_player_name and get_profile:
    Get membership info with search_player_name using Bungie Name,
    then use membership info to get_profile'''
    player = search_player_name(bungie_name)["Response"][0]
    membershipType = player["membershipType"]
    membershipId = player["membershipId"]
    return get_profile(membershipType, membershipId, components)

def get_character(membershipType, destinyMembershipId, characterId, components):
    '''Get character duh'''
    path = f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/"
    params = {"components": components}
    return api_get(path, params)