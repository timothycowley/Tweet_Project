import pandas as pd
import numpy as np
import os
import sys
import csv
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
import tweetToken

PROJECT_DIR = '/home/timothy/Desktop/Public/AI/Data Mining class/Project/'
TWEET_DIR = PROJECT_DIR + "tweets"
TRAINING_FILE = PROJECT_DIR + "cleaned_tweets.csv"

TFIDF_PKL = PROJECT_DIR + 'models/X_train_tfidf.pkl'
COUNT_VECT_PKL = PROJECT_DIR + 'models/count_vect.pkl'
TRANSFORMER_PKL = PROJECT_DIR + 'models/tfidf_transformer.pkl'
CLINTON = TWEET_DIR + '/clinton.csv'
TRUMP = TWEET_DIR + '/trump.csv'
TWEET_COLUMNS = ['id', 'handle', 'text', 'is_retweet', 'time', 'in_reply_to_screen_name', 'in_reply_to_status_id',
			 'in_reply_to_user_id', 'is_quote_status', 'lang','retweet_count','favorite_count','coordinates',
			 'place','source_url','truncated', 'entities', 'source','symbols','hashtags']


''' 
	Takes the individual CSV files and returns the text and lables as well as creates 
	one large CSV file containing the labels and text

	@param source_dir the directory containing all the politician tweet csv files
	@param output_file the name of the file that will contain the combined tweet data

	@return data the tweet text after cleaning (removal of stopwords and other unwanted elements) as a list
	@return labels the labels (twitter handles) corresponding to data as a list

	Generates a CSV file, without header, where each row consists of a label (twitter handle) 
	and data (cleaned text)

'''
def combineTweetCSVs(source_dir=TWEET_DIR, output_file=TRAINING_FILE):
	labels = []
	data = []
	for file in os.listdir(source_dir):
		if file.endswith(".csv"):
			print(file)
			df = pd.read_csv(source_dir + "/" + file, header=None, names=TWEET_COLUMNS)
			labels = labels + list(df['handle'])
			data = data + clean(df['text'])
	print("created masssive traiing set")
	rows = []
	for i in range(len(data)):
		row = [labels[i], data[i]]
		with open(output_file, 'a') as out:
			wr = csv.writer(out)
			wr.writerow(row)
	return data, labels

''' 	
	cleans the text by changing to lowercase, removing stopwords, removing urls, and removing twitter handles.
	
	NOTE: Requires download of the nltk stopwords corpus prior to running 
 '''
def clean(text_data):
	text = list(text_data)
	clean_text = []
	for t in text:
		t = tweetToken.preprocess(t)
		t = " ".join(t)
		clean_text.append(t)
	return clean_text


'''Does the vectorization for sparse data (which greatly reduces the size) and does the 
	tfidf normalization'''
def createFeaturesFromFileandSave(source_file=TRAINING_FILE):
	print("starting")
	df = pd.read_csv(source_file, header=None, names=['label', 'value'])
	X_train = list(df['value'].values.astype('U'))
	y_train = list(df['label'].values.astype('U'))
	count_vect = CountVectorizer()
	X_train_counts = count_vect.fit_transform(X_train)
	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
	print("created features")
	save_object(count_vect, COUNT_VECT_PKL)
	save_object(X_train_tfidf, TFIDF_PKL)
	save_object(tfidf_transformer, TRANSFORMER_PKL)
	return X_train_tfidf, X_train, y_train, count_vect, tfidf_transformer


def createModelFromFile(source_file=TFIDF_PKL, data_file=TRAINING_FILE, k=8, dimensions=100):
	with open(source_file, 'rb') as input:
		data = pickle.load(input)
		df = pd.read_csv(data_file, header=None, names=['label', 'value'])
		labels = list(df['label'])
		print("attempting dimensionality reduction")
		tSVD = TruncatedSVD(n_components=dimensions)
		tSVD_fitted = tSVD.fit_transform(data)
		print("truncatedSVD transformed")
		clf = KMeans(random_state=5, n_clusters=k)
		result = clf.fit_predict(tSVD_fitted)
		print("clustered")
		return result, labels

def save_object(obj, filename):
	with open(filename, 'wb') as out:
		pickle.dump(obj, out, pickle.HIGHEST_PROTOCOL)

def main(args):
	if len(args) == 1:
		if args[0] == 'combine':
			combineTweetCSVs()
		elif args[0] == 'features':
			createFeaturesFromFileAndSave()
	if len(args) == 2:
		if args[0] == 'model':
			createModelFromFile(k=args[1])
	if len(args) == 3:
		if args[0] == 'model':
			createModleFromFile(k=args[1], dimensions=args[2])
		elif args[0] == 'kmeans':
			cluster_from_file(filename=args[1], k=args[1])

if __name__ == "__main__":
	main(sys.argv[1:])
