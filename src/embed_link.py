from src.utils.all_utils import read_yaml
from src.utils.embed_utils import extract_uri_id_link, folder_items_response, videos_response
import logging
import os
import vimeo
from glob import glob
import pandas as pd


logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,
                    filemode="a")


class VimeoEmbed:
    def __init__(self, secret_path, config_path):
        self.secrets = read_yaml(secret_path)
        self.config = read_yaml(config_path)

        # vimeo authentication
        self.vimeo_path = self.secrets["vimeo"]
        self.tokens = self.vimeo_path["token"]
        self.keys = self.vimeo_path["key"]
        self.sec = self.vimeo_path["secret"]

        # config setup
        self.video_path = self.config["video_path"]
        self.current_path = os.getcwd()

        self.uploader_path = os.path.join(self.current_path, self.video_path)
        self.client = vimeo.VimeoClient(token=self.tokens, key=self.keys, secret=self.sec)
    
    def level_0_embed_link(self, link):
        try:
            logging.info('>>>>>>>Level 0 Process Started')
            
            uri_id = extract_uri_id_link(link)
            video_response_data_list = videos_response(self.client, uri_id)
            
            response = self.client.get(f"/users/127902260/folders/{uri_id}")
            folder_name = response.json()['name']
            
            embedded_link_list = []
            video_name_list = []
            root_folder_name = []
            for video_data in video_response_data_list:
                for i in video_data:
                    video_name_list.append(i['name'])
                    embedded_link_list.append(i['player_embed_url'])
                    root_folder_name.append(folder_name)
            data = {'Root Folder': root_folder_name,'Lesson Title': video_name_list, 'Lesson URL': embedded_link_list}
            df = pd.DataFrame(data)
            os.makedirs('artifacts/level_0', exist_ok= True)
            df.to_excel(f'artifacts/level_0/{folder_name}.xlsx', index= False)
            logging.info('Level 0 Process Completed >>>>>>')
        except Exception as e:
            logging.info(e)
            raise e
    
    def level_1_embed_link(self, link):
        try: 
            uri_id = extract_uri_id_link(link)
            folder_response_data_list = folder_items_response(self.client, uri_id)
            
            response = self.client.get(f"/users/127902260/folders/{uri_id}")
            folder_name = response.json()['name']
            
            embedded_link_list = []
            video_name_list = []
            parent_folder_list = []
            subfolder_uri_id_list = []
            root_folder_name = []
            for folder_data in folder_items_response(self.client, uri_id):
                for i in folder_data:
                    subfolder_uri_id_list.append(extract_uri_id_link(i['folder']['uri']))

            for ids in subfolder_uri_id_list:
                for video_data in videos_response(self.client, ids):
                    for i in video_data:
                        video_name_list.append(i['name'])
                        embedded_link_list.append(i['player_embed_url'])
                        parent_folder_list.append(i['parent_folder']['name'])
                        root_folder_name.append(folder_name)
                        
            data = {'Root Folder': root_folder_name, 'Section Name': parent_folder_list, 'Lesson Title': video_name_list,'Lesson URL': embedded_link_list}
            df = pd.DataFrame(data)
            os.makedirs('artifacts/level_1', exist_ok= True)
            df.to_excel(f'artifacts/level_1/{folder_name}.xlsx', index= False)
        except Exception as e:
            logging.error(e)
            raise e
                
    def level_2_embed_link(self, link):
        try: 
            uri_id = extract_uri_id_link(link)
            
            response = self.client.get(f"/users/127902260/folders/{uri_id}")
            folder_name = response.json()['name']
            
            sub_subfolder_uri_id_list = []
            video_name_list = []
            embedded_link_list = []
            parent_folder_list = []
            root_folder_name = []
            subject_name_list = []
            for folder_data in folder_items_response(self.client, '7658377'):
                for i in folder_data:
            #         print(i['folder']['name'])
                    sub_subfolder_uri_id_list.append(extract_uri_id_link(i['folder']['uri']))
            subfolder_uri_id_list = []
            for ids in sub_subfolder_uri_id_list:
                for folder_data in folder_items_response(self.client, ids):
                    for i in folder_data:
                        subfolder_uri_id_list.append(extract_uri_id_link(i['folder']['uri']))

            for ids in subfolder_uri_id_list:
                for video_data in videos_response(self.client, ids):
                    for i in video_data:
                        video_name_list.append(i['name'])
                        embedded_link_list.append(i['player_embed_url'])
                        parent_folder_list.append(i['parent_folder']['name'])
                        root_folder_name.append(folder_name)
                        
            data = {'Root Folder': root_folder_name, 'Subject Name': subject_name_list,'Section Name': parent_folder_list, 'Lesson Title': video_name_list,'Lesson URL': embedded_link_list}
            df = pd.DataFrame(data)
            os.makedirs('artifacts/level_2', exist_ok= True)
            df.to_excel(f'artifacts/level_2/{folder_name}.xlsx', index= False)
        except Exception as e:
            logging.error(e)
            raise e
