from src.utils.all_utils import read_yaml
import logging
import os
import vimeo
from glob import glob


logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,
                    filemode="a")
class VimeoUploader:
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

        self.uploader_path = os.path.join(self.current_path, self.video_path + "/")
        self.client = vimeo.VimeoClient(token=self.tokens, key=self.keys, secret=self.sec)
        response = self.client.get("/me")
        # print(response.json())

    
    def varify_folder(self, folder_name):
        try:
            response = self.client.get("/me/folders")
            folder_response = response.json()

            folder_info = folder_response['data']

            folder_list = []
            for i in folder_info:
                folder_names = i['name']
                folder_list.append(folder_names)

            lower = (map(lambda x: x.lower(), folder_list))
            lower_folder_list = list(lower)

            # print(lower_folder_list)
            # print(folder_name.lower())

            floder_lower = folder_name.lower()

            if floder_lower in lower_folder_list:
                return True
            else:
                return False

        except Exception as e:
            logging.info(e)
            print(e)

    
    def get_uri(self, folder_name):
        response = self.client.get("/me/folders")
        folder_response = response.json()

        folder_info = folder_response['data']
        uri_list = []
        folder_list = []
        for i in folder_info:
            folder_names = i['name']
            uri_list.append(i['uri'])
            folder_list.append(folder_names)

        lower = (map(lambda x: x.lower(), folder_list))
        lower_folder_list = list(lower)
        
        folder_index = lower_folder_list.index(folder_name.lower())
        actual_uri = uri_list[folder_index]

        # print(uri_list)
        # print(lower_folder_list)

        # print(actual_uri)

        return actual_uri



    def upload(self):
        name_list = os.listdir(self.uploader_path)
        url_list = []

        for name in glob(self.uploader_path+"*.mp4"):
            url_list.append(name)
        
        print(len(name_list))
        print(url_list)

        varified = self.varify_folder(self.video_path)
        print(varified)
        
        try:
            if varified == True:
                logging.info("folder already exists")
                print("folder already exists")

                uri_folder = self.get_uri(self.video_path)

                for indx in range(len(name_list)):
                    video_name = name_list[indx]
                    video_url = url_list[indx]

                    uri = self.client.upload(video_url, data={
                    'name': video_name,
                    'description': 'The description goes here.',
                    "privacy": { "view": "nobody"},
                    'folder_uri' : uri_folder
                    })

                    logging.info('Your video URI is: %s' % (uri))
                    print('Your video URI is: %s' % (uri))

            else:
                logging.info("folder doesn't exists")
                print("folder doesn't exists")
                self.client.post("/me/projects", data ={'name': self.video_path})

                uri_folder = self.get_uri(self.video_path)

                for indx in range(len(name_list)):
                    video_name = name_list[indx]
                    video_url = url_list[indx]

                    uri = self.client.upload(video_url, data={
                    'name': video_name,
                    'description': 'The description goes here.',
                    "privacy": { "view": "nobody"},
                    'folder_uri' : uri_folder
                    })

                    logging.info('Your video URI is: %s' % (uri))
                    print('Your video URI is: %s' % (uri))

        except Exception as e:
            logging.info(e)
            print(e)

        