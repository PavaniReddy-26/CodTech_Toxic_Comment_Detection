<p align="center">
  <img width="621" alt="logo" src="https://user-images.githubusercontent.com/76659596/105877123-eb112280-5fff-11eb-9425-8432e693f92e.png">
</p>



<p align="center">
  <img width="721" alt="web-app-screencast" src="https://user-images.githubusercontent.com/76659596/108608735-37663d00-73c9-11eb-8e6e-304dd535f527.gif">
</p>

## Motivation

People tend to discuss or share opinions on social platforms but such activities sometimes encounter threats or harassments which compel people to not express themselves properly.

Many social platforms try to find out such harassments or threats in conversations so that such conversations can easily be prevented before it causes any further damage.

Toxicity detection in comments is one of such methodologies to find out the different types of conversations that can be classified as toxic in nature.

To increase the efficacy in classifying such comments, we can make use of machine learning algorithms to determine the toxicity in comments. 

In this model, many toxic comments have been fed to build a `Bidirectional Long Short-Term Memory (LSTM) Recurrent Neural Network (RNN)` model for fulfilling the purpose.

## Requirements

- Python 3.7.0+
- Tensorflow 2.4.1+
- Keras 2.4.3+
- matplotlib 3.3.3+
- numpy 1.19.5+
- pandas 1.2.1+
- scikit-learn 0.24.1+ 
- nltk 3.5+
- spacy 3.0.3+
- textblob 0.15.3+
- Flask 2.0.0+

## Dataset

You can downloaded the dataset from [kaggle](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge). Use the underlying download link to download the dataset.

### Instructions

* Navigate to `data` section
* In the `Data Explorer`, you will find four separate zip archives to download
* Download `test.csv.zip`, `test_labels.csv.zip` and `train.csv.zip`
* Extract the files
* Copy the CSV files to the `data` directory

The following list enumerates different classes (types) of comments -

| Toxic | Very Toxic | Obscene | Threat | Insult | Hate | Neutral |
|-------|------------|---------|--------|--------|------|---------|


## Installation

* Install the required libraries

`pip3 install -r requirements.txt`

## Model Ideology

* `Clean text`: 
    * Lower all text
    * Remove uncommon signs
    * Expand abbreviations
    * Correct misspelled words
    * Remove punctuations
    * Remove emojis
    * Remove stop words
    * Apply lemmatisation
* `Tokenize text` data
* Create `Embedding Vector` using [Glove.6B](https://nlp.stanford.edu/projects/glove/)
* Train a `Recurrent Neural Network (RNN)` with a `Bidirectional LSTM` layer

## Usage

Navigate to the `source` directory to execute the following source codes.

* To generate the model on your own, run

`python3 model_training.py`

* You can also provide your own CSV data:

`python3 model_training.py --data=csv_file_location`

* To evaluate any dataset using the pre-trained model (in the `model` directory), run

`python3 model_evaluation.py`

Note that, for evaluation, `model_evaluation.py` will use the `test.csv` and `test_labels.csv` (inside `data` directory).

Alternatively, you can find the whole analysis in the notebook inside the `notebook` directory. To open the notebook, use either `jupyter notebook` or `google colab` or any other IDE that supports notebook feature such as `PyCharm Professional`.

## Web Application

To run the web application locally, go to the `webapp` directory and execute:

`python3 app.py`

This starts a local Flask server (by default at `http://127.0.0.1:5000`). Open that address in your browser, type or paste in any comment, and the model will break down its toxicity across all seven categories.


This project is licensed under Apache License Version 2.0

##########################################################################################
py -3.11 -m venv venv311
venv311\Scripts\activate
python -m pip install flask nltk numpy pandas matplotlib scikit-learn spacy textblob tensorflow keras
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
python -c "import flask,nltk,tensorflow,keras,spacy; print('ENVIRONMENT READY')"
python -m pip install keras-preprocessing
python -c "import keras_preprocessing; print('keras_preprocessing OK')"
python app.py
#############################################################################################