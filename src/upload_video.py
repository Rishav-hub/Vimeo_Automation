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
        self.client = vimeo.VimeoClient(token=self.tokens, key=self.keys, secret=self.sec)
        self.response = self.client.get("/me")

    def upload(self):
        self.create_folder_structure()
        self.upload_root_video()
        self.upload_sub_video()
   

    def return_roo_uri(self):
        root_uri = vim.get_uri(self.video_path)
        return root_uri

    def return_ancester_uri(self,folder_name):
        response = self.client.get("/me/folders")
        res = response.json()
        # print(res)
        for i in range(len(res['data'])):
            if len(res['data'][i]['metadata']['connections']['ancestor_path']) > 0:
     
                if res['data'][i]['metadata']['connections']['ancestor_path'][0]['name'] == self.video_path:
                    par_uri = res['data'][i]['metadata']['connections']['ancestor_path'][0]['uri']

                    return par_uri


    def create_folder_structure(self):
        vim.create_rootfolder(self.video_path)
        sub_folder_name = vim.return_sub_folder()
        print(sub_folder_name)

        uri_dict = {}
        root_uri = self.return_roo_uri()

        for i in sub_folder_name:
            
            ancester_uri = self.return_ancester_uri(i)
            if vim.folder_verification(i) == True and ancester_uri == root_uri:
                uri_dict[i] = vim.get_uri(i)
            else:
                vim.create_subfolder(i)
                uri_dict[i] = vim.get_uri(i)
        print(uri_dict)
        return uri_dict
   
    
    def upload_root_video(self):
        root_uri = self.return_roo_uri()
        print(root_uri)
        for i in os.listdir(self.uploader_path):
            if i.endswith(".mp4"):
                video_url = f"{self.uploader_path}/{i}"
                uri = self.client.upload(video_url, data={
                    'name': i,
                    'description': 'The description goes here.',
                    "privacy": { "view": "nobody"},
                    'folder_uri' : root_uri
                    })
                print(f"{i} uploaded")
    

    def upload_sub_video(self):
        for i in os.listdir(self.uploader_path):
            if not i.endswith(".mp4"):
                sub_url = f"{self.uploader_path}/{i}"
                sub_contents = os.listdir(sub_url)
                for video in sub_contents:
                    if video.endswith(".mp4"):
                        video_url = f"{sub_url}/{video}"
                        uri = self.client.upload(video_url, data={
                            'name': video,
                            'description': 'The description goes here.',
                            "privacy": { "view": "nobody"},
                            'folder_uri' : vim.get_uri(i)
                            })
                        print(f"{video} uploaded")

       


    
