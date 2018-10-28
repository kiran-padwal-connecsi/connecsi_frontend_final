import datetime
import requests
from connecsiApp import base_url


class Classified:
    def __init__(self,user_id,classified_id=''):
        self.user_id=user_id
        self.classified_id=classified_id
        self.url_view_classified = base_url + 'Classified/' + str(self.user_id)
        self.url_view_classified_details = base_url + 'Classified/' + str(self.classified_id) + '/' + str(self.user_id)

    def get_all_classifieds(self):
        view_classfied_data = ''
        try:
            view_classified_response = requests.get(url=self.url_view_classified)
            view_classfied_data = view_classified_response.json()
            print(view_classfied_data)
            for item in view_classfied_data['data']:
                # print(item)
                region_id_list = item['regions'].split(',')
                region_name_list = []
                for region_id in region_id_list:
                    try:
                        region_name_response = requests.get(url=base_url + 'Youtube/regionCode/' + str(region_id))
                        region_data = region_name_response.json()
                        region_name = region_data['data'][0][1]
                        region_name_list.append(region_name)
                    except:
                        pass
                cat_response = requests.get(url=base_url + 'Youtube/videoCategories/' + str(item['video_cat_id']))
                # print(cat_response.json())
                cat_json_data = cat_response.json()
                video_cat_name = cat_json_data['data'][0]['video_cat_name']
                item.update({'video_cat_name': video_cat_name})
                item.update({'region_name_list': region_name_list})
                try:
                    string_from_date = datetime.datetime.strptime(item['from_date'], '%Y-%m-%d')
                    string_from_date = string_from_date.strftime('%d-%b-%y')
                    string_to_date = datetime.datetime.strptime(item['to_date'], '%Y-%m-%d')
                    string_to_date = string_to_date.strftime('%d-%b-%y')
                    item.update({'from_date': string_from_date})
                    item.update({'to_date': string_to_date})
                except Exception as e:
                    print(e)
            print('classified data', view_classfied_data)
            return view_classfied_data
        except Exception as e:
            print(e)
            pass
            return view_classfied_data

    def get_classified_details(self):
        view_classfied_details = ''
        try:
            view_classified_details_response = requests.get(url=self.url_view_classified_details)
            view_classfied_details = view_classified_details_response.json()
            print(view_classfied_details)

            for item in view_classfied_details['data']:
                # print(item)
                region_id_list = item['regions'].split(',')
                region_name_list = []
                for region_id in region_id_list:
                    try:
                        region_name_response = requests.get(url=base_url + 'Youtube/regionCode/' + str(region_id))
                        region_data = region_name_response.json()
                        region_name = region_data['data'][0][1]
                        region_name_list.append(region_name)
                    except:
                        pass
                cat_response = requests.get(url=base_url + 'Youtube/videoCategories/' + str(item['video_cat_id']))
                # print(cat_response.json())
                cat_json_data = cat_response.json()
                video_cat_name = cat_json_data['data'][0]['video_cat_name']
                item.update({'video_cat_name': video_cat_name})
                item.update({'region_name_list': region_name_list})
                try:
                    string_from_date = datetime.datetime.strptime(item['from_date'], '%Y-%m-%d')
                    string_from_date = string_from_date.strftime('%d-%b-%y')
                    string_to_date = datetime.datetime.strptime(item['to_date'], '%Y-%m-%d')
                    string_to_date = string_to_date.strftime('%d-%b-%y')
                    item.update({'from_date': string_from_date})
                    item.update({'to_date': string_to_date})
                except Exception as e:
                    print(e)
            print('classified details data', view_classfied_details)
            return view_classfied_details
        except Exception as e:
            print(e)
            pass
            return view_classfied_details
