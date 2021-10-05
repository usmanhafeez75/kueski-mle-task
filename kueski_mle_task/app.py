# coding: utf8
from flask import Flask, request, jsonify

from kueski_mle_task.core.pipeline import Pipeline


pipeline = Pipeline()
app = Flask(__name__)


@app.route('/get_features', methods=["POST"])
def get_features():
    user_ids = request.get_json(force=True)
    features_list = pipeline.get_features(user_ids)
    return jsonify(dict(zip(user_ids, features_list)))


@app.route('/predict', methods=['POST'])
def predict():

    user_ids = request.get_json(force=True)
    features_list = pipeline.get_features(user_ids)

    valid_user_ids = []
    valid_features_list = []
    invalid_user_ids = []
    for user_id, features in zip(user_ids, features_list):
        if features:
            valid_user_ids.append(user_id)
            valid_features_list.append(features)
        else:
            invalid_user_ids.append(user_id)

    predictions = pipeline.predict(valid_features_list)
    predictions = map(int, predictions)
    predictions = dict(zip(valid_user_ids, predictions))

    response = {'predictions': predictions, 'invalid_user_ids': invalid_user_ids}
    return jsonify(response)


if __name__ == "__main__":
    pipeline.prepare_for_serving()
    app.run(debug=True)
