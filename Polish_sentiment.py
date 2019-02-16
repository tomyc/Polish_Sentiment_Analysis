
import csv
import json
import os
import io
from tqdm import tqdm
import codecs



class Classifier:


   def __init__(self,filename, info = True):
        self.info = info
        file = io.open(filename, 'r', encoding='utf8')
        self.dict = json.load(file)
        file.close()
   @staticmethod
   def evaluate(sentence , dictionary_file = 'sentiment.json' , info = True):
        file = io.open(dictionary_file, 'r', encoding='utf8')
        dict = json.load(file)
        file.close()
        
        words = sentence.replace(",", "").lower().replace(".","").replace("/","").split(" ")
        
        if(use_class_probabilites):
            positive = dict["Positive"]
            negative = dict["Negative"]
        
        else:
            positive = 1
            negative = 1

        for word in words:
            if word in dict["Words"]:
                if info:
                    print(word + " : Word in dictionary")
            

                positive *= dict["Words"][word]["Positive"]
                negative *= dict["Words"][word]["Negative"]
            
        if info:
            print("Sentence score:")
            print("Positive: " +str(positive))
            print("Negative: " + str(negative))
            
        if positive> negative:
            return "Positive"
        elif negative>positive:
            return "Negative"
        else:
            return "Undefined"

    



   @staticmethod
   def loadDictionary(filename):

        with open(filename, 'r', encoding='utf8') as file:
            dictionary = json.load(file)
        

        
        return dictionary
   @staticmethod
   def updateFile(filename,dictionary):
        file = codecs.open(filename, 'rw', encoding='utf8')
        json.dump(dictionary, file, ensure_ascii=False)
        file.close

   @staticmethod
   def preprocess_comments(positive_file='positive_comments_form_score.txt', dictionaryFile = "dictionary.json"):
        
        dict = Classifier.loadDictionary(dictionaryFile)
        
        
        file =codecs.open(stopwords_file, 'r', "windows-1250",errors='ignore')



        with open(positive_file) as f:
            lines = f.readlines()
        print(lines[0])

   @staticmethod
   def preprocess_reviews(stopwords_file = "stopwords-pl.json",data = "data.csv",dictionaryFile = "dictionary.json",treshold = 5,normalize= False):

        dict = {'Words':{}}

        file =codecs.open(stopwords_file, 'r', "windows-1250",errors='ignore')
        stopwords = json.load(file)
        file.close()


        f =codecs.open(data,'r',"windows-1250",errors='ignore')
        reader = csv.reader(f)
        i=0
        num_negative = 0
        num_positive = 0
        words = []

        positive_sentences = []
        negative_sentences = []


        num_words=0
        for row in tqdm(reader):
            #print("reading row " + str(i))
            #print(row)
        
            if (row!=[]):
                if row[0]=="Wymaga uzupełnienia.":
                    continue
                
                i+=1
                if (i >105000):
                    break
                if float(row[1]) > treshold+2:
                    positive_sentences.append(row[0])
                elif float(row[1]) <= treshold-2:
                    negative_sentences.append(row[0])
                    
        i=0           

        num_positive_sentences = len(positive_sentences)
        num_negative_sentences = len(negative_sentences)



        lower_number = min(num_negative_sentences,num_positive_sentences)



        if(normalize):
            
            num_positive_sentences = lower_number
            num_negative_sentences = lower_number


        for i in tqdm(range(num_positive_sentences)):
            
            #print(i)
            #print(positive_sentences[i].strip(",").strip(".").split(" "))
            words = positive_sentences[i].replace(",", "").replace(".","").lower().replace("/","").split(" ")
            new_words= []
            for word in words:
                if word not in new_words:
                    new_words.append(word)
            for word in new_words:
                if word in stopwords:
                    #print("Stopword")
                    continue
                num_words+=1
                
                num_positive +=1
                

                if word not in dict["Words"]:
                    
                    dict["Words"][word]={'Positive':1}
                    dict["Words"][word]["Negative"]=0
                    
                else:
                
                    dict["Words"][word]["Positive"]+=1




        for i in tqdm(range(num_negative_sentences)):               
            words = negative_sentences[i].replace(",", "").lower().replace(".","").replace("/","").split(" ")
            new_words= []
            for word in words:
                if word not in new_words:
                    new_words.append(word)
            for word in new_words:
                if word in stopwords:
                    #print("Stopword")
                    continue
                
                
                num_negative +=1

                if word not in dict["Words"]:
                
                    dict["Words"][word]={'Positive':0}
                    dict["Words"][word]["Negative"]=1
                    
                

                else:
                    dict["Words"][word]["Negative"]+=1


        Classifier.updateFile(dictionaryFile,dict)
        if not normalize:

            print("Negative sentences :" + str(len(positive_sentences)))
            print("Positive sentences :" + str(len(negative_sentences)))

        

            dict["Negative_sentences"] = len(positive_sentences)
            dict["Positive_sentences"] = len(negative_sentences)

        else:
            dict["Negative_sentences"] = lower_number
            dict["Positive_sentences"] = lower_number 
        


        dict["Positive_words"] = num_positive
        dict["Negative_words"] = num_negative

        dict["Words_count"] = num_words
        print("Word count: " + str(num_words))
        print("Positive words: " + str(num_positive))
        print("Negativee words: " + str(num_negative))
        print(str(len(dict["Words"])))

        Classifier.updateFile(dictionaryFile,dict)

   def learn(filename= "dictionary.json",sentimentfile = "sentiment.json"):
        file =codecs.open(filename, 'r', "windows-1250",errors='ignore')
        dict = json.load(file)
        file.close()

        sentdict = {'Words': {}}


        print(len(dict["Words"].keys()))
        print(dict.keys())

        size = 0
        for word in dict["Words"]:
            size += dict["Words"][word]['Positive']+ dict["Words"][word]['Negative']

        size-=2
        print(size)
        i =0

        print("Looping through words")

        for word in tqdm(dict["Words"]):
            i+=1
            #print("-------Word :" + word)
        


            P_positive_word = (dict["Words"][word]["Positive"]+1)/(dict["Positive_words"]+len(dict["Words"]))
            #print("P_positive_word: "+ str(P_positive_word))

            

            P_negative_word = (dict["Words"][word]["Negative"]+1)/(dict["Negative_words"]+len(dict["Words"]))

            sentdict["Words"][word] = {"Positive":0}

            sentdict["Words"][word]["Positive"] = P_positive_word
            sentdict["Words"][word]["Negative"] = P_negative_word
        sentdict["Negative"] = dict["Negative_sentences"]/(dict["Negative_sentences"] + dict["Positive_sentences"])

        Classifier.updateFile(sentimentfile,sentdict)
        sentdict["Positive"] = dict["Positive_sentences"]/(dict["Negative_sentences"] + dict["Positive_sentences"])
        Classifier.updateFile(sentimentfile,sentdict)
        print(sentdict["Positive"])
        print(sentdict["Negative"])
        print("Finished succesfully")
   @staticmethod
   def accuracy_check():

        m = confusion_matrix()
        
        f = codecs.open("data.csv",'r','utf-8',errors='ignore')
        reader = csv.reader(f)

        i=0

        print(reader)

        positive_sentences = []
        negative_sentences = []


        for row in tqdm(reader):
            #print("reading row " + str(i))
            #print(row)
        
            if (row!=[]):
                if row[0]=="Wymaga uzupełnienia.":
                    continue
                i+=1
                if (i <15000):
                    continue

                
                
            
                if float(row[1]) > treshold+2:
                    positive_sentences.append(row[0])
                elif float(row[1]) <= treshold-2:
                    negative_sentences.append(row[0])

        num_positive_sentences = len(positive_sentences)
        num_negative_sentences = len(negative_sentences)



        lower_number = min(num_negative_sentences,num_positive_sentences)



        if(normalize):
            
            num_positive_sentences = lower_number
            num_negative_sentences = lower_number



        for i in tqdm(range(num_positive_sentences)):
            score = Classifier.evaluate(positive_sentences[i])
            if score == "Positive":
                        m.TP+=1
            if score == "Negative":
                        m.FN+=1


        for i in tqdm(range(num_positive_sentences)):
            score = Classifier.evaluate(negative_sentences[i])
            if score == "Negative":
                        m.TN+=1
            if score == "Positive":
                        m.FP+=1


        print("Finished analyzing " + str(i) + "sentences")
        m.print_results()
        m.save_results()
   @staticmethod
   def convert_score(data = 'data.csv',lower = 5, upper = 5,positive_file = "positive_comments_form_score.txt",negative_file = "negative_comments_form_score.txt"):
        f =codecs.open(data,'r',"windows-1250",errors='ignore')
        reader = csv.reader(f)
        
        positive_sentences = []
        negative_sentences = []


     
        for row in tqdm(reader):
            
        
            if (row!=[]):
                if row[0]=="Wymaga uzupełnienia.":
                    continue
                
                
             
                if float(row[1]) > upper:
                    positive_sentences.append(row[0])
                elif float(row[1]) <= lower:
                    negative_sentences.append(row[0])
        
        
        with open(positive_file,"a") as text_file:
            text_file.write("\n".join(positive_sentences))


        with open(negative_file,"a") as text_file:
            text_file.write("\n".join(negative_sentences))


        















