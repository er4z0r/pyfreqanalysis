# -*- coding: utf-8 -*-
# Author: Tilman Bender tilman.bender@rub.de
import re
import string
from reference import ReferenceModel

class AnalysisModel(object):

    def __init__(self,filename,text):
        self.filename = filename
        self.text = text
        #map that stores the absolute frequencies of letters in the ciphertext
        #init the dictionary with 0s
        self.symbol_counts = dict.fromkeys(unicode(string.ascii_uppercase),0.0)
        # #map that stores the frequency model for the ciphertext
        # #init the dictionary with 0s
        self.symbol_freqs = dict.fromkeys(unicode(string.ascii_uppercase),0.0)
        #blacklist of punctuation characters
        self.blacklist = [u"É",u"!", u".", u",", u"|", u"?", u":", u";",u"+", u"-",u"\"",u"§",u"$",u"%",u"&",u"/",u"(",u")",u"=",u"[",u"]",u"{",u"}",u"@",u"1",u"2",u"3",u"4",u"5",u"6",u"7",u"8",u"9",u"0"]
        
        self.word_counts = {}
        self.word_freqs = {}    
        
        self.bigram_counts = {}
        self.bigram_freqs = {}
        
        self.trigram_counts = {}
        self.trigram_freqs = {}

        self.repeat_counts = {}
        self.repeat_freqs = {}

    def get_letter_freq(self,letter):
        return self.symbol_freqs[letter]

    def get_letter_freqs(self):
        return self.symbol_freqs.items()

    def get_bigram_freq(self,bigram):
        return self.bigram_freqs[bigram]

    def get_bigram_freqs(self):
        return self.bigram_freqs.items()

    def get_trigram_freq(self,trigram):
        return self.trigram_freqs[trigram]

    def get_trigram_freqs(self):
        return self.trigram_freqs.items()

    def get_repeat_freqs(self):
        return self.repeat_freqs.items()

    def show_letter_freqs(self):
        print "=== Symbol Frequencies in %s ===" % self.filename
        freqs = self.get_letter_freqs()
        freqs = sorted(freqs, key=lambda x: x[1],reverse=True)
        for f in freqs :
            print u"\t{}\t({:6.2f}%) {}".format(f[0],f[1],'#'*int(f[1]*10))

    def show_repeat_freqs(self):
        print "=== Repeat Frequencies in %s ===" % self.filename
        freqs = self.get_repeat_freqs()
        freqs = sorted(freqs, key=lambda x: x[1],reverse=True)
        for f in freqs :
            print u"\t{}\t({:6.2f}%)".format(f[0],f[1])

    def count_bigram(self, bigram):
        #print u"Found bigram: %s" % bigram
        if not bigram in self.bigram_counts:
            self.bigram_counts[bigram] = 1.0
        else:
            self.bigram_counts[bigram] += 1.0

    def count_trigram(self, trigram):
        #print u"Found trigram %s" % trigram
        if not trigram in self.trigram_counts:
            self.trigram_counts[trigram]  = 1.0
        else:   
            self.trigram_counts[trigram] += 1.0

    def count_repeat(self, repeat):
        if not repeat in self.repeat_counts:
            self.repeat_counts[repeat]  = 1.0
        else:   
            self.repeat_counts[repeat] += 1.0
    
    def calculate_relative_freqs(self):
        for symbol in self.symbol_counts.keys():
            self.symbol_freqs[symbol] = self.symbol_counts[symbol]  / sum(self.symbol_counts.values()) * 100
        
        for bigram in self.bigram_counts.keys():
            self.bigram_freqs[bigram] = self.bigram_counts[bigram] / sum(self.bigram_counts.values()) * 100
        
        for trigram in self.trigram_counts.keys():
            self.trigram_freqs[trigram] = self.trigram_counts[trigram] / sum(self.trigram_counts.values()) * 100

        for repeat in self.repeat_counts.keys():
            self.repeat_freqs[repeat] = self.repeat_counts[repeat] / sum(self.repeat_counts.values()) * 100
        
        for word in self.word_counts.keys():
            self.word_freqs[word] = self.word_counts[word] / sum(self.word_counts.values()) * 100

    def show_text(self):
        print self.text

    @classmethod
    def from_file(cls,filename,reference):
        f = open(filename, 'r')
        ciphertext = f.read()
        ciphertext = ciphertext.decode('utf-8')
        ciphertext = ciphertext.lower()
        f.close()
        return AnalysisModel.from_text(filename,ciphertext,reference)

    @classmethod
    def from_text(cls,name,text,reference):
        ws = re.compile('\S')
        model = AnalysisModel(name,text)
        word =u''
        bigram =u''
        trigram =u''
        for symbol in text:
            #if it is not a whitespace or punctuation symbol
            if ws.match(symbol) and not symbol in model.blacklist:
                #print u"Found a letter: %s" % symbol
                word += symbol
                bigram += symbol
                trigram += symbol
                #once we read 2 characters we have a bigram
                if len(bigram) == 2:
                    model.count_bigram(bigram)
                    if bigram[0] == bigram[1]:
                        model.count_repeat(bigram)
                    #any new bigram starts with the last letter of the previous bigram (overlap)
                    bigram=bigram[1:]


                #once we read 3 characters we have a trigram
                if len(trigram) == 3:
                    model.count_trigram(trigram)
                    #any new trigram starts with the last two letters of the previous trigram (overlap)
                    trigram = trigram[1:]
        
                if not symbol in model.symbol_counts:
                    model.symbol_counts[symbol] = 1.0
                else:
                    model.symbol_counts[symbol]  += 1.0
            else:
                #print u"Found something else: %s" % symbol 
                #print u"Current word: %s" % word
                if len(word) > 0:
                    if not word in model.word_counts:
                        model.word_counts[word] = 1.0
                    else:
                        model.word_counts[word] += 1

                #the end of a word is also the end of any n-gram
                word=u''
                bigram = u''
                trigram = u''
        #print self.symbol_counts
        model.calculate_relative_freqs()
        print u"Ciphertext contains %d letters and %d words" % (sum(model.symbol_counts.values()), sum(model.word_counts.values()))
        #since the encryption/decryption is a bijection, ciphertext-alphabet and plaintext-alphabet must be of same size    
        if len(model.symbol_counts.keys()) != reference.size():
            print u"WARNING: Size of ciphertext-alphabet and referenced plaintext-alphabet do not match!"
        return model