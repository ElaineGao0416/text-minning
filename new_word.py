import jieba
import itertools
import re
from collections import Counter
from thulac import thulac
import numpy as np 
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



def PMI_Phrases(path = '/Users/zp/Desktop/nlp/SHARE_NLP/05',seg_only=False, filt=False,get_word_num = [2,3,4],\
	renewable_dict_path = '/Users/zp/Desktop/nlp/dict.txt' ,min_frequency = 2,min_pmi = 0):
	'''遍历文档
	并追加字典'''
	text =  codecs.open(path,'r','utf-8').read().encode('utf8').replace("]","】").replace("[","【")
	file_num = len(codecs.open(path,'r','utf-8').readlines())
	thu = thulac(user_dict=None, model_path=None, T2S=False, seg_only=seg_only, filt=filt)
	word = thu.cut(text)    
	words = []
	for i in word:
		words.append(i[0])
	set_word = []
	for v in words:
		try:
			if v not in set_word:
				set_word.append(v)
		except:
			continue
	#查找特殊字符病去除
	mark = re.compile(r'[|][@,，,),,(,~,.,_,|,！,）,@,～,（,|,:,/,-,-,+,=,！,-,。,、,*,⋯]{1,}[|]')
	part2 = mark.findall('|'.join(set_word))	
	for i in part2:
		try:
			set_word.remove(i[1:-1])
			text = text.replace(i[1:-1],'')
		except:
			continue	
	cnt_word = Counter(words)
	for i in get_word_num:
		get_words(set_word=set_word,word_num = i,min_frequency = min_frequency,min_pmi = min_pmi,renewable_dict_path=renewable_dict_path,file_num=file_num)
		



def get_words(set_word,file_num,word_num = 2, min_frequency = 5,min_pmi = 0,renewable_dict_path='/Users/zp/Desktop/dict2.txt'):
	'''计算pmi
	并且追加字典'''
	for i in range(len(set_word)-word_num + 1):
		xy = ''.join(set_word[i:i+word_num])
		try:
			yx_com = re.compile(xy)
		except:
			print xy+" can't be compiled!"
		p_yx = len(yx_com.findall(text))
		if p_yx > min_frequency :
			down = 1
			for k in range(word_num):
				down = down*cnt_word[set_word[i+k]]
			pmi_xy = np.log((p_yx*(file_num**(word_num-1))+0.0)/down)/np.log(2)
			if pmi_xy >= min_pmi:
				print "-"*25
				print xy, p_yx,pmi_xy
				#观察字典中是否有xy
				out = compile_find(p = xy,label='',renewable_dict_path=renewable_dict_path)
				#字典中有xy
				if len(out[0]) == 0 :
					decision = raw_input("would you set it as a word (y/n)?: ")
					decision = ask_for_decision(decision,question = "would you set it as a word (y/n)?: ")
					if decision == 'y' :
						newlabel = raw_input("its tag:   ")
						newp = xy.encode("utf8").replace("\xef\xbc\x8c","").replace(",","").replace("\xe3\x80\x82","").replace("\xef\xbc\x9f","").replace("\xef\xbc\x81","").replace(".","")
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
				#字典中没有xy
				elif len(out[0]) != 0 :
					print 'It is not a new word!'
					label = raw_input("Provide your tag:   ")
					out3 = compile_find(p =xy,label=label,renewable_dict_path=renewable_dict_path)
					if len(out3[0]) != 0 and len(out3[1]) == 0 :
						replace_input(xy,label,finding = out[0],renewable_dict_path=renewable_dict_path)
					else:
						print "Word exist!"
				else:
					print "this is not a new word!"
	print "-"*25
					



def ask_for_decision(decision,question = "would you correct it (y/n)?: "):
	'''输入文字鉴定
	返回正确输入的decision'''
	while decision != "y" and decision != "n" :
		print "i can't understand your input!"
		print "pleace do it again!"
		decision = raw_input(question)
	return decision



def replace_input(p,label,finding,renewable_dict_path):
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


def compile_find(p,label,renewable_dict_path = '/Users/gaozhiping/Desktop/dict2.txt'):
	'''查找新词是否在字典中存在
	返回两个结果，1.查找到的p；2.查到到的p+label'''
	file = open(renewable_dict_path, 'r')
	dict_renew = file.readlines()
	file.close()
	p = p.encode("utf8").replace("\xef\xbc\x8c","").replace("\xe3\x80\x82","").replace("\xef\xbc\x9f","")
	target = re.compile(p+r'\s[a-z]+')
	consequence1 = target.findall(",".join([i.strip() for i in dict_renew]))
	combine = re.compile(p+r'\s'+label)
	consequence2 = combine.findall(",".join([i.strip() for i in dict_renew]))
	return (consequence1,consequence2)



renewable_dict = '/Users/zp/Desktop/nlp/SHARE_NLP/dict.txt'
sampe_path = '/Users/zp/Desktop/nlp/SHARE_NLP/05'
PMI_Phrases(path = sampe_path,seg_only=False, filt=False,get_word_num = [2,3,4],\
	renewable_dict_path = renewable_dict ,min_frequency = 1,min_pmi = 0)

