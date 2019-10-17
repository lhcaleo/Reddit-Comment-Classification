import pandas as pd
import numpy as np
from sklearn import feature_extraction, preprocessing, tree
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer, TfidfVectorizer
import nltk
from nltk import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from string import punctuation
import re
nltk.download('punkt')

# Read in files
train = pd.read_csv("reddit_train.csv", sep=',')
test = pd.read_csv("reddit_test.csv", sep=',')

comments = train['comments']
test_x = test['comments']
labels = train['subreddits']

# Show first 5 rows of raw data

# # Remove URLs
# def remove_URLs(text):
#     text = re.sub(r"http\S+", " ", text)
#     return text
#
# # Set all words to lowercase
# def set_lowercase(text):
#     text = text.lower();
#     return text;
#
# # Remove tags
# def remove_tags(text):
#     text = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
#     return text
#
# # Remove special characters and digits
# def remove_special_chars_digits(text):
#     text = re.sub("(\\d|\\W)+"," ",text)
#     return text
#
# # Note: Order of remove operations matters!
# comments = comments.apply(lambda x: remove_URLs(x))
# comments = comments.apply(lambda x: set_lowercase(x))
# comments = comments.apply(lambda x: remove_tags(x))
# comments = comments.apply(lambda x: remove_special_chars_digits(x))
# print("----remove urls tags, set lowercase, remove specials characters and digits----\n", comments.head(5))
#
# # Tokenize comments
# comments = comments.apply(word_tokenize)
# print("----tokenized----\n", comments.head(12))
#
# # Lemmatize
# lemmatizer = nltk.WordNetLemmatizer()
# def lemmatize(text):
#     for row_i in range(comments.shape[0]):
#         for word_j in range(len(comments[row_i])):
#             comments[row_i][word_j] = lemmatizer.lemmatize(comments[row_i][word_j])
#     return text
# comments = lemmatize(comments)
# print("----lemmatized----\n", comments.head(12))
#
# # Remove Stopwords
# stop_words = set(stopwords.words('english'))
# comments = comments.apply(lambda x: [item for item in x if item not in stop_words])
# print("----removed stop words----\n", comments.head(5))
#
# # Repeat Replacer
# # http://www.ishenping.com/ArtInfo/971959.html
# class RepeatReplacer():
#     def __init__(self):
#         self.repeat_reg = re.compile(r'(\w*)(\w)\2(\w*)')
#         self.repl = r'\1\2\3'
#     def replace(self, word):
#         if wordnet.synsets(word):  # 判断当前字符串是否是单词
#             return word
#         repl_word = self.repeat_reg.sub(self.repl, word)
#         if repl_word != word:
#             return self.replace(repl_word)
#         else:
#             return repl_word
# replacer = RepeatReplacer()
# def remove_repeat(text):
#     for row_i in range(comments.shape[0]):
#         for word_j in range(len(comments[row_i])):
#             comments[row_i][word_j] = replacer.replace(comments[row_i][word_j])
#     return text
# comments = remove_repeat(comments)
# print("----removed repeat----\n", comments.head(5))


keywords = pd.read_csv("test_processed.csv")
keywords = keywords[keywords.columns[1]]
keywords = keywords.apply(word_tokenize)
print("keywords shape", len(keywords[0]))
labels=labels.iloc[0:1009].tolist()

#conclude comments into a [V] vocabulary vector
def getVocabularyVector ():

    vocabularyVector = keywords.to_numpy().reshape(-1)
    return vocabularyVector

#preprocess comments into a two-dimentional binary matrix based on the absence and presence of words in [V]
def preprocessComments (vocabV):
    documentM = keywords
    binaryM = np.zeros((documentM.shape[0],vocabV.shape[0]))
    for x in range(vocabV.shape[0]):
        for y in range(documentM.shape[0]):
            for z in range(len(documentM[y])):
                if(vocabV[x]==documentM[y][z]):
                    binaryM[y][z]=1
    return binaryM

def fit (vocabV):
    documM = keywords
    #total number of comments
    N=documM.shape[0]
    #count number of comments labelled with class K
    Karray = np.array([["hockey",0,[]],["nba",0,[]],["soccer",0,[]],["baseball",0,[]],["GlobalOffensive",0,[]],
                       ["canada",0,[]],["conspiracy",0,[]],["europe",0,[]],["anime",0,[]],["Overwatch",0,[]],
                       ["wow",0,[]],["nfl",0,[]],["leagueoflegends",0,[]],["trees",0,[]],["Music",0,[]],
                       ["AskReddit",0,[]],["worldnews",0,[]],["funny",0,[]],["gameofthrones",0,[]],["movies",0,[]]])
    for x in range(len(labels)):
        for y in range(Karray.shape[0]):
            if(labels[x]==Karray[y][0]):
                Karray[y][1]+=1
                Karray[y][2].append(documM[x])

    numberOfCommentsContainWordInClass=[[0]*vocabV.shape[0]]*Karray.shape[0]
    #count number of comments of class K containing word w
    for i in range(Karray.shape[0]):
        index=0
        for l in range(Karray[i][2].shape[0]):
            if(Karray[i][2][l][index]==1):
                numberOfCommentsContainWordInClass[i][l]+=1
        index+=1

    #compute the relative frequency of comments of class K
    totalNumberOfComments = N
    priors=[0]*Karray.shape[0]
    for p in range(Karray.shape[0]):
        priors[p]=Karray[p][1]/totalNumberOfComments

    #compute probabilities of each word given the comment class
    likelyhoods=[[0]*vocabV.shape[0]]*Karray.shape[0]
    for q in range(Karray.shape[0]):
        for s in range(vocabV.shape[0]):
            likelyhoods[q][s]=numberOfCommentsContainWordInClass[q][s]/Karray[q][1]

    result = [priors,likelyhoods]
    return result


#To classify an unlabelled comment in C_test,we estimate the posterior probability for each class K
def predict ():
    C_test = keywords
    Karray = np.array(
        ["hockey", "nba", "soccer", "baseball", "GlobalOffensive",
         "canada", "conspiracy", "europe", "anime", "Overwatch",
         "wow", "nfl", "leagueoflegends", "trees", "Music",
         "AskReddit", "worldnews", "funny", "gameofthrones", "movies"])
    vocVector=getVocabularyVector()
    docMatrix=preprocessComments(vocVector)
    priors = fit(vocVector)[0]
    likelyhoods = fit(vocVector)[1]
    for i in range(docMatrix.shape[0]):
        for j in range(docMatrix.shape[1]):
            if (docMatrix[i][j]==1):
                docMatrix[i][j]*likelyhoods[i][j]
            else:
                docMatrix[i][j]=1-likelyhoods[i][j]

    product=[1]*docMatrix.shape[0]
    for p in range(docMatrix.shape[0]):
        for q in range(docMatrix.shape[1]):
            product[p]=product[p]*docMatrix[p][q]

    #compute posterior probabilities for each comment based on 20 classes
    #the final prediction will be the max of all the posterior probabilities
    posProb = [[0]*priors.shape[0]]*product.shape[0]
    predictionArray=[0]*product.shape[0]
    for x in range(product.shape[0]):
        for y in range(priors.shape[0]):
            posProb[x][y]=product[x]*priors[y]
    for z in range(posProb.shape[0]):
        maximumProb = max(posProb[z])
        indexOfMaxima=posProb.index(maximumProb)
        predictionArray[z]=Karray[indexOfMaxima]

    return predictionArray

print(*predict(),sep="/n")
