from pypinyin import pinyin, lazy_pinyin
from fuzzywuzzy import fuzz 
import pypinyin
import jieba
import jieba.posseg as pseg
jieba.initialize()
from thulac import thulac
from collections import Counter
from gensim.models.word2vec import Word2Vec
# from gensim.models.word2vec import LineSentence  
import codecs
import os
import re
import itertools
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# soundex = fuzzy.Soundex(3) 
# a = " ".join(lazy_pinyin(u'无形'))
# b = " ".join(lazy_pinyin(u'无心'))
# fuzz.token_sort_ratio(a,b)
# fuzz.token_set_ratio(a,b)
# fuzz.ratio(a,b)
# fuzz.token_set_ratio(u'无锡',u'无心')

# words = pseg.cut("/".join(text2[600:700]))
# for word, flag in words:
# 	print word,flag

# from jieba.analyse import ChineseAnalyzer
# analyzer = ChineseAnalyzer()
# data = ' '.join([i.text for i in analyzer(text)])

text = codecs.open('/Users/zp/Desktop/nlp/SHARE_NLP/07','r','utf-8').read().encode('utf8')
text = u'未来的事物总会有所变化，今天，我就来给大家介绍一下未来的智能汽车。\
　　未来的汽车华丽而又实用，是驾驶人不可离开的交通工具，未来的汽车一律都是一个牌子的——保时捷，瞧，我爸爸要开车啦!\
　　我和爸爸坐上车，按了一下一个蓝色的按钮，汽车就启动了，从导航里传出优雅的女声：“主人你好，请问要去何处?”“去陡水湖。”爸爸对导航说，\
	立刻，我们的座椅往后拉到最低，安全带自动系上，原来导航可以自动驾驶啊，到了目的地，我们还没察觉，叮——，闹钟声把我们叫醒了，我们下了车。\
　　要回家了，导航又自动返回。\
　　嘻嘻，未来的汽车怎么样啊?'


#定义字典
renewable_dict = '/Users/zp/Desktop/nlp/SHARE_NLP/dict.txt'
address_dict = '/Users/zp/Desktop/nlp/SHARE_NLP/address_dict/'
jieba_stop_word = '/Users/zp/Desktop/nlp/SHARE_NLP/stopword.txt'
textrank4zh_stop_word = '/Users/zp/Desktop/nlp/SHARE_NLP/stopword.data'

#导入辞典
jieba.load_userdict(renewable_dict)
load_address_dict(address_dict)
jieba.analyse.set_stop_words(jieba_stop_word)
stopword = codecs.open(jieba_stop_word, 'r', 'utf-8').read()
stopword_path = textrank4zh_stop_word

#
thulac_find_rspell(text,path='/Users/zp/Desktop/08test',seg_only=False, filt=True,size=600, window=6, min_count=1, workers=4,sg=1)
jieba_fine_rspell(text,path='/Users/zp/Desktop/08test1',size=600, window=8, min_count=1, workers=7,sg=0)
text = find_wrong_spell(path='/Users/zp/Desktop/08test',text=text)

def thulac_find_rspell(text,path='/Users/zp/Desktop/08test',seg_only=False, filt=True,size=600, window=6, min_count=1, workers=4,sg=1):
	thu = thulac(user_dict=None, model_path=None, T2S=False, seg_only=seg_only, filt=filt)
	model = Word2Vec(text.encode("utf8"), size=size, window=window, min_count=min_count, workers=workers,sg=sg)
	##分词	
	all_words = []
	only_word = []
	words = thu.cut(text.encode("utf8"))
	for i in words:
		all_words.append((i[0],i[1]))
		only_word.append(i[0])
	cnt_word = Counter(only_word)
	#笛卡尔积
	sample = list(set(all_words))
	for i in itertools.product(range(len(sample)), range(len(sample))):
		if i[0] < i[1]:
			if sample[i[0]][1] != 'ns' and sample[i[0]][1] != 'nr' and sample[i[1]][1] != 'ns' and sample[i[1]][1] != 'nr':
				a = sample[i[0]][0].decode('utf8')
				b = sample[i[1]][0].decode('utf8')
				unicode = fuzz.token_set_ratio(a,b)
				c = " ".join(lazy_pinyin(a))
				d = " ".join(lazy_pinyin(b))
				pinyin1 = fuzz.ratio(c,d)
				pinyin = fuzz.token_set_ratio(c,d)
				if cnt_word[a.encode('utf8')] < 4:
					if len(a) == len(b)  and len(a) > 1 and a != b :
	 					if unicode == 0 and pinyin > 92 and pinyin1 > 94:
	 						simi = model.wv.n_similarity(a.encode('utf8'), b.encode('utf8'))
	 						if simi > 0.5:
	 							a_num = cnt_word[a.encode('utf8')]
	 							b_num = cnt_word[b.encode('utf8')]
								print a,a_num,b,b_num
								print simi
								if a_num < b_num:
									write_file(path=path,wrong_word=a,ww_num=a_num,right_word=b,rw_num=b_num,simi=simi)
								else:
									write_file(path=path,wrong_word=b,ww_num=b_num,right_word=a,rw_num=a_num,simi=simi)
		


