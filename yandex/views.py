from rest_framework import generics

class GetAllPoints(generics.RetrieveAPIView):
    def __get_yandex_type_by_cdek(data, city_code, already_loaded_points, deliver_rule):
        """
        The function converts point data from CDEK format to Yandex format

        @param data                     - data about points
        @param city_code                - Yandex city ID
        @param already_loaded_points    - set of points already loaded
        @param deliver_rule             - terms of delivery of the product from the sender

        @return returns the list of these points in Yandex format
        """

        if deliver_rule == {}: return []

        all_items = []
        for item in data:
            if f"{item['name']} [{item['code']}]" in already_loaded_points: 
                print(f"ПВЗ с именем {item['name']} уже загружена.")
                continue

            #sheduleItems = __get_shedule_items(item['workTimeYList'], 'cdek')

            #if sheduleItems == -1: continue    

            #phone_number = __get_format_phone(item['phoneDetailList'][0]['number'], 'cdek')

            descr = item['fullAddress']
            if len(descr) > 250: descr = descr[:251]

            all_items.append({
                'name'              : f"{item['name']} [{item['code']}]",
                'type'              : 'DEPOT',
                'coords'            : ', '.join([item['coordX'], item['coordY']]),
                'address'           : {
                    'regionId'          : city_code,
                    'street'            : item['address'].split(',')[0],
                    'number'            : item['address'].split(',')[1],
                    'additional'        : descr
                },
                #'phones'            : [phone_number],
                'workingSchedule'   : {
                #    'scheduleItems'     : sheduleItems,
                },
                'deliveryRules'     : deliver_rule,
            })

            return all_items