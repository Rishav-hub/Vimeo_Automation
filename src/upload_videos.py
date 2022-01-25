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


def video_upload(secret_path, config_path):
    secrets = read_yaml(secret_path)
    config = read_yaml(config_path)

    #vimeo authentication
    vimeo_path = secrets["vimeo"]
    tokens = vimeo_path["token"]
    keys = vimeo_path["key"]
    sec = vimeo_path["secret"]

    #config setup
    video_path = config["video_path"]
    current_path = os.getcwd()

    uploader_path = os.path.join(current_path, video_path)
    try:
        client = vimeo.VimeoClient(token=tokens,key=keys, secret=sec)
        response = client.get("/me")
        # print(response.json())

        #uploading videos
        name_list = os.listdir(uploader_path)
        url_list = []

        for name in glob(uploader_path+"*.mp4"):
            url_list.append(name)
        
        # print(len(name_list))
        # print(url_list)

        for indx in range(len(name_list)):
            video_name = name_list[indx]
            video_url = url_list[indx]

            uri = client.upload(video_url, data={
            'name': video_name,
            'description': 'The description goes here.',
            "privacy": { "view": "nobody"}
            })

            logging.info('Your video URI is: %s' % (uri))
    
    except Exception as e:
        logging.error(e)
        print(e)

# video_upload("secrets/secret.yaml", "config/config.yaml")