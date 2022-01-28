'''
author:    1.Bappy Ahmed
            2.Rishav Dash

Email:   entbappy73@gmail.com
         ris.das.rt18@rait.ac.in

Date: 25 January 2022

'''

from src.upload_video import VimeoUploader
from src.embed_link import VimeoEmbed
from src.utils.all_utils import read_yaml
from flask import Flask, render_template,request,jsonify
from flask_cors import CORS, cross_origin
import yaml
import webbrowser
from threading import Timer

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET'])
@cross_origin()
def upload():
    return render_template('upload.html')

@app.route('/upload_engine', methods=['POST', 'GET'])
@cross_origin()
def upload_engine():
    config = read_yaml("config/config.yaml")
    secrets = read_yaml("secrets/secret.yaml")

    if request.method == 'POST':
        try:
            # Inputs based to data
            folder_name = request.form['folder_name']
            token = request.form['token']
            key = request.form['key']
            secret = request.form['secret']
           
            print('Dumping Yaml')
            
            #config
            config['video_path'] = folder_name

            #secrets
            secrets['vimeo']['token'] = token
            secrets['vimeo']['key'] = key
            secrets['vimeo']['secret'] = secret
           

            with open('config/config.yaml', 'w') as file:
                yaml.dump(config, file)

            with open('secrets/secret.yaml', 'w') as file:
                yaml.dump(secrets, file)
                
            
            uploader.upload()

            return render_template('upload.html')
 
        except Exception as e:
            print("Input format not proper", end= '')
            print(e)
    else:
        return render_template('upload.html')

@app.route('/embed', methods=['GET'])
@cross_origin()
def embed():
    return render_template('embed.html')

@app.route('/embed_engine', methods=['POST', 'GET'])
@cross_origin()
def embed_engine():
    config = read_yaml("config/config.yaml")
    secrets = read_yaml("secrets/secret.yaml")

    if request.method == 'POST':
        try:
            # Inputs based to data
            folder_name = request.form['folder_name']
            token = request.form['token']
            key = request.form['key']
            secret = request.form['secret']
           
            print('Dumping Yaml')
            
            #config
            config['video_path'] = folder_name

            #secrets
            secrets['vimeo']['token'] = token
            secrets['vimeo']['key'] = key
            secrets['vimeo']['secret'] = secret
           

            with open('config/config.yaml', 'w') as file:
                yaml.dump(config, file)

            with open('secrets/secret.yaml', 'w') as file:
                yaml.dump(secrets, file)
                
            USER_FOLDER_NAME = read_yaml('config/config.yaml')['video_path']
            
            embed_obj.get_embed(USER_FOLDER_NAME)

            return render_template('embed.html')
 
        except Exception as e:
            print("Input format not proper", end= '')
            print(e)
    else:
        return render_template('embed.html')
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8080/')


def start_app():
    Timer(1, open_browser).start()
    app.run(host="127.0.0.1", port=8080,debug=True)

if __name__ == '__main__':
    uploader = VimeoUploader(secret_path="secrets/secret.yaml", config_path="config/config.yaml")
    embed_obj=VimeoEmbed("secrets/secret.yaml", "config/config.yaml")
   
    # USER_FOLDER_NAME = read_yaml('config/config.yaml')['video_path']

    start_app()



