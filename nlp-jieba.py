import jieba.analyse
import jieba
import jieba.posseg as pseg
import codecs
import re
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from snownlp import SnowNLP
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')


'''
###手动设置单词
###可以手动设置人名
jieba.suggest_freq(('一年', '一交'), True)
jieba.suggest_freq('七月二十日', True)
jieba.del_word('他收了')

###分词
seg_list = jieba.cut(d, cut_all=False)    #显示精确结果
seg_list = jieba.cut(a, cut_all=True)     #显示全部结果
print("Default Mode: " + "/ ".join(seg_list))    
# raw = " ".join(seg_list)

###分布式操作
jieba.enable_parallel(4)
jieba.disable_parallel()

##按照tf-idf提取关键词
jieba.analyse.tfidf
'''


'''
##测试用样本
a = u"四月十五号，我家的路由器开始发生故障，早上的时候还好，\
就是网速慢一点，下午开始一断一断的，到半个小时以前已经完全连不上了，请过来修理一下。我家住在下沙高教园区学正街20号。"
b = "五月，我们家的路由器最近老是发烫，然后使用超过三个小时以后就自动断开了，要等一个小时左右才能好，已经持续3天了，能不能来解决一下，\
	我的地址是天目山路8号,报错号码是256."
c = u"喂，你好，我要投诉，雅士苑这边的网络信号超差，根本连不上，从上周开始就这样了，\
你们也不管的吗？我已经投诉过一次了，你们都不认真对待，这样糟糕的服务态度，让我感到失望。"
d =u"你好我是西湖区的我在你们这里订购了1年的套餐可是这几天突然断网了是因为我没有交钱吗还是因为别的原因不是一年一交的吗"
f =u'他妈的，老子一年两千块钱的宽带费白交了。果断放弃电信，走移动，走联通，累觉不爱，哎！'
g = u'你好我家宽带突然连不上了，经常这样，时好时坏，你们可不可以派个人过来维修一下，我这周六在家，杭州市拱墅区湖州街浙江大学城市学院。'
e = u'你好，我上午在打王者荣耀的时候，宽带突然断了。请问你们要不要做出补偿，我打的是排位赛。'
h = u'晚上，用手机的时候，突然没网了，后来发现是网断了，但是，路由器上的指示灯还在闪，我也不知道是什么原因，麻烦你们来看一下。'
z = codecs.open('/Users/zp/Desktop/nlp/01', 'r', 'utf-8').read()
i = u"我也是用电信的，哎...有时给他们帮忙解决一点问题，他们推三阻四。真的很让人生气...而且他们的客服一个个都是赵本山的徒弟！‘大忽悠’！！！\
那些维修人员更是可恶至极！！！一个个牛气冲天，让他们来维修还要受一肚子气！！说什么：怎么弄的，这个能这么弄吗？下次再这么弄，不给修！\
什么态度呀？你说。以后不用电信、所有的电信实名制的选择！！"
j = '以前真的好，现在越来越垃圾，一到晚上基本都是卡到你怕，自从AD换了光纤后，晚上7点过后一定卡，12点后你就别想玩什么，\
我以为只是我有这种问题，晚上一搜，原来这问题基本全国普遍，所以你自己掂量。'
i =u'本人现在用的是长城宽带感觉特别垃圾整天卡/(等到下半夜2点钟到8点才好一点点)也就是玩这游戏要等到这时候/'
i =u'曾经有一个说法，北联通，南电信，本人使用的就是电信光纤 速度20兆的，还没开100兆的...感觉上网速度够用 ...  请采纳'
i =codecs.open('/Users/zp/Desktop/nlp/04', 'r', 'utf-8').read()
'''

#step1
#输入样本
text1 = u"四月十五号，我家的路由器开始发生故障，早上的时候还好，\
就是网速慢一点，下午开始一断一断的，到半个小时以前已经完全连不上了，请过来修理一下。我家住在下沙高教园区学正街20号。"
text2 = codecs.open('/Users/zp/Desktop/nlp/05', 'r', 'utf-8').readlines()

#step2
#定义字典
renewable_dict = '/Users/zp/Desktop/nlp/dict.txt'
address_dict = '/Users/zp/Desktop/address_dict/'
jieba_stop_word = '/Users/zp/Desktop/nlp/stopword.txt'
textrank4zh_stop_word = '/Users/zp/Desktop/nlp/stopword.data'

