import yaml 
import logging
import os


def read_yaml(self,path_to_yaml: str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    logging.info(f"yaml file: {path_to_yaml} loaded successfully")
    return content


def user_info(clint):
    response = clint.get("/me")
    return response.json()
   

