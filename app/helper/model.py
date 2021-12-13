import pickle
import sklearn
from .preprocess import preprocess

def load_model(filename):
    """Load the pickle models from the disk"""
    with open(filename, 'rb') as file:
        pickle_model = pickle.load(file)
    return pickle_model

def text_to_tfidf(text, tf_idf, pca):
    """
    Convert text to tfidf format so models can predict it.

    parameter : text -> text will be predicted
                tf_idf -> tf_idf object loaded from tf_idf.pkl
                pca -> pca object loaded from pca.pkl
    """
    clean_text = preprocess(text)
    list2vec = tf_idf.transform([clean_text])
    pcalist2vec = pca.transform(list2vec.toarray())
    return pcalist2vec
