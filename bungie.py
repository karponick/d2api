'''Wrapper module for Bungie API'''
import requests
import json

CLIENT_ID = "39282"
AUTH_PATH = "https://www.bungie.net/en/OAuth/Authorize"
ROOT_PATH = "https://www.bungie.net/Platform"
HEADERS = {"X-API-Key": "21a9e8aa1323434abbcb65442849a058"}

def api_get(path):
    '''Basic GET call
    Args:
        path (String): path for API call
    Returns:
        (JSON) from response'''
    try:
        r = requests.get(ROOT_PATH + path, headers=HEADERS)
        return r.json()
    except:
        print(r)
        print(r.url)
        exit()

def api_getp(path, params):
    '''GET call with parameters'''
    r = requests.get(ROOT_PATH + path, headers=HEADERS, params=params)
    return r.json()

def api_post(path, body):
    '''Basic POST call
    Args:
        path (String): path for API call
        body (Dictionary): Extra daya in body required for API call
    Returns:
        (JSON) from response
    '''
    r = requests.post(ROOT_PATH + path, headers=HEADERS, data=body)
    return r.json()

def get_manifest_links():
    '''Gets urls for manifests'''
    path = "/Destiny2/Manifest"
    return api_get(path)

def get_manifest():
    '''Get actual manifest info for definition using manifest urls'''
    path = get_manifest_links()["Response"]["jsonWorldContentPaths"]["en"]
    r = requests.get(f"https://www.bungie.net/{path}", headers=HEADERS)
    return r.json()

def search_name(name, page):
    '''Search for player by name'''
    path = f"/User/Search/GlobalName/{page}"
    body = {"displayNamePrefix": name}
    return api_post(path, json.dumps(body))

def get_player(bungie_name):
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
    return api_getp(path, params)

def get_user(bungie_name, components):
    '''Combination of get_player and get_user:
    Get membership info with get_player using Bungie Name,
    then use membership info to get_profile'''
    player = get_player(bungie_name)["Response"][0]
    membershipType = player["membershipType"]
    membershipId = player["membershipId"]
    return get_profile(membershipType, membershipId, components)

def get_character(membershipType, destinyMembershipId, characterId, components):
    '''Get character duh'''
    path = f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/"
    params = {"components": components}
    return api_get(path, params)