def jieba_fine_rspell(text,path='/Users/zp/Desktop/08test1',size=600, window=8, min_count=1, workers=7,sg=0):
	##分词
	model = Word2Vec(text.encode("utf8"), size=size, window=window, min_count=min_count, workers=workers,sg=sg)	
	words = pseg.cut(text)
	all_words = []
	only_word = []
	for word,flag in words:
		all_words.append((word,flag))
		only_word.append(word)
	cnt_word = Counter(only_word)
	#笛卡尔积
	sample = list(set(all_words))
	for i in itertools.product(range(len(sample)), range(len(sample))):
		if i[0] < i[1]:
			if sample[i[0]][1] != 'ns' and sample[i[0]][1] != 'nr' \
			and sample[i[1]][1] != 'ns' and sample[i[1]][1] != 'nr' and sample[i[0]][1] != 'm'  and sample[i[1]][1] != 'm':
				a = sample[i[0]][0]
				b = sample[i[1]][0]
				unicode = fuzz.token_set_ratio(a.encode('utf8'),b.encode('utf8'))
				c = " ".join(lazy_pinyin(a))
				d = " ".join(lazy_pinyin(b))
				pinyin1 = fuzz.ratio(c,d)
				pinyin = fuzz.token_set_ratio(c,d)
				if cnt_word[a] < 4:
					if len(a) == len(b)  and len(a) == 2 and a != b :
	 					if unicode == 0 and pinyin > 92 and pinyin1 > 94:
	 						simi = model.wv.n_similarity(a.encode('utf8'), b.encode('utf8'))
	 						if simi > 0.5:
								a_num = cnt_word[a]
	 							b_num = cnt_word[b]
								print a,a_num,b,b_num
								print simi
								if a_num < b_num:
									write_file(path=path,wrong_word=a,ww_num=a_num,right_word=b,rw_num=b_num,simi=simi)
								else:
									write_file(path=path,wrong_word=b,ww_num=b_num,right_word=a,rw_num=a_num,simi=simi)
					elif len(a) == len(b)  and len(a) > 2 and a != b :
						if unicode == 0 and pinyin > 94 and pinyin1 > 97:
	 						simi = model.wv.n_similarity(a.encode('utf8'), b.encode('utf8'))
	 						if simi > 0.7:
	 							a_num = cnt_word[a]
	 							b_num = cnt_word[b]
								print a,a_num,b,b_num
								print simi
								if a_num < b_num:
									write_file(path=path,wrong_word=a,ww_num=a_num,right_word=b,rw_num=b_num,simi=simi)
								else:
									write_file(path=path,wrong_word=b,ww_num=b_num,right_word=a,rw_num=a_num,simi=simi)
	


def write_file(path,wrong_word,ww_num,right_word,rw_num,simi):
	file = open(path,"a+")
	file.write(wrong_word+'|'+str(ww_num)+'|'+right_word+'|'+str(rw_num)+'|'+str(simi)+'\n')
	file.close()



write_file(path='/Users/zp/Desktop/08test1',wrong_word='你好',ww_num=30,right_word='你吗',rw_num=20,simi=0.268)



def define_wrong_spell(old_word,new_word,text):
	p = old_word
	word1 = re.compile(r'\，[^，]+?'+p+'.+?\，')
	sentence1 = word1.findall(text)
	if len(sentence1) == 0:
		word1 = re.compile(r'.+?'+p+'.+?\，')
		sentence1 = word1.findall(text)
	for i in sentence1:
		print i[3:-3] 
		defination = raw_input("Is it right spelled ? (y/n) : ")
		while defination != 'y' and defination != 'n' :
			print "Cannot understand your input!"
			defination = raw_input("Is it right spelled ? (y/n) : ")
		if defination == 'n':
			new = i.replace(old_word,new_word)
			text = text.replace(i,new)
		else:
			continue
	return text



def find_wrong_spell(path,text):
	data = open(path,'r').readlines()
	for line in data:
		ln = line.strip().split("|")
		print 'wrong_word: '+ln[0]
		print 'possible word: '+ln[2]
		text = define_wrong_spell(ln[0],ln[2],text)
	return text




def load_address_dict(address_dict):
	'''导入地理位置字典'''
	files = os.listdir(address_dict)
	for i in files:
		full_address_dict = address_dict+i
		try:
			jieba.load_userdict(full_address_dict)
		except:
			print full_address_dict
			print "file not load!"


'''
# model = Word2Vec(LineSentence(only_word), size=200, window=5, min_count=1, workers=4)
# model = Word2Vec(only_word, size=200, window=4, min_count=1, workers=4,sg=0)
# model.wv.n_similarity( '没有', '没哟')
'''