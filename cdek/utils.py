from requests import request
import json

from django.db.transaction import atomic

from cdek.models import CdekPoint
from core.models import Coordinat

def get_city_code(name, area=None):
    """
    The function receives via the CDEK API the ID of the selected city in the CDEK system

    @param name - name of the city
    @param area - area in which the city is located

    @return ID of the city in the CDEK system
    """

    url = f'http://integration.cdek.ru/v1/location/cities/json?cityName={name}'

    response = request("GET", url).json()

    if len(response) == 1 or area is None: 
        return response[0]['cityCode']
    
    for item in response:
        try:
            if item['region'].split()[0] == area: return item['cityCode']
        except KeyError:
            return item['cityCode']

def update_db(city, region):
    city_code = get_city_code(city, region)
    
    response = request('GET', f'http://integration.cdek.ru/pvzlist/v1/json?cityid={city_code}').json()

    pvz_bd_codes = CdekPoint.objects.filter(
        city_name = city,
    ).values_list('code', flat=True)

    for point_data in response['pvz']:
        if point_data['code'] not in pvz_bd_codes:
            with atomic():

                point = CdekPoint(
                    code = point_data['code'],
                    active_status = point_data['status'],
                    region_name = point_data['regionName'],
                    city_code = point_data['cityCode'],
                    city_name = point_data['city'],
                    work_time = point_data['workTime'],
                    address = point_data['address'],
                    full_address = point_data['fullAddress'],
                    phone_number = point_data['phone'],
                    note = point_data['note'],
                    name = 'CDEK_' + point_data['code']
                )
                point.save()

                coordinat = Coordinat(
                    point = point,
                    x = point_data['coordX'],
                    y = point_data['coordY']
                )
                coordinat.save()


def get_rule_deliver_to_point(code):
    """
    TODO Сделать вариативный выбор города отправителя

    The function receives information by API CDEK on the conditions of delivery to the selected city of Moscow

    @param code - ID of the selected city in the CDEK system

    @return data on delivery conditions in Yandex format
    """

    url = f'http://api.cdek.ru/calculator/calculate_price_by_json.php'

    headers = {
        'Content-Type' : 'application/json'
    }

    data = {
        "version"           : "1.0",
        "senderCityId"      : get_city_code('Москва', 'Москва'),
        "receiverCityId"    : code,
        "tariffId"          : 363,
        "goods" :
            [
                {
                    "weight"    : "0.2",
                    "length"    : "20",
                    "width"     : "30",
                    "height"    : "10"
                }
            ],
    }  
    response = request("POST", url, headers=headers, data=json.dumps(data)).json()

    try:
        data = response['result']
    except KeyError:
        return {'cost':-1}

    return {
        'cost'              : data['price'],
        'minDeliveryDays'   : data['deliveryPeriodMin'],
        'maxDeliveryDays'   : data['deliveryPeriodMax'],
        'deliveryServiceId' : 51
    }