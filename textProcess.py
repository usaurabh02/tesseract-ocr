import re
import os
def readFile(path):
    file = open(path, "r")
    text = file.read()
    file.close()
    return text

def parseText(text):
    report=''
    sentences = text.split('\n')
    #Remove the empty string
    sentences = [sentence for sentence in sentences if sentence != '']
    #Remove the '\t'
    sentences = [sentence.replace('\t', '') for sentence in sentences]

    #if numbers and letters appear together without a space, add a space
    for i in range(len(sentences)):
        if sentences[i].isdigit() and sentences[i-1].isalpha():
            print(sentences[i])
            sentences[i] = sentences[i-1] + ' ' + sentences[i]
            print(sentences[i])

    # use regex  to find dates in the form dd-mm-yyyy in sentences store inside dates variable
    dates = re.findall(r'\d{2}-\d{2}-\d{4}', text)
    print(dates)


    #if there are more than one ':' in a sentence then send it to the next line
    for i in range(len(sentences)-1):
      if sentences[i].count(':') > 1:
         print(sentences[i])
         #split the sentence into two parts
         sentences[i] = sentences[i].split(':')[0] + ':' + sentences[i].split(':')[1]

    #if sentence ends with ':' then bring the next sentence to the same line
    for i in range(len(sentences)):
        if sentences[i].endswith(':'):
            sentences[i] = sentences[i] + sentences[i+1]

    #find the word report and the word before it and store in the variable report
    for i in range(len(sentences)):
        if sentences[i].lower().startswith('report'):
            report = sentences[i-1]
            break
    print(report)
    
    #Write sentences to a file
    with open('static\\healthRecords\\recognized_new.txt', 'w') as f:
        for sentence in sentences:
            f.write(sentence + '\n')
    
    return sentences

def extractKeyValue(sentences):
    keyValuePairs = []
    for sentence in sentences:
        #Find all the key value pairs separated by ':' 
        keyValuePairs.extend(re.findall(r'(.*):(.*)', sentence))

    return keyValuePairs
#Convert the key value pairs to a json
import json
def convertToJson(keyValuePairs):
    json = {}
    for keyValuePair in keyValuePairs:
        key = keyValuePair[0].strip()
        value = keyValuePair[1].strip()
        json[key] = value
    return json


