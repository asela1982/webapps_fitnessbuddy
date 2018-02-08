def getGeo(address):
    import requests
    import json

    dictGeo ={}

    api_key = "AIzaSyBPtERPD47WmGx7r91ibrHiC_lRpcT99Xo"

    #construct the query
    base_url = "https://maps.googleapis.com"
    endpoint = "/maps/api/geocode/json"

    #configuration
    params = {
                "address" : address,
                "key" : api_key
                }
    
    try:
        # request the url
        response = requests.get(base_url+endpoint, params=params)
        results = response.json()['results'][0]

        def getCountry(results):

                for result in results['address_components']:
                    if result['types'][0] == "country":
                        return result['long_name']
                    
        dictGeo['lat'] = results['geometry']['location']['lat']
        dictGeo['lng'] = results['geometry']['location']['lng']
        dictGeo['country'] = getCountry(results)

        return dictGeo

    except Exception as ex:
        dictGeo['lat'] = 88.88
        dictGeo['lng'] = 88.88
        dictGeo['country'] = str(ex)
        return dictGeo