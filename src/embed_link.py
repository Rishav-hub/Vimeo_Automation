from src.utils.all_utils import read_yaml, video_info, user_info, folder_info
from src.utils.embed_utils import child_folder_list, folder_name_with_ID, parent_folder_ID_func
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
    def check_folder(self, folder_name):
        try:
            folder_json_data = folder_info(self.client)
            folder_list = []

            for folder in folder_json_data["data"]:
                folder_list.append(folder["name"])

            lower = (map(lambda x: x.lower(), folder_list))
            lower_folder_list = list(lower)

            if folder_name.lower() in lower_folder_list:
                logging.info(f"{folder_name} folder found")
                return True
            else:
                logging.info(f"{folder_name} folder NOT found")

                return False    
        except Exception as e:
            logging.error(e)
            raise(e)
    
    def get_embed(self, USER_FOLDER_NAME):
        b = self.check_folder(USER_FOLDER_NAME.lower())
        embedded_link_list = []
        video_name = []

        root_folder_name = []

        sub_folder_name = []

        try:
            if b:
                video_json_data = video_info(self.client)
                folder_json_data = folder_info(self.client)

                data_list = video_json_data["data"]

                for i in data_list:
                    if i['parent_folder']:
                        # print(i['parent_folder']['name'])
                        iframe = i['embed']['html']
                        embedded_link_list.append(iframe.split(' ')[1][5:-2])
                        video_name.append(i['name'])
                        if i['parent_folder']['name'] in child_folder_list(folder_json_data):
                            folder_name_ID = folder_name_with_ID(folder_json_data)
                            parent_folder_ID = parent_folder_ID_func(folder_json_data)
                            name = folder_name_ID[i['parent_folder']['uri'].split('/')[-1]]
                            sub_folder_name.append(name)
                            root_folder_name.append(folder_name_ID[parent_folder_ID[i['parent_folder']['uri'].split('/')[-1]]])
                        else:
                            name = folder_name_ID[i['parent_folder']['uri'].split('/')[-1]]
                            root_folder_name.append(name)
                            sub_folder_name.append('None')

                data = {'Video_Name': video_name, 'Link': embedded_link_list, 'ROOT_Folder_Name' :root_folder_name,'SUB_Folder_Name' : sub_folder_name}
                df = pd.DataFrame(data)
                df = df.where(df['ROOT_Folder_Name'] == USER_FOLDER_NAME).dropna()

                os.makedirs('artifacts', exist_ok=True)
                excel_path = os.path.join('artifacts', f"{USER_FOLDER_NAME}.xlsx")
                df.to_excel(excel_path, index=False)
                logging.info(f"{USER_FOLDER_NAME} folder embed links saved to {excel_path}")
        except Exception as e:
            logging.error(e)
            raise(e)


        


