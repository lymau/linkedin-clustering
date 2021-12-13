import string, re, nltk
from nltk.stem import WordNetLemmatizer

def remove_brackets(text):
    """Remove brackets from text"""
    res = str(text)[1:-1]
    return res

def remove_punctuation_with_whitespace(text):
    """Remove punctuation with whitespace"""
    punctuationfree = " ".join([i for i in text if i not in string.punctuation])
    return punctuationfree

def remove_punctuation(text):
    """Remove the punctuations from given text"""
    punctuationsFree = "".join([i for i in text if i not in string.punctuation])
    return punctuationsFree

def remove_number(text):
    """Remove the number from given text"""
    numberfree = "".join([i for i in text if re.sub(r"\d+","",i)])
    return numberfree

def character_encoding(text):
    """Remove the unwanted character encoding from given text"""
    characterencoding = "".join([c for c in text if 0 < ord(c) < 127])
    return characterencoding

def remove_urls(text):
    """Remove urls from given text"""
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

def tokenization(text):
    """Tokenizes text by word_tokenize method"""
    tokens = nltk.word_tokenize(text)
    return tokens

def remove_stopwords(text):
    """Remove stopwords from given text"""
    stopwords = nltk.corpus.stopwords.words('english')
    output= [i for i in text if i not in stopwords]
    return output

def lemmatizer(text):
    """Lemmatize the text"""
    wordnet_lemmatizer = WordNetLemmatizer()
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
    return lemm_text

def preprocess(text):
    """Wrapper for all preprocessing functions"""
    clean_text = remove_punctuation(text)
    clean_text = remove_number(clean_text)
    clean_text = character_encoding(clean_text)
    clean_text = remove_urls(clean_text)
    clean_text = tokenization(clean_text)
    clean_text = remove_punctuation_with_whitespace(clean_text)
    return clean_text