#导入辞典
jieba.load_userdict(renewable_dict)
load_address_dict(address_dict)
jieba.analyse.set_stop_words(jieba_stop_word)
stopword = codecs.open(jieba_stop_word, 'r', 'utf-8').read()
stopword_path = textrank4zh_stop_word


#遍历样本，追加字典内容
for i in range(540,560):
	phrases(text2[i],renewable_dict_path = renewable_dict )

#step3
#导入辞典
jieba.load_userdict(renewable_dict)

#step4
#提取关键词和摘要
train_sample(file=text1,tr4_stopword_path=textrank4zh_stop_word,window = 2,keywords_num = 20,num_sentence = 5)
train_sample(file=b,tr4_stopword_path=textrank4zh_stop_word)
train_sample(file=j,tr4_stopword_path=textrank4zh_stop_word)
for i in range(530,550):
	train_sample(file=text2[i],tr4_stopword_path=textrank4zh_stop_word)



set_rule_for_phrases = (
	("ns","ns","ns","ns","ns","ns"),
	("vn","ns","v","n","v","v","n"),
	("ns","x","ns","n","ns"),
	("nr","nr","nr","nr","ns"),
	("v","n","v","n","n","v"),
	("v","n","n","n","n"),
	("v","v","n","n","v"),
	("v","n","uj","n","v"),
	("v","d","v","v","v"),
	("v","d","v","v","v"),
	("v","v","n","v","v"),
	("v","t","n","ns","v"),
	('n','m','m','m'),
	("t","t","ts","t"),
	("n","v","n","n"),
	("n","v","v","v"),
	("n","v","v","v"),
	("v","n","v","v"),
	("n","d","v","v"),
	("v","nr","n","v"),
	("n","v","n","n"),
	("d","v","v","a"),
	('m','n','n'),
	("v","nr","n"),
	("v","v","v"),
	("nr","n","n"),
	("v","d","v"),
	("t","t","t"),
	("v","n","v"),
	("m","eng","m"),
	("ns","m","m"),	
	("ns","n","ns"),
	("d","v","a"),	
	("n","v","v"),
	("v","v","v"),
	("d","a","a"),
	("v","m","v"),
	("m","tt","tt"),
	('m','m','m'),
	('a','v','a'),
	('v','a','a'))


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


def read_rule(start_place,wrong_phrase,sentence,rule,renewable_dict_path):
	'''自定义字典更新规则'''
	for i in rule:
		new_sentence = []
		for k,v in enumerate(i[:-1]):
			if sentence[start_place+k][1] == v:
				new_sentence.append(sentence[start_place+k][0])
			else:
				break
		if len(new_sentence) > 1 : 
			new_phrases = "".join(new_sentence)
			map_dict(p=new_phrases,wrong_phrase=wrong_phrase,label=i[-1],renewable_dict_path=renewable_dict_path)



def phrases(file,renewable_dict_path='/Users/gaozhiping/Desktop/dict2.txt'):
	'''
	遍历新sample，将新词汇加入辞典
	'''
	wrong_phrase = []
	words = pseg.cut(file)
	sentence = []
	for word, flag in words:
		sentence.append((word,flag))
	for i,v in enumerate(sentence):
		try:
			read_rule(start_place=i,wrong_phrase=wrong_phrase,sentence=sentence,rule=set_rule_for_phrases,renewable_dict_path=renewable_dict_path)
		except:
			continue



