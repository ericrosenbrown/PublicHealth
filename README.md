DESCRIPTION OF RESEARCH:

I first wrote a python program to clean the csv file due to transcription errors. This mostly cleans up lower/upper case, numbers, punctuation. I then attempted to create word-frequency vectors of each transcript and tried to train a multiclass SVM of 2^7 = 128 classes, for each possible combination of class. This classified terribly, and we assumed this may be because each class is not truly separate, they are probably correlated to each other, so we decided to try a classifier that wouldn't treat each class as independent.

However, during this we noticed that many of the labels for the transcripts did not seem correct. For example, in many transcripts, people mention that they enjoy drinking with friends, but the label "drink for social reasons" was not selected. We thought that these noisy labelings could be bad, but haven't addressed this.

The next step was to take the word frequency vectors we ran through the SVM, and try to put it into Weka instead to perform some off-the-shelf ML algorithms. In order to use Weka, the data format needs to be an arff. I created a python program to take my vectors in python and write to .arff in the correct format to automatically import to Weka.  After applying many different classifiers to the vectors in Weka, we were not able to get anything that classified in any meaningful way.

After getting no meaningful results from Weka, we decided that there may be no real information in how the variables are correlated, so we decided to calculate the correlations between the 7 labels. corr_labs1.png is a picture of these correlations, none of the labels seemed to have any significant correlation to any other label.

After seeing no real correlation between labels, we decided that instead of doing word-frequency, we may want to try term-frequency inverse-document frequency (TF-IDF), which may be able to give us better results. So I created a python program to turn all of the transcripts into TF-IDF vectors. The TF-IDF vectors seems to better represent important features in the transcripts while weighting words that weren’t important way less. However, after taking the vectorizations of the transcripts with TF-IDF features and plugging them into the SVM, Bayes, and Weka, we still not get any significant results. The best thing we got was applying random forests to the TF-IDF vectorizations in Weka. I included a picture of the results (random_forest.png)

Professor Littman suggested trying to use word2vec in order to possibly create better vectorizations than tf-idf. I was never able to get a successful run of word2vec working on the data, so this may be a good place to start. However, it seems that the current data is not large enough to train your own model, so it may be helpful to use an off-the-shelf trained one by Google.

All in all, almost of all the classifiers ended up only predicting the majority labeling. After looking, the first 3 labels are almost always labeled 1 in the csv, and the last 4 labels are labeled 0 significantly more. This may be a reason why most models just predict the first three labels as 1 and the last four as 0. However, better feature extraction may help mitigate this issue.s


Attached files:
my-tf-idf.py
	- reads in a local file 'publichealth_data.csv', and grabs all of the transcripts with their respective labels. Afterwards, it calls populatedWordList, which creates a list of all unique words in the transcripts, with some cleaning applied. The transcripts are then split into training (80%) and testing (20%). After this, the script calculates totalWordFreq, which is a list where the ith element represents the ith word in wordList, and the value of the ith element in totalWordFreq is how frequent that word appears in all of the documents. These vectorizations can be used for various purposes (all of this is up to line 113)
	- after line 113, I implemented a TF-IDF vectorization of the transcripts. tfidfs contains all of the tfidf values for each word and document. I implemented a SVM to try to classify transcripts tfidfs representations. This is a multiclass SVM that treats each of the class labels seperate.
	- This script also contains a write_arff function, which will create a valid arff, where each entry in the arff is represented by the frequency of all the words in that particular transcript, as well as the 7 included labelings. The written arff can be plugged into weka for further statistical analysis.

final.arff
	- this is a valid arff that I wrote out from my-tf-idf that can be directly opened in Weka. This arff contains each transcript as a vector of tf-idf values.

tf_idf_weka.arff
	- this is another valid arff that I wrote out from my-tf-idf that can be directly opened in Weka. This arff contains each transcript as a vector of word frequency values in that particular transcript.

bayes.py
	- This is a file where I implemented a MAP (Maximum Aposterior) implementation on the word frequency vectors for the transcripts.
