import re
from collections import Counter,defaultdict 		
import numpy as np

words_sv = re.findall(r'\w+', open('/content/europarl-v7.sv-en.lc.sv').read())
words_en = re.findall(r'\w+', open('/content/europarl-v7.sv-en.lc.en').read())

"""### **(a) Warmup**"""

words_freq_sv = Counter(words_sv)
words_freq_en = Counter(words_en)
total_words_sv = sum(words_freq_sv.values())
total_words_en = sum(words_freq_en.values())
print("10 most frequent words in English language")
print(words_freq_en.most_common(10))
print("10 most frequent words in Swedish language")
print(words_freq_sv.most_common(10))
print("\nThe probability that randomly picked word is 'speaker'")
print((words_freq_en['speaker']/total_words_en) +( words_freq_sv['speaker']/total_words_sv))
print("The probability that randomly picked word is 'zebra'")
print((words_freq_en['zebra']/total_words_en) +( words_freq_sv['zebra']/total_words_sv))

"""### **(b) Language modeling**"""

def cal_prob_bigram(bigram_freq,words_freq):
  prob = {}
  for bigram in bigram_freq.items():
    prob[bigram[0]] = bigram[1]/words_freq[bigram[0][0]]
  return prob

def cal_prob_sentence(input_string,bigram_prob ):
  list_words=input_string.split(' ')
  bigram_list = [(list_words[i],list_words[i+1]) for i in range(len(list_words)-1)]
  prob_sentence = 1
  count_bigrams_common = 0
  for bi in bigram_list:
    if bi in bigram_prob:
      count_bigrams_common+=1
      prob_sentence *= bigram_prob[bi]
  if(count_bigrams_common==0):
    prob_sentence = 0
  return prob_sentence

data =  open('/content/europarl-v7.sv-en.lc.en').read().split(' ')
bigram_freq = Counter((data[idx],data[idx+1]) for idx in range(len(data) - 1)) 
words_freq = Counter(data)
bigram_prob = cal_prob_bigram(bigram_freq, words_freq)

input1 ="sweety if you  wish"
input2 = "sweety thank you"
input3 = "at the request of a french member , mr zimeray , a petition has already been presented , which many people signed , including myself . however , i would ask you , in accordance with the line which is now constantly followed by the european parliament and by the whole of the european community , to make representations , using the weight of your prestigious office and the institution you represent , to the president and to the governor of texas , mr bush , who has the power to order a stay of execution and to reprieve the condemned person .this is all in accordance with the principles that we have always upheld ."
input4 = "I like zebra"

print("Probabilities of different sentences: ")
print(input1)
print(cal_prob_sentence(input1,bigram_prob))
print('\n')
print(input2)
print(cal_prob_sentence(input2,bigram_prob))
print('\n')
print(input3)
print(cal_prob_sentence(input3,bigram_prob))
print('\n')
print(input4)
print(cal_prob_sentence(input4,bigram_prob))
print('\n')

"""### **(c) Translation modeling**"""

eng = open('/content/europarl-v7.sv-en.lc.en').read()
sve = open('/content/europarl-v7.sv-en.lc.sv').read()

eng_sentences = eng.split('\n')[:10000]
#eng_sentences.pop()
sve_sentences = sve.split('\n')[:10000]
#sve_sentences.pop()

t  =  defaultdict ( float )

for i in range(len(eng_sentences)):
  e = eng_sentences[i]
  s = sve_sentences[i]
  eng_words = list(set(e.split()))
  sve_words = list(set(s.split()))
  eng_words.append("NULL")
  for each_s in sve_words:
    for each_e in eng_words:
      t [( each_s, each_e  )] =  1.0

def get_top(t,word,count):
  dict_ = dict( filter(lambda elem: elem[0][1] == word, t.items()))
  dict_sorted = dict(sorted(dict_.items(), key=lambda item: item[1],reverse=True))
  return(list(dict_sorted.items())[:count])

num_iterations = 5
for ite in range(num_iterations):
  count  =  defaultdict ( float )
  total_e  =  defaultdict ( float )
  total_s  =  defaultdict ( float )
  for i in range(len(eng_sentences)):
    e = eng_sentences[i].split(' ')
    s = sve_sentences[i].split(' ')
    
    for s_word in s:
      #print(s_word)
      total_s [ s_word ] =  0.0
      for e_word in e:
        total_s [ s_word ] +=  t [(s_word  , e_word )]

    for s_word in s:
      for e_word in e:
        sigma = t [(s_word  , e_word )]/total_s[ s_word ] # Compute alignment prob.
        count[(e_word  , s_word )] += sigma # Update pseudocount
        total_e[e_word]+= sigma # Update pseudocount

t

"""### **(d) Decoding**"""

input = "thank you"
list_input = input.split(" ")
output = []
for l in list_input:
  sve_word = get_top(t,l,1)
  output.append(sve_word[0][0][0])
print(" ".join(output))

