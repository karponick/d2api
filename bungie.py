'''Wrapper module for Bungie API'''
import requests
import json

CLIENT_ID = "39282"
AUTH_PATH = "https://www.bungie.net/en/OAuth/Authorize"
ROOT_PATH = "https://www.bungie.net/Platform"
HEADERS = {"X-API-Key": "21a9e8aa1323434abbcb65442849a058"}

'''Basic GET call
Params:
    path (String): path for API call
Returns:
    (JSON) from response'''
def api_get(path):
    try:
        r = requests.get(ROOT_PATH + path, headers=HEADERS)
        return r.json()
    except:
        print(r)
        print(r.url)
        exit()

'''GET call with querystring parameters'''
def api_getp(path, params):
    r = requests.get(ROOT_PATH + path, headers=HEADERS, params=params)
    return r.json()

'''Basic POST call
Params:
    path (String): path for API call
    body (Dictionary): Extra daya in body required for API call
Returns:
    (JSON) from response'''
def api_post(path, body):
    r = requests.post(ROOT_PATH + path, headers=HEADERS, data=body)
    return r.json()

'''Gets urls for manifests'''
def get_manifest():
    path = "/Destiny2/Manifest"
    return api_get(path)

'''Get actual manifest info for definition using manifest urls'''
def get_definitions(definition):
    path = get_manifest()["Response"]["jsonWorldContentPaths"]["en"]
    r = requests.get(f"https://www.bungie.net/{path}", headers=HEADERS)
    return r.json()[definition]

'''Search for player by name'''
def search_name(name, page):
    path = f"/User/Search/GlobalName/{page}"
    body = {"displayNamePrefix": name}
    return api_post(path, json.dumps(body))

'''Get Destiny Player using Bungie Name
Returned info contains Membership Type and ID'''
def get_player(bungie_name):
    bn = bungie_name.split("#") # 0 = name, 1 = code
    path = "/Destiny2/SearchDestinyPlayerByBungieName/All/"
    body = {"displayName": bn[0], "displayNameCode": int(bn[1])}
    return api_post(path, json.dumps(body))

'''Get Destiny Profile using Membership Type and Id'''
def get_profile(membershipType, destinyMembershipId, components):
    path = f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/"
    params = {"components": components}
    return api_getp(path, params)

'''Combination of get_player and get_user:
Get membership info with get_player using Bungie Name,
then use membership info to get_profile'''
def get_user(bungie_name, components):
    player = get_player(bungie_name)["Response"][0]
    membershipType = player["membershipType"]
    membershipId = player["membershipId"]
    return get_profile(membershipType, membershipId, components)

'''Get character duh'''
def get_character(membershipType, destinyMembershipId, characterId, components):
    path = f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/"
    params = {"components": components}
    return api_get(path, params)