def map_dict(p,label,wrong_phrase,renewable_dict_path = '/Users/zp/Desktop/dict2.txt'):
	'''
	添加新词汇到词典中
	'''
	p = p.encode("utf8").replace("\xef\xbc\x8c","").replace(",","").\
	replace("\xe3\x80\x82","").replace("\xef\xbc\x9f","").replace("\xef\xbc\x81","").replace(".","")
	if p not in wrong_phrase:
		out = compile_find(p,label,renewable_dict_path)
		if len(out[0]) == 0 and len(out[1]) == 0:
			print "this is a new word!"
			print  ("the new one is :   " + " ".join([p,label]))
			decision = raw_input("would you add it ? press no can correct it (y/n): ")
			decision = ask_for_decision(decision,question = "would you add it ? press no can correct it (y/n): ")
			if decision == "y" :
				new_line = " ".join([p,label])
				file  = open(renewable_dict_path, 'a+')
				file.write(new_line+'\n')
				file.close()
			elif decision == "n" :
				wrong_phrase.append(p)
				decision2 = raw_input("would you correct it (y/n)?: ")
				decision2 = ask_for_decision(decision2,question = "would you correct it (y/n)?: ")
				if decision2 == 'y':
					newp = raw_input("new word:   ")
					newlabel = raw_input("new tag:   ")
					out2 = compile_find(newp,newlabel,renewable_dict_path)
					if len(out2[0]) == 0 and len(out2[1]) == 0:
						new_line = " ".join([newp.replace(" ",""),newlabel.replace(" ","")])
						file  = open(renewable_dict_path, 'a+')
						file.write(new_line+'\n')
						file.close()
					elif len(out2[0]) != 0 and len(out2[1]) == 0:
						replace_input(newp.replace(" ",""),newlabel.replace(" ",""),finding = out2[0],renewable_dict_path=renewable_dict_path)
					else:
						print "this is not a new word!"
		elif len(out[0]) != 0 and len(out[1]) == 0:
			replace_input(p,label,finding = out[0],wrong_phrase=wrong_phrase,renewable_dict_path=renewable_dict_path)
		else:
			print "this is not a new word!"


def ask_for_decision(decision,question = "would you correct it (y/n)?: "):
	'''输入文字鉴定'''
	while decision != "y" and decision != "n" :
		print "i can't understand your input!"
		print "pleace do ti again!"
		decision = raw_input(question)
	return decision



def replace_input(p,label,finding,wrong_phrase,renewable_dict_path):
	'''修改自定义字典'''
	print "this word has been tagged as another tag!"
	print  ("the old one is :   " +'/'.join(finding))
	print  ("the new one is :   " + " ".join([p,label]))
	decision = raw_input("would you replace it (y/n)?: ")
	decision = ask_for_decision(decision,question = "would you replace it (y/n)?: ")
	if decision == "y" :
		file = open(renewable_dict_path, 'r')
		dict_renew = [i.encode("utf8") for i in file.readlines()]
		file.close()
		for i in finding:
			i = i.encode("utf8")
			try:
				dict_renew.remove(i+'\n')
			except:
				print "wrong finding!"
				new_line = " ".join([p,label])
				file  = open(renewable_dict_path, 'a+')
				file.write(new_line+'\n')
				file.close()
				continue
		new_line = " ".join([p,label])
		dict_renew.append(new_line+"\n")
		file  = open(renewable_dict_path, 'w')
		for line in dict_renew:
			file.write(line)
		file.close()
	else:
		wrong_phrase.append(p)


def compile_find(p,label,renewable_dict_path = '/Users/gaozhiping/Desktop/dict2.txt'):
	'''查找新词是否在字典中存在'''
	file = open(renewable_dict_path, 'r')
	dict_renew = file.readlines()
	file.close()
	p = p.encode("utf8").replace("\xef\xbc\x8c","").replace("\xe3\x80\x82","").replace("\xef\xbc\x9f","")
	target = re.compile(p+r'\s[a-z]+')
	consequence1 = target.findall(",".join([i.strip() for i in dict_renew]))
	combine = re.compile(p+r'\s'+label)
	consequence2 = combine.findall(",".join([i.strip() for i in dict_renew]))
	return (consequence1,consequence2)


def add_punctuations(p):
	'''
	手动加入标点
	精准度不高，建议从数据源就加入标点，尽量不要人工加入
	'''
	words = pseg.cut(p)
	new_sentence = []
	for word, flag in words:
		if flag == 't' or flag == 'ul' or flag == 'y' or flag == 'a' or flag == 'ts' or flag == 'uj' or flag == "st":
			new_sentence.append(word)
			new_sentence.append(u'，')
		elif flag == 'c':
			new_sentence.append(u'。')
			new_sentence.append(word)
		elif flag == 'start':
			new_sentence.append(u'。')
			new_sentence.append(word)
		else:
			new_sentence.append(word)
	return "".join(new_sentence).replace(u"，。",u"，")


