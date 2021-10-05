# kueski-mle-task
The repo contains the code to deploy a Machine Learning Model.

### 1. Project Setup
Clone the repository, cd to the project root directory and install the package and requirements using `pip install .`

### 2. Running the Project
Edit the [Configuration File](config/config.yaml) according to the requirements.
You may need to create `data` and `model` directories and place the raw data file in `data` directory <br>
Below are the commands to be used according to the requirement.
```
python kueski_mle_task/run.py --help
```
```
usage: run.py [-h] [--preprocess-data] [--train-model] [--load-model]
              [--generate-prediction] [--input-file INPUT_FILE]
              [--output-file OUTPUT_FILE] [--serve-model]

Credit Risk Model

optional arguments:
  -h, --help            show this help message and exit
  --preprocess-data     Processes Raw Data
  --train-model         Train Model
  --load-model          Load Model
  --generate-prediction
                        Generate Prediction
  --input-file INPUT_FILE
                        input csv file with data to be predicted
  --output-file OUTPUT_FILE
                        output csv file with status prediction
  --serve-model         Serve Model

```
**preprocess-data**: Generates features from the raw data and save them.<br>
**train-model**: Trains the model and save it<br>
**load-model**: Loads the model <br>
**generate_prediction**: Generates predictions for the computed features saved in a file and saves predictions<br>
**serve-model**: Serves the model and computed features through flask API

### 3. Running through Docker

Building Image
```
docker image build -t <image-name>:<tag> .
```
Running Image
```
docker run -p 5000:5000 -v <config-folder-path>:/app/config -v <data-folder-path>:/app/data -v <model-folder-path>:/app/model <image-name>:tag <command>
```

### 4. Running with docker-compose.yml
No need to setup environment or build image manually. Just run `docker-compose run task <desired-command>` to complete the desired task.

### 5. Hitting Endpoints
By running the `--serve-model` command either using python, Docker or docker-compose, the model will be become online for predictions as:
```
>>> import requests

>>> user_ids = [5009033, 5009034, 0]

>>> url = 'http://0.0.0.0:5000/get_features'

>>> requests.post(url, json=user_ids).json()
{'0': [], '5009033': [51.0, 0.0, 16.0, 129.5547329260326, 0.0], '5009034': [51.0, 0.0, 17.0, 123.41509324149632, 0.0]}

>>> url_predict = 'http://0.0.0.0:5000/predict'

>>> requests.post(url_predict, json=user_ids).json()
{'invalid_user_ids': [0], 'predictions': {'5009033': 0, '5009034': 0}}
```

**Note**: Real world ML projects are deployed separately for inference and training. Model for predictions are usually deployed on wsgi servers like gunicorn.