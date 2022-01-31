from src.utils.all_utils import read_yaml
import logging
import os
import vimeo


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
        self.ROOT_FOLDER_NAME = self.config["ROOT_FOLDER_NAME"]
        self.current_path = os.getcwd()

        self.uploader_path = os.path.join(self.current_path, self.video_path + "/")
        self.video_path_list = self.config['video_path_list']
        self.client = vimeo.VimeoClient(token=self.tokens, key=self.keys, secret=self.sec)
        self.response = self.client.get("/me")
        # print(response.json())


    def return_all_page_data(self):
        response = self.client.get(f"/users/127902260/folders?page=1")
        folder_response = response.json()
        starting_page = int(folder_response['paging']['first'].split('=')[-1])
        last_page = int(folder_response['paging']['last'].split('=')[-1])

        folder_response_list = []

        for i in range(starting_page, last_page + 1):
            response = self.client.get(f"/users/127902260/folders?page={i}")
            folder_response = response.json()
            folder_response_list.append(folder_response['data'])

        return folder_response_list



    def folder_verification(self,folder_name):
        
        folder_response_list = self.return_all_page_data()
       
        folder_list = []
        for i in folder_response_list:
            list_of_data = i
            for j in list_of_data:
                folder_list.append(j['name'])

        lower = (map(lambda x: x.lower(), folder_list))
        lower_folder_list = list(lower)

        # print(lower_folder_list)
        # print(folder_name.lower())

        floder_lower = folder_name.lower()

        if floder_lower in lower_folder_list:
            return True
        else:
            return False


    
    def get_sub_uri(self,folder_name):
        folder_response_list = self.return_all_page_data()
        for i in folder_response_list:
            list_of_data = i
            for j in list_of_data:
                if j['name'] == folder_name:
                    if (j['metadata']['connections']['ancestor_path'][0]['name'] == self.video_path) and (j['metadata']['connections']['ancestor_path'][1]['name'] == self.ROOT_FOLDER_NAME):
                        print(f"This is the uri {j['uri']} of the folder {folder_name}")
                        return j['uri']


                
                
    
    def root_folder_uri(self):
        folder_response_list = self.return_all_page_data()
        for i in folder_response_list:
            list_of_data = i
            for j in list_of_data:
                if j['name'] == self.ROOT_FOLDER_NAME:
                    print(f'Retuned root folder uri: {j["uri"]}')
                    return j['uri']

    
    def verify_parent_folder(self):
        folder_response_list = self.return_all_page_data()
        for i in folder_response_list:
            list_of_data = i
            for j in list_of_data:
                if j['name'] == self.video_path:
                    if j['metadata']['connections']['ancestor_path'][0]['name'] == self.ROOT_FOLDER_NAME:
                        return True
                    else:
                        return False

    
    def create_rootfolder(self,folder_name):
        varified = self.folder_verification(folder_name)
        print(varified)
        
        
        if (varified == True):
            print("root folder already exists")


        else:
            print("root folder doesn't exists")
            ROOT_FOLDER_URI = self.root_folder_uri()
            self.client.post("/me/projects", data ={'name': folder_name, 'parent_folder_uri' : ROOT_FOLDER_URI})
            print('root folder created')



    def create_subfolder(self,folder_name):
 
        varified = self.folder_verification(folder_name)
        print(varified)

        root_uri = self.return_parent_uri()
        ancestor_uri = self.return_ancester_uri(folder_name)
    
        if (varified == True) and (root_uri == ancestor_uri):
            print("sub folder already exists")

        else:
            print("sub folder doesn't exists")
            parent_folder_uri = self.return_parent_uri()
            response = self.client.post("/me/projects", data ={'name': folder_name, 'parent_folder_uri' : parent_folder_uri})
            print('sub folder created')



    def return_parent_uri(self):
        folder_response_list = self.return_all_page_data()
        for i in folder_response_list:
            list_of_data = i
            for j in list_of_data:
                if j['name'] == self.video_path:
                    if j['metadata']['connections']['ancestor_path'][0]['name'] == self.ROOT_FOLDER_NAME:
                        print(f"This is the uri {j['uri']} of the parent {self.video_path}")
                        return j['uri']

   

    def return_ancester_uri(self,folder_name):
        folder_response_list = self.return_all_page_data()
        for i in folder_response_list:
            list_of_data = i
            for j in list_of_data:
                if j['name'] == folder_name:
                    if (j['metadata']['connections']['ancestor_path'][0]['name'] == self.video_path) and (j['metadata']['connections']['ancestor_path'][1]['name'] == self.ROOT_FOLDER_NAME):
                        print("Ansester True")
                        return j['metadata']['connections']['parent_folder']['uri']

   


    def return_sub_folder(self):
        sub_folder_list = []
        for i in os.listdir(self.video_path_list):
            if not i.endswith('.mp4'):
                sub_folder_list.append(i)
    #     print(sub_folder_list)
        return sub_folder_list