def text_file(p):
	'''
	检测数据源师傅包含标点
	'''
	punctuation1 = re.compile(r'\xef\xbc\x8c')
	outp1 = len(punctuation1.findall(p))
	punctuation2 = re.compile(r'\xef\xbc\x9f')
	outp2 = len(punctuation2.findall(p))
	punctuation3 = re.compile(r'\xe3\x80\x82')
	outp3 = len(punctuation3.findall(p))
	if outp1 == outp2 == outp3 == 0 :
		return add_punctuations(p)
	else:
		return p


def train_sample(file,tr4_stopword_path,window = 2,keywords_num = 20,num_sentence = 5):
	'''关键词查找及输出'''
	'''版本1'''
	tr4w = TextRank4Keyword(tr4_stopword_path)
	tr4s = TextRank4Sentence(tr4_stopword_path)
	tr4w.analyze(text=file, lower=True, window=window)  
	tr4s.analyze(text=text_file(file),  lower=True, source = 'all_filters')
	sentence = tr4s.get_key_sentences(num=4)
	ext_tag = jieba.analyse.extract_tags(file, topK=keywords_num,withWeight=False, allowPOS=('n','ns','nse','ne','v','ve','vde','l','a'))
	key_word = [i for i in ext_tag if i.isdigit() == False]
	text_rank1 = jieba.analyse.textrank(file, topK=40, withWeight=False, allowPOS=('tl','tt', 't','tle','ts'))
	key_time = [i for i in text_rank1 if i.isdigit() == False]
	if len(key_time) == 0:
		text_rank1 = jieba.analyse.extract_tags(file, topK=2*keywords_num, withWeight=False, allowPOS=('t','tt','tl','tle'))
		key_time = [i for i in text_rank1 if i.isdigit() == False]
	text_rank2 = jieba.analyse.textrank(file, topK=40, withWeight=False, allowPOS=('ns','nse', 'nz', 'ts','nt','nrt'))
	key_position = [i for i in text_rank2 if i.isdigit() == False]
	if len(key_position) == 0:
		text_rank2 = jieba.analyse.extract_tags(file, topK=2*keywords_num, withWeight=False, allowPOS=('ns','nse', 'nz','nt','nrt'))
		key_position = [i for i in text_rank2 if i.isdigit() == False]
	new_tag = jieba.analyse.tfidf(file, topK=keywords_num,withWeight=False, allowPOS=('tt','ns','n','v','t','a','tl','tle'))
	key_tag = [i for i in new_tag if i.isdigit() == False][:5]
	error = re.compile(r"\xe6\x8a\xa5\xe9\x94\x99+.{1,}[0-9]")
	if len(file) < 400:
		s = SnowNLP(u"。".join([ i["sentence"] for i in sentence]))
		key_sentence = s.summary(num_sentence)
	else:
		s = SnowNLP(file)
		key_sentence = s.summary(num_sentence)
	print "====================================="
	print (u'事件关键词:   ' +'/'.join(key_word) )
	print (u"时间关键词:   " + "/".join(key_time))
	print (u"地点关键词:   " +"/".join(key_position))
	print (u"关键短语:   " +"/".join(key_tag))
	if len(error.findall(file))>0:
		print (u'报错情况:   '+ error.findall(file)[0])
	print (u'摘要 :    '+ '\n'.join([i for i in key_sentence if not i in stopword ]))
	print "====================================="



	


