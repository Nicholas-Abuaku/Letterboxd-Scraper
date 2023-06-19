import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from PyQt6.QtCore import QThread, pyqtSignal
from scipy.special import softmax

class sentimentAnalyser(QThread):
    analysisComplete = pyqtSignal()
    def __init__(self, file):
        MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        self.file = file
        self.df = pd.read_csv(file)
    
    def polarity_scores_roberta(self, example):
        encoded_text = self.tokenizer.encode_plus(
            example,
            add_special_tokens=True,
            return_tensors="pt"
        )
        output = self.model(**encoded_text)
        scores = output.logits[0].detach().numpy()
        scores = softmax(scores)
        scores_dict = {
            'Negative': scores[0],
            'Neutral': scores[1],
            'Positive': scores[2]
        }
        return scores_dict
    
