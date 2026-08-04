__author__ = "Baishali Dutta"
__copyright__ = "Copyright (C) 2022 Baishali Dutta"
__license__ = "Apache License 2.0"
__version__ = "0.2"

# -------------------------------------------------------------------------
#                           Import Libraries
# -------------------------------------------------------------------------
import pickle
import sys
import os
from keras.layers import LSTM

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

from source.config import *
from source.data_cleaning import clean_text

# -------------------------------------------------------------------------
#                     Load Existing Model and Tokenizer
# -------------------------------------------------------------------------

app = Flask(__name__)

# load the trained model
rnn_model = load_model(
    MODEL_LOC,
    custom_objects={"LSTM": LSTM},
    compile=False
)

# load the tokenizer
with open(TOKENIZER_LOC, 'rb') as handle:
    tokenizer = pickle.load(handle)

# -------------------------------------------------------------------------
#                       Category Metadata (for UI)
# -------------------------------------------------------------------------
CATEGORY_META = [
    {"key": "toxic", "label": "Toxic", "tier": "mid"},
    {"key": "severe_toxic", "label": "Severe Toxic", "tier": "high"},
    {"key": "obscene", "label": "Obscene", "tier": "mid"},
    {"key": "threat", "label": "Threat", "tier": "high"},
    {"key": "insult", "label": "Insult", "tier": "mid"},
    {"key": "hate", "label": "Hate", "tier": "high"},
    {"key": "neutral", "label": "Neutral", "tier": "safe"},
]


# -------------------------------------------------------------------------
#                           Prediction Logic
# -------------------------------------------------------------------------
def make_prediction(input_comment):
    """
    Predicts the toxicity of the specified comment
    :param input_comment: the comment to be verified
    :return: a list of dicts with key, label, tier and score for each category
    """
    cleaned = clean_text(input_comment)
    cleaned = cleaned.split(" ")

    sequences = tokenizer.texts_to_sequences(cleaned)
    sequences = [[item for sublist in sequences for item in sublist]]

    padded_data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    result = rnn_model.predict(padded_data, len(padded_data), verbose=0)

    scores = []
    for i, meta in enumerate(CATEGORY_META):
        scores.append({
            "key": meta["key"],
            "label": meta["label"],
            "tier": meta["tier"],
            "score": round(float(result[0][i]) * 100, 2)
        })
    return scores


# -------------------------------------------------------------------------
#                              Routes
# -------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    comment = (data.get("comment") or "").strip()

    if not comment:
        return jsonify({"error": "Please enter a comment to analyze."}), 400

    scores = make_prediction(comment)
    return jsonify({"results": scores})


if __name__ == "__main__":
    app.run(debug=True)
