from src.upload_video import VimeoUploader

if __name__ == '__main__':
    uploader = VimeoUploader(secret_path="secrets/secret.yaml", config_path="config/config.yaml")
    uploader.upload()
