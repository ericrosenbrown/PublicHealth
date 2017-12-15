import csv
import math
import copy
import sys
import tfidf
from sklearn import svm

def write_arff():
        f = open('tf_idf_weka.arff', 'w')

        myStr = "@RELATION tfidf\n\n"

        for k in wordList:
                myStr += "@ATTRIBUTE " + k + " NUMERIC\n"

        myStr += "\n@DATA\n"

        for i in range(len(transcriptions)):
                for w in range(len(wordList)):
                        myStr += str(tfidfs[w][i][1])+","
                myStr += str(labels[i]).replace("[","").replace("]","").replace(" ","")
                myStr += "\n"
        f.write(myStr)
        f.close()

transcriptions = []
labels = []
remove = "0123456789,\":.-*[]"
wordList = []


def populateWordList(bag):
        for sentence in bag:
                for word in sentence:
                        if word not in wordList:
                                letin = True
                                for letter in word:
                                        if letter not in "abcdefghijklmnopqrstuvwxyz":
                                                letin = False
                                if letin:
                                        wordList.append(word)


with open('publichealth_data.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        counter = 0
        for row in spamreader:
                if counter >= 2:
                        #Get the score/lastWord if there is one
                        score = row[-1]
                        score = score.split(',')
                        lastWord = score[0]
                        score = score[1:]
                        nscore = [] #numberedScore
                        for s in score:
                                nscore.append(int(s))
                        labels.append(copy.deepcopy(nscore))


                        #Now get transcriptions
                        words = row[:-1]
                        cleanWords = []
                        for word in words:
                                for b in remove:
                                        word = word.replace(b,"")
                                cleanWords.append(word.lower())
                        for b in remove:
                                lastWord = lastWord.replace(b,"")
                        if lastWord != '':
                                cleanWords.append(lastWord)

                        transcriptions.append(copy.deepcopy(cleanWords))
                        #print cleanWords
                        #print nscore, lastWord
                counter = counter + 1

populateWordList(transcriptions)

trainingAmount = int(len(transcriptions)*.8)
testingAmount = len(transcriptions)-trainingAmount

XTrain_pre = transcriptions[:trainingAmount]
XTest_pre = transcriptions[trainingAmount:]

YTrain = []
XTrain = []

#Now we need to convert each transcription into vector of word frequency
for x in XTrain_pre: #Loop through each transcription
        datapoint = []
        for w in wordList: #for each unique word in the word list
                frequency = 0
                for word in x: #for each word in a specific x transctipon
                        if w == word: #word matches the word in wordlist
                                frequency += 1
                datapoint.append(frequency)
        XTrain.append(copy.deepcopy(datapoint))

totalWordFreq = [sum(x) for x in zip(*XTrain)] #frequency of each word in wordList, indexed same way
#print totalWordFreq
totalWordFreq = [x+1 for x in totalWordFreq] #Alpha-smoothing on word frequency

#further cleaning 
new_wordList = []
for w in range(len(wordList)):
        if totalWordFreq[w] >= 5:
                new_wordList.append(wordList[w])

YTrain = labels[:trainingAmount]
YTest = labels[trainingAmount:]


               
table = tfidf.tfidf()
for i in range(len(transcriptions)):
        table.addDocument(str(i), transcriptions[i])

tfidfs = []
for w in new_wordList:
        tfidfs.append(table.similarities([w]))

x_svm_train = []
for i in range(trainingAmount):
                l = []
                for w in range(len(new_wordList)):
                        l.append(tfidfs[w][i][1])
                x_svm_train.append(copy.deepcopy(l))

y_svm_train = []
yclass=2
for i in range(trainingAmount):
        y_svm_train.append(labels[i][yclass])

x_svm_test = []
for i in range(testingAmount):
                l = []
                for w in range(len(new_wordList)):
                        l.append(tfidfs[w][i+trainingAmount][1])
                x_svm_test.append(copy.deepcopy(l))

y_svm_test = []
for i in range(testingAmount):
        y_svm_test.append(labels[i+trainingAmount][yclass])
        

#write_arff()
clf = svm.SVC()
clf.fit(x_svm_train, y_svm_train)

print clf.predict(x_svm_test)
print new_wordList
#print wordList
