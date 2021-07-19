import nltk
import re
from nltk.corpus import stopwords
from  nltk.stem import SnowballStemmer
TEXT_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"

stop_words = stopwords.words("english")
stemmer = SnowballStemmer("english")

def preprocess(text, stem=False):
            
            text = re.sub(TEXT_CLEANING_RE, ' ', str(text).lower()).strip()
            tokens = []
            for token in text.split():
                if token not in stop_words:
                    if stem:
                        tokens.append(stemmer.stem(token))
                    else:
                        tokens.append(token)
            return " ".join(tokens)
