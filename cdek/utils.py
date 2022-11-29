from requests import request

def get_city_code(name, area=None):
    """
    The function receives via the CDEK API the ID of the selected city in the CDEK system

    @param name - name of the city
    @param area - area in which the city is located

    @return ID of the city in the CDEK system
    """

    url = f'http://integration.cdek.ru/v1/location/cities/json?cityName={name}'

    response = request("GET", url).json()
    print(response[-1])
    if len(response) == 1 or area is None: 
        return response[0]['cityCode']
    
    for item in response:
        try:
            if item['region'].split()[0] == area: return item['cityCode']
        except KeyError:
            return item['cityCode']