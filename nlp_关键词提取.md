#NLP关键词、摘要提取脚本
作者：Zhiping Gao  
备注：1.脚本输出形式为print，如需修改为其他形式，需要稍作修改；2.自定义字典还未完全，需要不断补充和修改；3.这里的遍历方法比较不成熟，需要人工的程度较高，如果先要简便一点，请参考PMI_Phrase.

##1.导入包

```
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
```
**简单介绍这些包：**  

* jieba的分词灵活性较高，分词的准确性也较高，可以自主添加字典和stop word；  
* textrank4zh在提取关键语句上具有一定优势。另外SnowNLP也具有提取关键语句的功能。SnowNLP提取的对象为短语，而textrank4zh提取的是句子。此处将两个方法结合，当语句较短时，采用SnowNLP为主的摘要提取，因为SnowNLP提取的对象为短语，而textrank4zh提取的是句子；  
* codecs在此处作为打开utf8文件的工具使用。

##2.define function
###命名规则
```
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
```
**设置短语规则：**  
每个tuple中，最后一个为短语的赋值。  
例如('m','m','m') 表示由m+m组成的短语仍为m。  
部分命名解释如下：

`m ：money`  
`tt ：自定义time`   
`t ： 时间点`   
`tl：时间段`  
`a：形容性质`  
`v：动词性质`   
`case：业务`  
`eng：英文字母`   
`nr：代词，代指人`    
... 

其他参考jieba的词性标注。

###函数脚本
```
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
	new_tag = jieba.analyse.tfidf(file, topK=keywords_num,withWeight=False, allowPOS=('tt','ns','n','v','t','a','tl','tle','case'))
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



def train_sample_new(file,tr4_stopword_path,window = 2,keywords_num = 20,num_sentence = 5):
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

```

##3.脚本应用
###step1
####输入样本
```
text1 = u"四月十五号，我家的路由器开始发生故障，早上的时候还好，\
就是网速慢一点，下午开始一断一断的，到半个小时以前已经完全连不上了，请过来修理一下。我家住在下沙高教园区学正街20号。"
text2 = codecs.open('/Users/zp/Desktop/nlp/05', 'r', 'utf-8').readlines()
```
两种输入形式，可以是文本，或者list。

###step2
```
#定义字典
renewable_dict = '/Users/zp/Desktop/nlp/dict.txt'   #自定义的可更新的字典
address_dict = '/Users/zp/Desktop/address_dict/'    #爬虫获得的浙江省的地理位置字典
jieba_stop_word = '/Users/zp/Desktop/nlp/stopword.txt'     #jieba自定义的stop word字典
textrank4zh_stop_word = '/Users/zp/Desktop/nlp/stopword.data'         #textrank4zh自定义的stop word字典


#导入辞典
jieba.load_userdict(renewable_dict)
load_address_dict(address_dict)
jieba.analyse.set_stop_words(jieba_stop_word)
stopword = codecs.open(jieba_stop_word, 'r', 'utf-8').read()
stopword_path = textrank4zh_stop_word
```

###step3
```
#遍历样本，追加字典内容
for i in range(740,760):
	phrases(text2[i],renewable_dict_path = renewable_dict )

#导入辞典
jieba.load_userdict(renewable_dict)
```
此步骤主要为更新自定义字典而设计，需要手动、人为地进行判断、加入。
###step4
```
#提取关键词和摘要
train_sample(file=text1,tr4_stopword_path=textrank4zh_stop_word,window = 2,keywords_num = 20,num_sentence = 5)
train_sample(file=b,tr4_stopword_path=textrank4zh_stop_word)
train_sample(file=j,tr4_stopword_path=textrank4zh_stop_word)
for i in range(630,650):
	train_sample_new(file=text2[i],tr4_stopword_path=textrank4zh_stop_word)

```

**评价：**

感觉版本1的效果并不好，且时间、地点关键词在样本中较少，因此推出版本2.  
版本2的指向性更高一点。  

`版本1: train_sample`
`版本2: train_sample_new`

##4.样例
```
事件关键词:   流量/来营业厅反映/客户表示/用在/要求查明/账务/停机/联系电话/无线/号码/手机/具体/产生/地方/发现
时间、地点关键词:   
态度、状况关键词:   流量/账务/号码/地方/具体/产生/无线/停机
处理关键短语:   流量/来营业厅反映/客户表示/用在/要求查明
摘要 :    客户表示自己在4号
客户来营业厅反映自己5号
发现流量用超了
流量怎么产生的
客户现要求查明具体
```
```
事件关键词:   商户/退钱/代金券/支付订单/没有收到/二线客服/杭州创谷信息技术有限公司/支付成功/用户来电反映/一鸣真鲜/补充说明/重发/回电/转给/兑换/核实/实体/支付/相关
时间、地点关键词:   一鸣真鲜/杭州创谷信息技术有限公司
态度、状况关键词:   商户/二线客服/代金券/一个/实体/没有收到/核实/32.00
处理关键短语:   商户/退钱/代金券/支付订单/二线客服
摘要 :    用户来电反映称说兑换了
用户称商户没有收到
请核实回电
一个一鸣真鲜的
代金券
```

```
事件关键词:   支付/小票/南大东路/一鸣真鲜奶/客户要求/补款/客户反映/回复本机/扣款/绑定/商户/后台/核实/现金/失败/处理/成功/交易/使用
时间、地点关键词:   南大东路/一鸣真鲜奶
态度、状况关键词:   补款/交易/核实/后台/成功/现金/商户/35.00
处理关键短语:   支付/小票/回复本机/客户要求/补款
摘要 :    银行卡支付35元
2017-08-05客户在姜山南大东路一鸣真鲜奶使用
客户反映
现客户要求
支付失败
```

##5.辅助功能介绍
```
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
```