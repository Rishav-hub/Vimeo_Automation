# from all_utils import read_yaml, video_info, user_info, folder_info
import logging
import os
import vimeo
from glob import glob
import pandas as pd



def child_folder_list(folder_json_data):
    try:
        child_folder = []

        parent_folder = []
        folder_data = folder_json_data['data']

        for i in folder_data:
        #     print(i['name'])
            
            ancestor_path = i['metadata']['connections']
        #     print(ancestor_path)
            if 'parent_folder' in ancestor_path.keys():
                child_folder.append(i['name'])
            else:
                parent_folder.append(i['name'])

        return child_folder
    except Exception as e:
        logging.error(e)
        raise(e)

def folder_name_with_ID(folder_json_data):
    try:
        folder_name_ID = {}
        for i in folder_json_data['data']:
            
            folder_ID = i['uri'].split('/')[-1]
            folder_name_ID[folder_ID] = i['name']
        # folder_name_ID = dict((v,k) for k,v in folder_name_ID.items())
        return folder_name_ID
    except Exception as e:
        logging.error(e)
        raise(e)

def parent_folder_ID_func(folder_json_data):
    try:
        parent_folder_ID = {}

        folder_data = folder_json_data['data']

        for i in folder_data:
        #     print(i['name'])
            
            ancestor_path = i['metadata']['connections']['ancestor_path']

            if len(ancestor_path) == 1 :
                parent_folder_ID[i['uri'].split('/')[-1]] = ancestor_path[0]['uri'].split('/')[-1]
        
        return parent_folder_ID
    except Exception as e:
        logging.error(e)
        raise(e)
        