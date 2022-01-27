from src.upload_video import VimeoUploader
from src.embed_link import VimeoEmbed
from src.utils.all_utils import read_yaml
if __name__ == '__main__':
    uploader = VimeoUploader(secret_path="secrets/secret.yaml", config_path="config/config.yaml")
    embed_obj=VimeoEmbed("secrets/secret.yaml", "config/config.yaml")
    uploader.upload()


    USER_FOLDER_NAME = read_yaml('config/config.yaml')['video_path']

    embed_obj.get_embed(USER_FOLDER_NAME)