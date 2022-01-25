# from src.upload_videos import VimeoEmbed
from src.embed_link import VimeoEmbed


# video_upload("secrets/secret.yaml", "config/config.yaml")

embed_obj=VimeoEmbed("secrets/secret.yaml", "config/config.yaml")

embed_obj.get_embed("big_data")
