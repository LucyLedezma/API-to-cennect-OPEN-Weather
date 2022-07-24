
from typing import Dict, List
import json
import requests
import os
from multiprocessing import Process
from time import sleep

def get_weather(user_id : str,
                api_key : str,
                directory_result : str = "./result/",
                file_name_ids : str = "cities_ids.json") -> Dict:
    """
    Function that rise the process of the OpenWeather API request.
    Args:
        user_id (str) : the id for the request entered by the user, this must be unique
        api_key (str) : the KEY of OpenWeather API.
        directory_result (str) : directory where the json files are stored
        file_names_isd (str) : the file that contain the list of cities identification
    """
                
    ids_requests = [file_name for file_name in  os.listdir(directory_result)]
    print(ids_requests)
    if "{}.json".format(user_id) in ids_requests:
        return {"message": "the user ID already exists!"}
    else:
        with open(file_name_ids, "r") as f:
            list_ids = json.load(f)
        file_user = "{}{}.json".format(directory_result, user_id)
        with open(file_user, "w") as f:
            json.dump([], f)
        proc = Process(
            target=sub_process_weather,
            args=(list_ids, file_user, api_key))
        proc.start()
       
    return {"message": "Operation made succesfully!"}

def get_download_progress(id_user : str,
                         directory_result : str = "./result/",
                         file_name_ids : str = "cities_ids.json")-> Dict:
    """
    Function that return the download progress of the infornmation
    Args:
        id_user (str) : the user id of the corresponding request
        directory_result (str) : directory where the json files are stored
        file_names_isd (str) : the file that contain the list of cities identification
    """
    file_name = "{}{}.json".format(directory_result, id_user)
    dc_result = {}
    if os.path.exists(file_name):
        with open(file_name, "r") as f_user, \
            open (file_name_ids, "r") as f_ids:
            count_total = len(json.load(f_ids))
            count_rows_user = len(json.load(f_user))
        dc_result = {"total_progress":"{} %".format(
            round((count_rows_user/count_total)*100, 2))}
    else:
        dc_result = {"message": "The request {} does not exist!".format(id_user)}
    return dc_result

def sub_process_weather(list_ids : List, file_user : str, api_key : str):
    """
    Funcion that make the request to OpenWeather API and store
    the result  in a json file
    Args:
        list_ids (List) : the list of city_id.
        file_user (str) : the file name of the specific user that store the query result.
        api_key (str) : the KEY of OpenWeather API.
    """
    for id in list_ids:
        api_url = "https://api.openweathermap.org/data/2.5/weather?id={}&appid={}&units=metric".format(id, api_key)
        dc_weather = requests.get(api_url).json()
        dc_weather = {"city_id": id,
                      "temperature": dc_weather["main"]["temp"],
                      "humidity": dc_weather["main"]["humidity"]}
        sleep(1)
        # Read the file content
        with open(file_user, "r") as f:
            list_dc_weather = json.load(f)
        list_dc_weather.append(dc_weather)
        # Write the update content
        with open(file_user, "w") as f:
            json.dump(list_dc_weather, f, indent=4)
