# -*- coding: utf-8 -*-
# Author: Tilman Bender tilman.bender@rub.de
import string
import pprint
import re
import sys
from mapper import Mapper
from reference import ReferenceModel
from analysis import AnalysisModel

class Cryptsession(object):
    def __init__(self):
#TODO Move frequency stuff to two separate models of same type. one for reference and one for ciphertext
        #map that stores the frequeny model for the plainText
        #self.symbol_ref = {}
        #self.bigram_ref = {}
        #load the reference frequencies from frequencies/<language>/
        self.reference = ReferenceModel.for_language("english")
        
        #map that stores the absolute frequencies of letters in the ciphertext
        #init the dictionary with 0s
        # self.symbol_counts = dict.fromkeys(unicode(string.ascii_uppercase),0.0)
        # #map that stores the frequency model for the ciphertext
        # #init the dictionary with 0s
        # self.symbol_freqs = dict.fromkeys(unicode(string.ascii_uppercase),0.0)
        #map to store the assumed mappings between symbol in ciphertext and symbol in plaintext
        #self.substitutions = {}    
        self.mapper = Mapper()

        #blacklist of punctuation characters
        # self.blacklist = [u"É",u"!", u".", u",", u"|", u"?", u":", u";",u"+", u"-",u"\"",u"§",u"$",u"%",u"&",u"/",u"(",u")",u"=",u"[",u"]",u"{",u"}",u"@",u"1",u"2",u"3",u"4",u"5",u"6",u"7",u"8",u"9",u"0"]
        # #map that stores absolute word frequencies
        # self.word_counts = {}
        # self.word_freqs = {}    
        # self.bigram_counts = {}
        # self.bigram_freqs = {}
        # self.trigram_counts = {}
        # self.trigram_freqs = {}    
   
    def show_most_frequent_symbols(self,n=5):
        smbls = self.ciphertext.get_letter_freqs()
        smbls = sorted(smbls, key=lambda x: x[1], reverse=True)
        print "=== %d most frequent symbols ===" % n
        for i in range(n):
            symbol = smbls[i][0]
            out = u"{} ({:.2f} %)".format(symbol.upper(), smbls[i][1]) 
            #if there is a known mapping, print it
            if self.mapper.has_mapping_from(symbol):
                plain = self.mapper.get_mapping_from(symbol)
                out += u" --> {} ({:.2f} %)".format(plain.lower(), self.reference.get_letter_freq(plain))
            print out
    
    def show_most_frequent_bigrams(self,n=5):
        bgrms = self.ciphertext.get_bigram_freqs()
        bgrms = sorted(bgrms, key=lambda x: x[1], reverse=True)
        print "=== %d most frequent bigrams ===" %n
        for i in range(n):
            bgrm = bgrms[i][0]
            out = u"{} ({:.2f} %)".format(bgrm.upper(), bgrms[i][1])
            #print bigram mapping (using current mappings)
            plainbgrm=u""
            #for each letter in the bigram
            for symbol in bgrm:
                #check if we have a mapping
                if self.mapper.has_mapping_from(symbol):
                    plainbgrm+=self.mapper.get_mapping_from(symbol)
                else:
                    #if we do not have a mapping use ?
                    plainbgrm+=u"?"
            #if none of the bigram letters has a mapping don't show bigram-mapping
            if plainbgrm.count(u"?") < len(bgrm):
                out+= u" --> {}".format(plainbgrm.lower())
            print out   
    
    def show_most_frequent_trigrams(self, n=5):
        trgrms = self.ciphertext.get_trigram_freqs()
        trgrms = sorted(trgrms, key=lambda x: x[1], reverse=True)
        print "=== %d most freqent trigrams ===" %n
        for i in range(n):
            trgrm = trgrms[i][0]
            out = u"{} ({:.2f} %)".format(trgrm.upper(), trgrms[i][1])
            #print trigram mapping (using current mappings)
            plaintrgrm=u""
            #for each letter in the trigram
            for symbol in trgrm:
                #check if we have a mapping
                if self.mapper.has_mapping_from(symbol):
                    plaintrgrm+=self.mapper.get_mapping_from(symbol)
                else:
                    #if we do not have a mapping use ?
                    plaintrgrm+=u"?"
            #if none of the trigram letters has a mapping don't show trigram-mapping
            if plaintrgrm.count(u"?") < len(trgrm):
                out+= u" --> {}".format(plaintrgrm.lower())
            print out
    
    def show_most_frequent_words(self, n=5):
        cwords = self.c.word_counts.items()
        cwords = sorted(cwords, key=lambda x: x[1], reverse=True)
        print "=== %d most frequent words ===" % n
        for i in range(n):
            word = cwords[i][0]
            out = u"{} ({:.2f} %)".format(word.upper(), cwords[i][1])
            #print word mapping (using current mappings)
            plainword=u""
            #for each letter in the word
            for symbol in word:
                #check if we have a mapping
                if self.mapper.has_mapping_from(symbol):
                    plainword+=self.mapper.get_mapping_from(symbol)
                else:
                    #if we do not have a mapping use ?
                    plainword+=u"?"
            #if not at least half of the letters have a mapping don't show word-mapping
            if plainword.count(u"?") <= len(word)/2:
                out+= u" --> {}".format(plainword.lower())
            print out


    
    def show_plaintext(self):
        decrypted = '' 
        for symbol in self.ciphertext.text:
                #check if there is a substitution-rule
                if self.mapper.has_mapping_from(symbol):
                    #use it
                    decrypted += self.mapper.get_mapping_from(symbol).lower()
                else:
                    #use letter from ciphertext instead
                    decrypted += symbol
        print decrypted

    def show_menu(self):
        choice =u''
        while True:
            print "======== Available Actions ========"
            print "[0] Read ciphertext from file"
            print "[1] Show ciphertext"
            #print "[2] Analyse ciphertext"
            print "[3] Show reference frequencies (symbols)"
            #TODO Show absolute frequencies
            print "[4] Show ciphertext frequencies (symbols)"
            print "[5] Shwo n most frequent symbols"
            print "[6] Show n most frequent bigrams"
            print "[7] Show n most frequent trigrams"
            print "[8] Show n most frequent words"
            print "[9] Create n substitution rules using symbol-frequencies "
            print "[10] Define substitution rule for ciphertext -> plaintext"
            print "[11] Remove substitution rule"
            print "[12] Show substitution rules"
            print "[13] Show decrypted text (uses substitution rules)"
            print "==================================="
            choice = input("Please choose: ")
            try:
                if choice == 0:
                    fn = raw_input("Path to ciphertext: ")
                    lan = raw_input("Language of ciphertext (german/english): ")
                    self.reference = ReferenceModel.for_language(lan)
                    self.ciphertext = AnalysisModel.from_file(fn,self.reference)
                    self.show_most_frequent_symbols()
                    self.show_most_frequent_bigrams()
                    self.show_most_frequent_trigrams()
                elif choice == 1:
                    self.ciphertext.show_text()
                elif choice == 2:
                    self.analyze()
                elif choice == 3:
                    self.reference.show_letter_freqs()
                elif choice == 4:
                    self.ciphertext.show_letter_freqs()
                elif choice == 5:
                    n = raw_input("n: ").decode(sys.stdout.encoding)
                    self.show_most_frequent_symbols(int(n))
                elif choice == 6:
                    n = raw_input("n: ").decode(sys.stdout.encoding)
                    self.show_most_frequent_bigrams(int(n))
                elif choice == 8:
                    n = raw_input("n: ").decode(sys.stdout.encoding)
                    self.show_most_frequent_words(int(n))
                elif choice == 7:
                    n = raw_input("n: ").decode(sys.stdout.encoding)
                    self.show_most_frequent_trigrams(int(n))
                elif choice == 9:
                    n = raw_input("n: ").decode(sys.stdout.encoding)
                    self.mapper.generate_mappings(self.reference,self.ciphertext,int(n))
                elif choice == 10:
                    ciph = raw_input("From: ").decode(sys.stdout.encoding)
                    plain = raw_input("To: ").decode(sys.stdout.encoding)
                    self.mapper.add_mapping(ciph, plain)
                elif choice == 11:
                    ciph = raw_input("Remove substitution for which letter?").decode(sys.stdout.encoding)
                    self.mapper.remove_mapping(ciph)
                elif choice == 12:
                    self.mapper.show_mappings()
                elif choice == 13:
                    self.show_plaintext()
                elif choice == 14:
                    fn = raw_input("filename: ").decode(sys.stdout.encoding)
                    self.mapper.load_mappings(fn)
                elif choice == 15:
                    fn = raw_input("filename: ").decode(sys.stdout.encoding)
                    self.mapper.store_mappings(fn)
                elif choice == 16:
                    self.mapper.generate_candidates(self.reference, self.ciphertext)
                elif choice == 'q':
                    system.exit(0)
                else:
                    print "Unknown option"
            except:
                raise

                

session1 = Cryptsession()
session1.show_menu()