def train_sample(file,tr4_stopword_path,window = 2,keywords_num = 20,num_sentence = 5):
	'''关键词查找及输出'''
	'''版本2'''
	tr4w = TextRank4Keyword(tr4_stopword_path)
	tr4s = TextRank4Sentence(tr4_stopword_path)
	tr4w.analyze(text=file, lower=True, window=window)  
	tr4s.analyze(text=text_file(file),  lower=True, source = 'all_filters')
	sentence = tr4s.get_key_sentences(num=4)
	ext_tag = jieba.analyse.extract_tags(file, topK=keywords_num,withWeight=False, allowPOS=('n','ns','nse','ne','v','ve','vde','l','a'))
	key_word = [i for i in ext_tag if i.isdigit() == False]
	text_rank1 = jieba.analyse.textrank(file, topK=40, withWeight=False, allowPOS=('tl','tt', 't','tle','ts','ns','nse','nt','nrt'))
	key_time = [i for i in text_rank1 if i.isdigit() == False]
	if len(key_time) == 0:
		text_rank1 = jieba.analyse.extract_tags(file, topK=2*keywords_num, withWeight=False, allowPOS=('t','ns','nse','tt','tl','tle'))
		key_time = [i for i in text_rank1 if i.isdigit() == False]
	text_rank2 = jieba.analyse.textrank(file, topK=40, withWeight=False, allowPOS=('a','n','case','m'))
	key_position = [i for i in text_rank2 if i.isdigit() == False][:8]
	if len(key_position) == 0:
		text_rank2 = jieba.analyse.extract_tags(file, topK=2*keywords_num, withWeight=False, allowPOS=('a','n','case'))
		key_position = [i for i in text_rank2 if i.isdigit() == False][:8]
	new_tag = jieba.analyse.tfidf(file, topK=keywords_num,withWeight=False, allowPOS=('v','n','case'))
	key_tag = [i for i in new_tag if i.isdigit() == False][:5]
	error = re.compile(r"\xe6\x8a\xa5\xe9\x94\x99+.{1,}[0-9]")
	if len(file) < 400:
		s = SnowNLP(u"。".join([ i["sentence"] for i in sentence]))
		key_sentence = s.summary(num_sentence)
	else:
		s = SnowNLP(file)
		key_sentence = s.summary(num_sentence)
	print "====================================="
	print (u'事件关键词:   ' +'/'.join(key_word) )
	print (u"时间、地点关键词:   " + "/".join(key_time))
	print (u"态度、状况关键词:   " +"/".join(key_position))
	print (u"处理关键短语:   " +"/".join(key_tag))
	if len(error.findall(file))>0:
		print (u'报错情况:   '+ error.findall(file)[0])
	print (u'摘要 :    '+ '\n'.join([i for i in key_sentence if not i in stopword ]))
	print "====================================="



#############部分测试脚本，暂无用处###########################################3
'''
words = pseg.cut(i)
for word, flag in words:
		print ('%s,%s' % (word,flag))


from optparse import OptionParser

python -m jieba /Users/zp/Desktop/百度地图/Data/CityData.csv  > /Users/zp/Desktop/百度地图/Data/cut_result.txt


from nltk.tokenize import sent_tokenize,word_tokenize
import nltk

day1 = re.compile(r".{1,3}\xe6\x9c\x88.+\xe6\x97\xa5") #七月二十日
day2 = re.compile(r".{1,3}\xe5\xa4\xa9") #昨天
noon = re.compile(r'.{1,3}\xe5\x8d\x88') #上午
hour = re.compile(r".{1,3}\xe7\x82\xb9") #三点
minites = re.compile(r".{1,3}\xe5\x88\x86") #分

def time(p):
	day1 = re.compile(r".{1,3}\xe6\x9c\x88.+\xe6\x97\xa5") #七月二十日
	day2 = re.compile(r".{1,3}\xe5\xa4\xa9") #昨天
	noon = re.compile(r'.{1,3}\xe5\x8d\x88') #上午
	hour = re.compile(r".{1,3}\xe7\x82\xb9") #三点
	minites = re.compile(r".{1,3}\xe5\x88\x86") #分
	time=[day1.findall(p),day2.findall(p),noon.findall(p),hour.findall(p),minites.findall(p)]
	if len(time[0]) > 0:
		day = time[0][0]
	elif len(time[1])>0:
		day = time[1][0]
	else:
		day = "当日"
	time2 =[[day],time[2],time[3],time[4]]
	out = [i[0] for i in time2 if len(i) >0]
	return out



from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
import sys
reload(sys)
sys.setdefaultencodeing('utf-8')


# Add the jar and model via their path (instead of setting environment variables):
jar = '/Users/zp/Downloads/stanford-postagger-full-2017-06-09/stanford-postagger.jar'
model = '/Users/zp/Downloads/stanford-postagger-full-2017-06-09/models/english-left3words-distsim.tagger'

pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')

text = pos_tagger.tag(word_tokenize(a))
print(text)
'''