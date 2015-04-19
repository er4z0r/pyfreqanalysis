# -*- coding: utf-8 -*-
# Author: Tilman Bender tilman.bender@rub.de
import math

class Mapper(object):

    def __init__(self):
        self.substitutions = {} 

    def add_mapping(self, cipher, plain):
        try:
            #print "New mapping: %s (%.2f) --> %s (%.2f)" % (cipher,self.symbol_freqs[cipher], plain, self.symbol_ref[plain])
            old = []
            for rule in self.substitutions.keys():
                if self.substitutions[rule] == plain:
                    print u"WARNING: Existing mapping %s --> %s will be deleted" % (rule, self.substitutions[rule])
                    old += rule
            for rule in old:
                del self.substitutions[rule]
            if cipher in self.substitutions:
                    print u"WARNING: Exisiting mapping %s --> %s will be deleted" % (cipher, self.substitutions[cipher])
            self.substitutions[cipher] = plain
        except KeyError as e:
            print e.strerror

    def has_mapping_from(self,cipher):
        return cipher in self.substitutions

    def has_mapping_to(self, plain):
        return plain in self.substitutions.values()

    def remove_mapping(self, cipher):
        del self.substitutions[cipher]

    def get_mapping_from(self, cipher):
        return self.substitutions[cipher]

    def get_mapping_to(self,plain):
        for (key,value) in self.substitutions.items():
            if value == plain: 
                return key

    def get_mappings(self):
        liste = self.substitutions.keys()
        liste.sort()
        mappings = [(cipher,self.substitutions[cipher]) for cipher in liste]
        return mappings

    def load_mappings(self,filename):
        #read file line by line
        f = open("mappings/"+filename+".map");
        lines = f.readlines()
        for l in lines:
            m = l[:-1].split(":")
            self.add_mapping(m[0],m[1])
        f.close()

    def store_mappings(self,filename):
        #open file
        f = open("mappings/"+filename+".map","w");
        #store mappping
        mappings = [(cipher,self.substitutions[cipher]) for cipher in self.substitutions.keys()]
        for m in mappings:
            f.write("%s:%s\n"%(m[0],m[1]))
        f.close()

    def show_mappings(self):
        print u"===== Codebook ======"
        print u"= Cipher =\t = Plain ="
        for m in self.get_mappings():
            print u"%s --> %s " % (m[0], m[1])

    def get_candidate(self, reference, actual, symbol):
        ref_freqs = reference.get_letter_freqs()
        freq = actual.get_letter_freq(symbol)
        differences = [(x[0], abs(float(freq)-float(x[1]))) for x in ref_freqs]
        candidate = min(differences, key=lambda x: x[1])
        print differences
        return candidate[0]

    def generate_candidates(self,reference,actual,n=5):
        #create a list of pairs from symbolFrequencies
        cipher = actual.get_letter_freqs()
        #sort the list by most frequent letter (descending)
        cipher = sorted(cipher, key=lambda x: x[1], reverse=True)
        for i in range(n):
            symbol = cipher[i][0]
            self.add_mapping(symbol,self.get_candidate(reference, actual, symbol ))

    def generate_mappings(self,reference,actual,n=5):
        #create a list of pairs from symbolReference
        plain = reference.get_letter_freqs()
        #create a list of pairs from symbolFrequencies
        cipher = actual.get_letter_freqs()
        #sort the list by most frequent letter (descending)
        plain = sorted(plain, key=lambda x: x[1], reverse=True)
        cipher = sorted(cipher, key=lambda x: x[1], reverse=True)
        #map the n most frequent letters in the ciphertext-alphabet to the n most frequent in the plaintext-alphabet
        for i in range(n):
            self.add_mapping(cipher[i][0], plain[i][0])
        
    def generate_bigram_mappings(self,reference,actual,n=5):
        plain = reference.get_bigram_freqs() 
        if(n>len(plain)):
            n = len(plain)
        cipher = actual.get_bigram_freqs()

        plain = sorted(plain, key=lambda x: x[1], reverse=True)
        cipher = sorted(cipher, key=lambda x: x[1], reverse=True)
        print cipher
        print plain

        for i in range(n):
            print u"Proposed bigram-mapping: %s --> %s" % (cipher[i][0],plain[i][0])
            for letter in cipher[i][0]:
                if self.has_mapping(letter):
                    print u"We already have a mapping for %s: %s --> not adding "  % (letter, self.get_mapping_from(letter))
                else:   
                    print u"No mapping defined for %s" % letter     
            #self.add_mapping(cipher[i][0], plain[i][0])
        #self.mapper.show_mappings(

    def swap_mappings(self, a, b):
        a_old = self.get_mapping_from(a)
        self.add_mapping(a,self.get_mapping_from(b))
        self.add_mapping(b,a_old)
# m = Mapper()
# m.add_mapping('A','B')
# print m.get_mappings()
# print m.has_mapping_from('A')
# print m.has_mapping_to('B')
# print m.get_mapping_from('A')
# print m.get_mapping_to('B')