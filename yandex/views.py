from rest_framework import generics
from rest_framework.response import Response

from cdek.utils import get_rule_deliver_to_point, get_city_code
from cdek.models import CdekPoint
from core.models import UserRequest, Coordinat

class GetAllPoints(generics.RetrieveAPIView):
    queryset = CdekPoint.objects.all()

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

    def __get_shedule_items(self):#, source_shedule):
        #TODO
        source_shedule = [{"day":"1","periods":"08:00/23:00"},{"day":"2","periods":"08:00/23:00"},{"day":"3","periods":"08:00/23:00"},{"day":"4","periods":"08:00/23:00"},{"day":"5","periods":"08:00/23:00"},{"day":"6","periods":"08:00/23:00"},{"day":"7","periods":"08:00/23:00"}]
        """
        The function converts the delivery point schedule from sender format to Yandex format

        @param source_shedule   - The line that contains information about the schedule
        @param service          - sender's service name

        @return delivery shedule in Yandex format
        """
    
        result = []
            
        result.append(
            {
                'startDay'  : self.__get_format_day(1),
                'endDay'    : self.__get_format_day(1),
                'startTime' : source_shedule[0]['periods'].split('/')[0],
                'endTime'   : source_shedule[0]['periods'].split('/')[1]
            }
        )
        for item in source_shedule:
            if result[-1]['startTime'] == item['periods'].split('/')[0] and result[-1]['endTime'] == item['periods'].split('/')[1]:
                continue
            result[-1]['endDay'] = self.__get_format_day(int(item['day']) - 1)
            result.append(
                {
                    'startDay'  : self.__get_format_day(int(item['day'])),
                    'endDay'    : self.__get_format_day(int(item['day'])),
                    'startTime' : item['periods'].split('/')[0],
                    'endTime'   : item['periods'].split('/')[1]
                }
            )
        result[-1]['endDay'] = self.__get_format_day(7)

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
        city_region = UserRequest.objects.get(pk=kwargs['request_id']).city_region
        city_code = get_city_code(
            city_region.split('-')[0],
            city_region.split('-')[1]
        )
        
        deliver_rule = get_rule_deliver_to_point(city_code)

        if deliver_rule == {}: return []

        all_items = []
        data = CdekPoint.objects.filter(
            city_code = city_code
        )
        for item in data:
            #TODO
            #if f"{item['name']} [{item['code']}]" in already_loaded_points: 
            #    print(f"ПВЗ с именем {item['name']} уже загружена.")
            #    continue

            sheduleItems = self.__get_shedule_items()#item['workTimeYList'])

            if sheduleItems == -1: continue    

            phone_number = self.__get_format_phone(item.phone_number)

            descr = item.full_address
            if len(descr) > 250: descr = descr[:251]

            all_items.append({
                'name'              : item.name,
                'type'              : 'DEPOT',
                'coords'            : Coordinat.objects.get(point=item.id).yandex_format,
                'address'           : {
                    'regionId'          : city_code,
                    'street'            : item.address.split(',')[0],
                    'number'            : item.address.split(',')[1],
                    'additional'        : descr
                },
                'phones'            : [phone_number],
                'workingSchedule'   : {
                    'scheduleItems'     : sheduleItems,
                },
                'deliveryRules'     : deliver_rule,
            })

        return Response(all_items)