class confusion_matrix(object):
    TP=0
    TN=0
    FP=0
    FN=0
    def __init__(self):
        self.TP=0
        self.TN=0
        self.FP=0
        self.FN=0



    def print_results(self):
        print("\n\n\n"+" C O N F U S I O N      M A T R I X" + "\n")
        print("True Positives: " + str(self.TP))
        print("True Negatives: " + str(self.TN))
        print("False Positives: " + str(self.FP))
        print("False Negatives: " + str(self.FN))
        print("\n")
        print("sensitivity: " + str(self.TP/(self.TP + self.FN)))
        print("specitivity: " + str(self.TN / (self.TN + self.FP)))
        print("precison: " + str(self.TP / (self.TP + self.FP)))
        print("accuracy: " + str((self.TP + self.TN) / (self.TP + self.TN + self.FP + self.FN)))


    def save_results(self):
        file = open('matrix_log.txt','a') 
        file.write("/n")
        file.write(time.strftime('%d/%m/%Y'))
        
        
        file.write("\n\n\n"+" C O N F U S I O N      M A T R I X  " +time.strftime('%d/%m/%Y ')+time.strftime("%H:%M:%S")+ "\n")
        file.write("\nTrue Positives: " + str(self.TP))
        file.write("\nTrue Negatives: " + str(self.TN))
        file.write("\nFalse Positives: " + str(self.FP))
        file.write("\nFalse Negatives: " + str(self.FN))
        file.write("\n")
        file.write("\nsensitivity: " + str(self.TP/(self.TP + self.FN)))
        file.write("\nspecitivity: " + str(self.TN / (self.TN + self.FP)))
        file.write("\nprecison: " + str(self.TP / (self.TP + self.FP)))
        file.write("\naccuracy: " + str((self.TP + self.TN) / (self.TP + self.TN + self.FP + self.FN)))
       
         
        file.close() 

