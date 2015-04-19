# -*- coding: utf-8 -*-
# Author: Tilman Bender tilman.bender@rub.de

class ReferenceModel(object):

    def __init__(self,language):
        self.language=language
        self.symbol_freq = {}
        self.bigram_freq = {}
        self.trigram_freq = {}

    def get_letter_freq(self,letter):
        return self.symbol_freq[letter]

    def get_letter_freqs(self):
        return self.symbol_freq.items()

    def get_bigram_freq(self,bigram):
        return self.bigram_freq[bigram]

    def get_trigram_freqs(self):
        return self.bigram_freq.items()

    def get_trigram_freq(self,trigram):
        return self.trigram_freq[trigram]

    def get_trigram_freqs(self):
        return self.trigram_freq.items()

    def size(self):
        return len(self.symbol_freq.keys())

    def show_letter_freqs(self):
        print "=== Letter Frequencies for %s ===" % self.language.capitalize()
        freqs = self.get_letter_freqs()
        freqs = sorted(freqs, key=lambda x: x[1],reverse=True)
        for f in freqs :
            print u"\t{}\t({:6.2f}%) {}".format(f[0],f[1],'#'*int(f[1]*10))

        # for i in range(0,len(letters)):
        #     lines[i%len(lines)] += u"\t{} ({:.2f} %)".format(letters[i], self.symbol_freq[l[letters]])
        # for line in lines:
        #     print line
    
    @classmethod
    def for_language(cls,language):
        m = ReferenceModel(language)
        m.symbol_freq = ReferenceModel.load_reference_freqs("frequencies/"+language+"/letters.freq")
        m.bigram_freq = ReferenceModel.load_reference_freqs("frequencies/"+language+"/bigrams.freq")
        return m

    @classmethod
    def load_reference_freqs(cls,filename):
#       try:
        f = open(filename)
        lines = f.readlines()
        refs = {}
        for l in lines:
            f = l.split(':')
            refs[unicode(f[0])]= float(f[1])
        return refs
#       except:
#           print "Problem loading frequencies for language %s" % language