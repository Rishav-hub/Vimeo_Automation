# from src.upload_videos import VimeoEmbed
from gevent import config
from src.embed_link import VimeoEmbed
from src.utils.all_utils import read_yaml

# video_upload("secrets/secret.yaml", "config/config.yaml")

embed_obj=VimeoEmbed("secrets/secret.yaml", "config/config.yaml")

config_path = "config/config.yaml"
config_data = read_yaml(config_path)

params_path = config_data['params_path']

USER_FOLDER_NAME = read_yaml(params_path)['USER_FOLDER_NAME']

embed_obj.get_embed(USER_FOLDER_NAME)
