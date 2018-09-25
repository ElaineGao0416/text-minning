# encoding=utf-8

import nltk
from nltk.corpus import sinica_treebank	# 带标注的中文语料库
import re

# 用print输出本地字符格式
def dump_result(result):
    for item in result:
        print item[0],",",item[1],
    print
    
# 等标注的词，以空格分词（分词问题不在此讨论）
raw = '讓 人工 智能 能夠 更 有效地 甄別 虛假 和 低俗 內容 並 控制 其 傳播 是 當前 業界 和 學界 要 重點 研究 的 問題'.decode('utf-8')
tokens = nltk.word_tokenize(raw)

sinica_treebank_tagged_sents = sinica_treebank.tagged_sents()	# 以句为单位标
size = int(len(sinica_treebank_tagged_sents) * 0.9)
train_sents = sinica_treebank_tagged_sents[:size]	# 90% 数据作为训练集
test_sents = sinica_treebank_tagged_sents[size:]	# 10% 数据作为测试集

t0 = nltk.DefaultTagger('Nab')	# 词性的默认值为名词
t1 = nltk.UnigramTagger(train_sents, backoff=regexp_tagger)	# 一元标注
t2 = nltk.BigramTagger(train_sents, backoff=t1)	# 多元（二元）标注

dump_result(t2.tag(tokens))
print t2.evaluate(test_sents)	# 根据带标注的文本，评估标注器的正确率

from nltk.tag import DefaultTagger
default_tagger = DefaultTagger('NN')
list(default_tagger.tag('This is a test'.split()))


patterns = [
	(r'.*\xe6\x9c\x88$', 'Ndabc'),
	(r'.*\xe6\x97\xa5$', 'Ndabc'), 
	(r'.*\xe5\xa4\xa9$', 'Ndabc'), 
	(r'.*\xe5\x8d\x88$', 'Ndabc'), 
	(r'.*\xe7\x82\xb9$', 'Ndabc'), 
	(r'.*\xe5\x88\x86$', 'Ndabc')]

regexp_tagger = nltk.RegexpTagger(patterns)
regexp_tagger.tag(tokens)
[('``', 'NN'), ('Only', 'NN'), ('a', 'NN'), ('relative', 'NN'), ('handful', 'NN'),('of', 'NN'), ('such', 'NN'), ('reports', 'NNS'), ('was', 'NNS'), ('received', 'VBD'),
("''", 'NN'), (',', 'NN'), ('the', 'NN'), ('jury', 'NN'), ('said', 'NN'), (',', 'NN'),('``', 'NN'), ('considering', 'VBG'), ('the', 'NN'), ('widespread', 'NN'), ...]
 regexp_tagger.evaluate(brown_tagged_sents)


unigram_tagger = nltk.UnigramTagger(k, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(k, backoff=unigram_tagger)

unigram_tagger.tag(tokens)
