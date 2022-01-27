from src.utils.all_utils import read_yaml
import logging
import os
import vimeo
from glob import glob
import argparse



logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,
                    filemode="a")


class VimeoManager:
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
        # print(response.json())


    def folder_verification(self,folder_name):
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


    
    def get_uri(self,folder_name):
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

    #     print(uri_list)
    #     print(lower_folder_list)

    #     print(actual_uri)

        return actual_uri


    
    def create_rootfolder(self,folder_name):
        varified = self.folder_verification(folder_name)
        print(varified)
        
        
        if varified == True:
            print("root folder already exists")
            uri_folder = self.get_uri(folder_name)   
#             print(uri_folder)
            return uri_folder

        else:
            print("root folder doesn't exists")
            self.client.post("/me/projects", data ={'name': folder_name})

            uri_folder = self.get_uri(folder_name)
            
            return uri_folder


    def create_subfolder(self,folder_name):
 
        varified = self.folder_verification(folder_name)
        print(varified)

        root_uri = self.return_roo_uri()
        ancestor_uri = self.return_ancester_uri(folder_name)
    
        if varified == True and root_uri == ancestor_uri:
            print("sub folder already exists")
            uri_folder = self.get_uri(folder_name)   
    #             print(uri_folder)
            return uri_folder

        else:
            print("sub folder doesn't exists")
            parent_folder_uri = self.create_rootfolder(self.video_path)
            print(parent_folder_uri)
            response = self.client.post("/me/projects", data ={'name': folder_name, 'parent_folder_uri' : parent_folder_uri})


            uri_folder = self.get_uri(folder_name)

            return uri_folder


    def return_roo_uri(self):
        root_uri = self.get_uri(self.video_path)
        return root_uri

    # def return_ancester_uri(self,folder_name):
    #     response = self.client.get("/me/folders")
    #     res = response.json()
    #     # print(res)
    #     for i in range(len(res['data'])):
    #         if len(res['data'][i]['metadata']['connections']['ancestor_path']) > 0:
              
    #             if res['data'][i]['metadata']['connections']['ancestor_path'][0]['name'] == self.video_path:
    #                 par_uri = res['data'][i]['metadata']['connections']['ancestor_path'][0]['uri']

    #                 return par_uri
    #         break

    def return_ancester_uri(self,folder_name):
        response = self.client.get("/me/folders")
        res = response.json()
        for n in range(len(res['data'])):
            if res['data'][n]['name'] == folder_name:
                if res['data'][n]['metadata']['connections']['ancestor_path'][0]['name'] == self.video_path:
                    par_uri = res['data'][n]['metadata']['connections']['ancestor_path'][0]['uri']

                    return par_uri

   


    def return_sub_folder(self):
        sub_folder_list = []
        for i in os.listdir(self.video_path):
            if not i.endswith('.mp4'):
                sub_folder_list.append(i)
    #     print(sub_folder_list)
        return sub_folder_list


# if __name__ == '__main__':
#     args = argparse.ArgumentParser()

#     args.add_argument("--config", "-c", default="config/config.yaml")
#     args.add_argument("--secret", "-s", default="secrets/secret.yaml")

#     parsed_args = args.parse_args()

#     try:
#         VimeoManager(secret_path=parsed_args.secret, config_path=parsed_args.config)
#         logging.info("Uploader manager is running")
#     except Exception as e:
#         logging.exception(e)
#         raise e