from rest_framework import generics
from rest_framework.response import Response

from cdek.utils import get_rule_deliver_to_point, get_city_code
from cdek.models import CdekPoint
from core.models import UserRequest

class GetAllPoints(generics.RetrieveAPIView):

    @staticmethod
    def __get_format_phone(phone_number):
        """
        The function converts the phone number from the sender standard to the Yandex standard

        @param phone_number - phone number in Boxberry standart
        @param service      - sender's service name

        @return phone number in Yandex format
        """

        return f'{phone_number[:2]} ({phone_number[2:5]}) {phone_number[5:8]}-{phone_number[8:10]}-{phone_number[10:]}'

    @staticmethod
    def __get_format_day(day_of_week):
        """
        The function converts the day of the week from the sender standard to the Yandex standard

        @param day_of_week  - value of current day
        @param service      - sender's service name

        @return day in Yandex format
        """

        if day_of_week == 1:
            return 'MONDAY'
        elif day_of_week == 2:
            return 'TUESDAY'
        elif day_of_week == 3:
            return 'WEDNESDAY'
        elif day_of_week == 4:
            return 'THURSDAY'
        elif day_of_week == 5:
            return 'FRIDAY'
        elif day_of_week == 6:
            return 'SATURDAY'
        elif day_of_week == 7:
            return 'SUNDAY'

    def __get_shedule_items(self, source_shedule):
        """
        The function converts the delivery point schedule from sender format to Yandex format

        @param source_shedule   - The line that contains information about the schedule
        @param service          - sender's service name

        @return delivery shedule in Yandex format
        """
    
        result = []
            
        result.append(
            {
                'startDay'  : self.__get_format_day(1, 'cdek'),
                'endDay'    : self.__get_format_day(1, 'cdek'),
                'startTime' : source_shedule[0]['periods'].split('/')[0],
                'endTime'   : source_shedule[0]['periods'].split('/')[1]
            }
        )
        for item in source_shedule:
            if result[-1]['startTime'] == item['periods'].split('/')[0] and result[-1]['endTime'] == item['periods'].split('/')[1]:
                continue
            result[-1]['endDay'] = self.__get_format_day(int(item['day']) - 1, 'cdek')
            result.append(
                {
                    'startDay'  : self.__get_format_day(int(item['day']), 'cdek'),
                    'endDay'    : self.__get_format_day(int(item['day']), 'cdek'),
                    'startTime' : item['periods'].split('/')[0],
                    'endTime'   : item['periods'].split('/')[1]
                }
            )
        result[-1]['endDay'] = self.__get_format_day(7, 'cdek')

        return result


    #def get(self, data, city_code, deliver_rule):
    def get(self, request, *args, **kwargs):
        """
        The function converts point data from CDEK format to Yandex format

        @param data                     - data about points
        @param city_code                - Yandex city ID
        @param already_loaded_points    - set of points already loaded
        @param deliver_rule             - terms of delivery of the product from the sender

        @return returns the list of these points in Yandex format
        """
        city_region = UserRequest.objects.get(pk=kwargs['pk']).city_region
        city_code = get_city_code(
            city_region.split('-')[0],
            city_region.split('-')[1]
        )
        
        deliver_rule = get_rule_deliver_to_point(kwargs['pk'])

        if deliver_rule == {}: return []

        all_items = []
        data = CdekPoint.objects.filter(

        )
        for item in data:
            #if f"{item['name']} [{item['code']}]" in already_loaded_points: 
            #    print(f"ПВЗ с именем {item['name']} уже загружена.")
            #    continue

            sheduleItems = self.__get_shedule_items(item['workTimeYList'], 'cdek')

            if sheduleItems == -1: continue    

            phone_number = self.__get_format_phone(item['phoneDetailList'][0]['number'], 'cdek')

            descr = item['fullAddress']
            if len(descr) > 250: descr = descr[:251]

            all_items.append({
                'name'              : f"{item['name']} [{item['code']}]",
                'type'              : 'DEPOT',
                'coords'            : ', '.join([item['coordX'], item['coordY']]),
                'address'           : {
                    'regionId'          : kwargs['pk'],
                    'street'            : item['address'].split(',')[0],
                    'number'            : item['address'].split(',')[1],
                    'additional'        : descr
                },
                'phones'            : [phone_number],
                'workingSchedule'   : {
                    'scheduleItems'     : sheduleItems,
                },
                'deliveryRules'     : deliver_rule,
            })

            return Response(all_items)
