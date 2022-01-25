from src.upload_videos import VimeoUploader


vimeo_obj = VimeoUploader("secrets/secret.yaml", "config/config.yaml")
vimeo_obj.upload()