import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np
import kipoiseq

SEQUENCE_LENGTH = 393216
model_path = 'https://tfhub.dev/deepmind/enformer/1'

class Enformer:

    #making a class so that model reading is only performed once. 
    def __init__(self):
        self._model = hub.load(model_path).model

    def enform(self, sequence):
        return(self.predict_on_batch(self.one_hot_encode(sequence)))['human'][0]

    def one_hot_encode(self, sequence):
        return kipoiseq.transforms.functional.one_hot_dna(sequence).astype(np.float32)
    
    def predict_on_batch(self, one_hot_seq):
        predictions = self._model.predict_on_batch(one_hot_seq[np.newaxis])
        return {k: v.numpy() for k, v in predictions.items()}