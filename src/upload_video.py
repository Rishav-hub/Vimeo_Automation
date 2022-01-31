import vimeo
import os
import logging
from src.utils.upload_manager import VimeoManager
from src.utils.all_utils import read_yaml

vim = VimeoManager(secret_path="secrets/secret.yaml", config_path="config/config.yaml")


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
        self.video_path_list = self.config['video_path_list']
        self.client = vimeo.VimeoClient(token=self.tokens, key=self.keys, secret=self.sec)
        self.response = self.client.get("/me")


    def upload(self):
        self.create_folder_structure()
        self.upload_root_video()
        self.upload_sub_video()
   


    def create_folder_structure(self):
        vim.create_rootfolder(self.video_path)

        sub_folder_name = vim.return_sub_folder()
        print(sub_folder_name)
        root_uri = vim.return_parent_uri()
        for i in sub_folder_name:
            ancester_uri = vim.return_ancester_uri(i)
            if vim.folder_verification(i) == True and ancester_uri == root_uri:
                print('folder already exist test')
            else:
                vim.create_subfolder(i)
              
            
    def upload_root_video(self):
        parent_uri = vim.return_parent_uri()
        # print(root_uri)
        for i in os.listdir(self.video_path_list):
            if i.endswith(".mp4"):
                video_url = f"{self.video_path_list}/{i}"
                uri = self.client.upload(video_url, data={
                    'name': i,
                    'description': 'The description goes here.',
                    "privacy": { "view": "nobody"},
                    'folder_uri' : parent_uri
                    })
                print(f"{i} uploaded")
    



    def upload_sub_video(self):
        response = self.client.get("/me/folders")
        res = response.json()
        for i in os.listdir(self.video_path_list):
            if not i.endswith(".mp4"):
                sub_url = f"{self.video_path_list}/{i}"
                sub_contents = os.listdir(sub_url)
                for video in sub_contents:
                    if video.endswith(".mp4"):
                        video_url = f"{sub_url}/{video}"
                        sub_uri = vim.get_sub_uri(i)
                        uri = self.client.upload(video_url, data={
                                        'name': video,
                                        'description': 'The description goes here.',
                                        "privacy": { "view": "nobody"},
                                        'folder_uri' : sub_uri
                                        })
                        print(f"{video} uploaded")



        


    
