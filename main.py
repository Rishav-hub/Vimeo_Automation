from src.upload_video import VimeoUploader
from flask import Flask, render_template,request,jsonify
from flask_cors import CORS, cross_origin
import webbrowser
from threading import Timer
from src.utils.all_utils import read_yaml
import yaml


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
  
    if request.method == 'POST':
        try:
            # Inputs based to data
            level = request.form['level']
            root = request.form['root']
            folder_name = request.form['folder_name']
            v_path = request.form['v_path']
           
            print('Dumping Yaml')
            
            #config
            config['video_path'] = folder_name
            config['ROOT_FOLDER_NAME'] = root
            config['level'] = level
            config['video_path_list'] = v_path

     
            with open('config/config.yaml', 'w') as file:
                yaml.dump(config, file)
            

            if level == 'level0':
                uploader.upload()
                print('level0')

            else:
                print("level1")

            return render_template('index.html')
 
        except Exception as e:
            print("Input format not proper", end= '')
            print(e)
    else:
        return render_template('index.html')



def open_browser():
    webbrowser.open_new('http://127.0.0.1:8080/')


def start_app():
    Timer(1, open_browser).start()
    app.run(host="127.0.0.1", port=8080,debug=True)



if __name__ == '__main__':
    uploader = VimeoUploader(secret_path="secrets/secret.yaml", config_path="config/config.yaml")
    # uploader.upload()
    start_app()
