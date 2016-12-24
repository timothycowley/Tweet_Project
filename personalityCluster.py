import csv
import sys
import numpy as np
import pandas as pd
import pickle

from sklearn import cluster

PROJECT_DIR = '/home/timothy/Desktop/Public/AI/Data Mining class/Project/'
PERSONALITY_TABLE = '/home/timothy/Desktop/Public/AI/TweetProject/Tim/personality_table.csv'
ID_TABLE_FILE = PROJECT_DIR + 'id_table.csv'
RESULT_FILE = PROJECT_DIR + 'personality_clusters/personality_cluster_result'
TWEET_COLUMNS = ['id', 'handle', 'text', 'is_retweet', 'time', 'in_reply_to_screen_name', 'in_reply_to_status_id',
			 'in_reply_to_user_id', 'is_quote_status', 'lang','retweet_count','favorite_count','coordinates',
			 'place','source_url','truncated', 'entities', 'source','symbols','hashtags']
ID_COLUMNS = ['first', 'last', 'party', 'state', 'handle', 'id', 'position', 'filename']

PERSONALITY_COLUMNS = ['handle', 'first', 'last', 'openness', 'adventurousness', 'artistic interests', 'emotionality', 'imagination', 'intellect',
'authority-challenging', 'conscientiousness', 'achievement striving', 'cautiousness', 'dutifulness', 'orderliness', 'self-discipline',
'self-efficacy', 'extraversion', 'activity level', 'assertiveness', 'cheerfulness', 'excitement-seeking', 'outgoing', 'gregariousness',
'agreeableness', 'altruism', 'cooperation', 'modesty', 'uncompromising', 'sympathy', 'trust', 'emotional range', 'fiery', 
'prone to worry', 'melancholy', 'immoderation', 'self-consciousness', 'susceptible to stress', 'challenge', 'closeness', 'curiosity',
'excitement', 'harmony', 'ideal', 'liberty', 'love', 'practicality', 'self-expression', 'stability', 'structure', 'conservation',
'openness to change', 'hedonism', 'self-enhancement', 'self-transcendence']

def analyze(source_file=PERSONALITY_TABLE, k=8, output=RESULT_FILE):
	personality = pd.read_csv(source_file, header=None, names=PERSONALITY_COLUMNS)
	print(personality.shape)
	features = personality
	y = personality['handle']
	del(features['handle'])
	del(features['first'])
	del(features['last'])
	clf = cluster.KMeans(n_clusters=k, random_state=5)
	result = clf.fit_predict(features, y=y)
	write_to_file(result, y, output_file=output + "_" + str(k) + ".csv")


def write_to_file(result, y, id_table=ID_TABLE_FILE, output_file=RESULT_FILE):
	df = pd.read_csv(id_table, header=None, names=ID_COLUMNS)
	try:
		open(output_file, 'x')
	except:
		pass
	for i in range(len(result)):
		df_match = df[df.handle == y[i]]
		
		row = [list(df_match['first'])[0], 
		       list(df_match['last'])[0], 
		       list(df_match['party'])[0],
				list(df_match['state'])[0],
				y[i],
				result[i]
				]
		print(y[i])
		with open(output_file, 'a') as out:
			wr = csv.writer(out)
			wr.writerow(row)


def main(args):
	if len(args) == 2:
		if args[0] == 'analyze':
			analyze(k=int(args[1]))

if __name__ == "__main__":
	main(sys.argv[1:])
