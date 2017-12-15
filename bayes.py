#from sklearn import svm
import csv
import math
import copy

def predict_transcript_answer(transcript):
        #Given a transcript, predict the answer by Naive Bayes implementation
        #TODO: TAKE THE CLEAN CODE, TURN IT INTO A CLEANING FUNCTION SO THIS CAN TAKE IN ARBITRARY STRINGS AND CLEAN THEM
        pass

def p_w_given_a(word,a_i,v):
        #calculate p(word|answer_i)
        #Loop through all answers, calculate how many with answer_i having value v have word in it.
        ai_counter = 0 #count how many have answer_i
        word_counter = 0 #count how many answer_i's have the word in it
        for answer in range(len(YTrain)): #Use the YTrain data for calculating these probabilitties
                if YTrain[answer][a_i] == v:
                        ai_counter += 1
                        if word in XTrain_pre[answer]:
                                word_counter += 1
                        
        return word_counter/float(ai_counter)

def vector2num(v):
        b = 6 #the number of possible fill in's
        num = 0
        for d in v:
                num += d*(math.pow(2,b))
                b = b-1
        return int(num)

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
#print wordList

trainingAmount = int(len(transcriptions)*.8)
XTrain_pre = transcriptions[:trainingAmount]
XTest_pre = transcriptions[trainingAmount:]
YTrain_pre = labels[:trainingAmount]
YTest_pre = labels[trainingAmount:]

#print XTrain_pre
#print YTrain_pre

YTrain = []
XTrain = []

YTest = []
XTest = []

#YTrain_pre and Test have classes in form of 7-len list with either 1 or 0's. we will convert these to binary for int class labels.
for l in YTrain_pre:
        YTrain.append(vector2num(l))
for l in YTest_pre:
        YTest.append(vector2num(l))

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

for x in XTest_pre: #Loop through each transcription
        datapoint = []
        for w in wordList: #for each unique word in the word list
                frequency = 0
                for word in x: #for each word in a specific x transctipon
                        if w == word: #word matches the word in wordlist
                                frequency += 1
                datapoint.append(frequency)
        XTest.append(copy.deepcopy(datapoint))

#print XTrain[10]
#print YTrain

#print wordList

totalWordFreq = [sum(x) for x in zip(*XTrain)] #frequency of each word in wordList, indexed same way
#print totalWordFreq
totalWordFreq = [x+1 for x in totalWordFreq] #Alpha-smoothing on word frequency

totalWords=sum(totalWordFreq) #total number of words in all transcripts
#print totalWordFreq
p_w = [freq/float(totalWords) for freq in totalWordFreq]

#print p_w
#print totalWordFreq[2]
#print totalWords
#print totalWordFreq
#print XTrain[0]

YTrain = YTrain_pre
#print YTrain

totalAnswerFreq = [sum(x) for x in zip(*YTrain)] #frequency of each answer in YTrain
#print totalAnswerFreq

p_a = [x/float(len(YTrain)) for x in totalAnswerFreq] #p(answer_i). Easily can calculate p(not answer_i) as the 1-p(answer_i)
#print p_a

#given a word, an answer location ,and an answer value
#print p_w_given_a('bars',0,1)

f = open('attempt1000.txt', 'w')


#for i in range(len(XTrain)):
#    myStr += str(XTrain[i]).replace("[","").replace("]","").replace(" ","")
#    myStr += ","
#    myStr += str(YTrain[i]).replace("[","").replace("]","").replace(" ","")
#    myStr += "\n"

#further cleaning 
moreThanThree = {}
for w in range(len(wordList)):
        if totalWordFreq[w] >= 5:
                moreThanThree[wordList[w]] = [p_w[w],w]

myStr = ""

for k in moreThanThree.keys():
	myStr += "@ATTRIBUTE " + k + " NUMERIC\n"

myStr += "\n"
                
for i in range(len(XTrain)):
        for d in moreThanThree.keys():
               myStr +=  str(moreThanThree[d][0]*float(XTrain[i][moreThanThree[d][1]]))+","
        myStr += str(YTrain[i]).replace("[","").replace("]","").replace(" ","")
        myStr += "\n"

 #   myStr += str(XTrain[i]).replace("[","").replace("]","").replace(" ","")
#    myStr += ","
#    myStr += str(YTrain[i]).replace("[","").replace("]","").replace(" ","")
#    myStr += "\n"


f.write(myStr)
f.close()

