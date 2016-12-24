import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import tweetToken


''' It would be a lot cleaner to use a pipeline (see sklearn documentation on text analysis)
	I had some sort of bug and just wanted to get it working so did it this way

	I'm leaving a lot of things out here. Most notabily:
		need to split off a test set and test on that instead of on the input data

	Pay close attention to the Notes below:
		1. File paths need to be updated to reflect those on your system
		2. tweetToken is what I called Crystal's code snippet on slack 
			I do not have the strip_urls function, so I just wrote an empty function for this, 
			that needs to be replaced with Crystal's code
'''



'''Generates a training set consisting of a list of tweet text and a list of corresponding labels
	 from Trump and Clinton tweet csv's. 

	***NOTE default file paths are only relevant on my system, please change these

'''
def createTrainingSet(trump_source='/media/sf_VM_share/TweetProject/tweets/trump.csv',
 clinton_source='/media/sf_VM_share/TweetProject/tweets/clinton.csv'):
	names = ['id', 'handle', 'text', 'is_retweet', 'time', 'in_reply_to_screen_name', 'in_reply_to_status_id',
'in_reply_to_user_id', 'is_quote_status', 'lang','retweet_count','favorite_count','coordinates','place','source_url','truncated', 
'entities', 'source','symbols','hashtags'] 
	clinton = pd.read_csv(clinton_source, header=None, names=names)
	trump = pd.read_csv(trump_source, header=None, names=names)
	labels = clinton['handle']
	labels = list(labels.append(trump['handle']))
	data = np.concatenate((clean(clinton['text']), clean(trump['text'])))
	return data, labels

'''Imports the code Crystal sent on slack to clean the text. I'm having trouble with pandas changing the 
	shape of the data so I just convert it to a list and back to a numpy array (avoiding use of pandas)  

	**** NOTE that I named this tweetToken, so make sure to update the input and name here to match
	the name on your system
	 '''
def clean(text_data):
	text = list(text_data)
	clean_text = []
	for t in text:
		t = tweetToken.preprocess(t)
		t = " ".join(t)
		clean_text.append(t)
	cleaned_text = np.asarray(clean_text)
	return cleaned_text

'''Does the vectorization for sparse data (which greatly reduces the size) and does the 
	tfidf normalization'''
def createFeatures(data):
	count_vect = CountVectorizer()
	X_train_counts = count_vect.fit_transform(data)
	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
	return X_train_tfidf, count_vect, tfidf_transformer

'''fits the data to a model - just replace MultinomialNB with something else to try other models'''
def createModel(data, labels):
	from sklearn.naive_bayes import MultinomialNB
	clf = MultinomialNB().fit(data, labels)
	return clf

'''makes a prediction after transforming the input with the same CountVectorizer and TfidfTransformer
	used to generate the model and then feeds it to the classifer. The output is a list of 
	predictions (the twitter handles: HillaryClinton or realDonaldTrump)'''
def predict(clf, count_vect, tfidf_transformer, data):
	X_test_counts = count_vect.transform(data)
	X_test_tfidf = tfidf_transformer.transform(X_test_counts)
	predicted = clf.predict(X_test_tfidf)
	return predicted

'''automatically trains a MultinomialNB classifier for Clinton and Trump tweets and then applies
	the model to the same train set (not best practice but 
	for demo purposes) and returns the accuracy of the prediction'''
def main():
	data, labels = createTrainingSet()
	tfidf, count_vect, tfidf_transformer = createFeatures(data)
	clf = createModel(tfidf, labels)
	predicted = predict(clf, count_vect, tfidf_transformer, data)
	correct = 0
	incorrect = 0
	for i in range(len(predicted)):
		if labels[i] == predicted[i]:
			correct += 1
		else:
			incorrect += 1
	print(correct*1.0/(correct + incorrect))

if __name__ == "__main__":
	main()