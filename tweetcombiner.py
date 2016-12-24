import csv
import numpy as np
import pandas as pd
import sys
import os
import shlex

source_dirLaptop = 'c/Users/Tim/Desktop/All Files/TweetProject/personality/'

def combinePersonalityCSV(source_dir='/media/sf_VM_share/TweetProject/personality/',
	id_file='/media/sf_VM_share/TweetProject/id_table.csv',
	output_file='/media/sf_VM_share/TweetProject/personality_table.csv'):
	suffix = "_personality.csv"
	names = ['first', 'last', 'party', 'state', 'handle', 'id', 'position', 'filename']
	politicians = pd.read_csv(id_file, header=None, names=names)
	filenames = (list(politicians['filename']))
	firsts = (list(politicians['first']))
	lasts = (list(politicians['last']))
	handles =(list(politicians['handle']))
	pNames =['feature', 'value']
	for i in range(len(filenames)):
		pfile = source_dir + filenames[i][:-4] + suffix
		personality = pd.read_csv(pfile, header=None, names=pNames)
		values = list(personality['value'])
		values = [lasts[i]] + values
		print(values)
		values = [firsts[i]] + values
		values = [handles[i]] + values
		with open(output_file, 'a') as out:
			wr = csv.writer(out)
			wr.writerow(values)

	#politician_handles = list(politicians[['filename']])
	#print(politician_handles.head(10))

	#data_iter = csv.reader(id_file)
	#for data in data_iter:
	#	print(data)
	#data = [data for data in data_iter]
	#data_array = np.asarray(data)
	#for politician in data_array:
	#	print(politician)
	#	handle = politician[4]
	#	print(handle)
	#	features = []
	#	data_iter2 = csv.reader(source_dir + handle + suffix)
	#	data2 = [data2 for data2 in data_iter2]
	#	data_array2 = np.asarray(data2)
	#	for trait in data_array2:
	#		features.append(trait[1])
	#	features.prepend(politician[0])
	#	features.prepend(politician[1])
	#	features.prepend(handle)
	#	with open(output_file, 'a') as out:
	#		wr = csv.writer(out)
	#		wr.writerow(features)

	#for file in os.listdir(source_dir):
	#	if file.endswith(".csv"):

			#look up individual on id_table using filename
			#add second element of each row to table as seperate columns in single row of final csv
			#Should be:
				#twitter handle
				#full name
				#features






def personalityCSV(source_dir="/home/timothy/Desktop/Public/AI/Data Mining class/Project/personality_insights", output_dir="/home/timothy/Desktop/Public/AI/Data Mining class/Project/personality/"):
	suffix = "_personality.csv"
	for file in os.listdir(source_dir):
		if file.endswith(".stats"):
			with open(source_dir + "/" + file, 'r') as f:
				output_file = output_dir + file[:-6] + suffix
				try:
					print('trying to create file ' + output_file)
					open(output_file, 'x')
				except:
					pass
				content = f.readlines()
				for line in content:
					if line.startswith('Openness'):
						break
					content.remove(line)
				for line in content:
					words = line.split()
				#	if len(words) == 4: 
				#		words = words[:2]
				#		words[1] = float(words[1].strip('%'))/100
					if len(words) >= 4:
						words = words[:len(words) -2]
						output = [0,1]
						output[0] = words[0]
						for i in range(1, len(words) - 1):
							output[0] = output[0] + " " + words[i]
						output[1] = str(float(words[-1].strip('%'))/100)
						with open(output_file, 'a') as out:
							wr = csv.writer(out)
							wr.writerow(output)
						
						
					
						
					
					
def removeDuplicates():
	for file in os.listdir("/home/timothy/Desktop/Public/AI/test_folder"):
		if file.endswith(".csv"):
			names = ['id', 'handle', 'text', 'is_retweet', 'time', 'in_reply_to_screen_name', 'in_reply_to_status_id',
'in_reply_to_user_id', 'is_quote_status', 'lang','retweet_count','favorite_count','coordinates','place','source_url','truncated', 
'entities', 'source','symbols','hashtags'] 
			table = pd.read_csv("/home/timothy/Desktop/Public/AI/test_folder/" + str(file), names=names)
			table = table.drop_duplicates(subset=['id'])
			table.to_csv("/home/timothy/Desktop/Public/AI/test_output/" + str(file), index=False, quoting=csv.QUOTE_NONNUMERIC, header=False)

def combineTweetsR():
	source_dir = "/home/timothy/Desktop/Public/AI/Data Mining class/Project/tweets"
	output_dir = "/home/timothy/Desktop/Public/AI/Data Mining class/Project/tweet_combined/"
	for file in os.listdir(source_dir):
		if file.endswith(".csv"):
			try:
				open(output_dir + str(file)[:-3] + 'txt', 'x')
			except:
				pass
			with open(source_dir + "/" + file, 'r') as tweets:
				data_iter = csv.reader(tweets)
				data = [data for data in data_iter]
				data_array = np.array(data)
				for tweet in data_array:	
					with open(output_dir + str(file)[:-3] + 'txt', 'a') as combined:
						combined.write(tweet[2])


def combineTweets(input_file, output_file):
	with open(input_file, 'r') as tweets:
		data_iter = csv.reader(tweets)
		data = [data for data in data_iter]
		data_array = np.asarray(data)
		for tweet in data_array:
			with open(output_file, 'a') as combined:
				combined.write(tweet[2])



def main(args):
	if len(args) == 1:
		if args[0] == 'clean':
			removeDuplicates()
		if args[0] == 'combine':
			combineTweetsR()
		if args[0] == 'personality':
			personalityCSV()
		if args[0] == 'combinePersonality':
			combinePersonalityCSV()
	if len(args) == 2:
		try:
			open(output_file, 'x')
		except:
			pass
		input_file = args[0]
		output_file = args[1]
		combineTweets(input_file, output_file)

if __name__ == "__main__":
	main(sys.argv[1:])
