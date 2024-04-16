'''This class takes in a DNA sequence and outputs the ML model results'''

import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np
import kipoiseq

SEQUENCE_LENGTH = 393216
model_path = 'https://www.kaggle.com/models/deepmind/enformer/TensorFlow2/enformer/1'

class Enformer:

    def __init__(self):
        # load the model from the provided path on tensorflow hub
        self._model = hub.load(model_path).model

    # predict on a given sequence 
    def enform(self, sequence):
        return(self.predict_on_batch(self.one_hot_encode(sequence)))['human'][0]

    # helper functions to pre-process given sequence 
    def one_hot_encode(self, sequence):
        return kipoiseq.transforms.functional.one_hot_dna(sequence).astype(np.float32)
    
    def predict_on_batch(self, one_hot_seq):
        predictions = self._model.predict_on_batch(one_hot_seq[np.newaxis])
        return {k: v.numpy() for k, v in predictions.items()}