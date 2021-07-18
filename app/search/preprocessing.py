import nltk
import re
from nltk.corpus import stopwords
TEXT_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"

stop_words = stopwords.words("english")

def preprocess(text, stopword=False):
    
    text = re.sub(TEXT_CLEANING_RE, ' ', str(text).lower()).strip()
    if stopword :
        tokens = []
        for token in text.split():
            if token not in stop_words:
                tokens.append(token)
        return " ".join(tokens)
    else :
        return text