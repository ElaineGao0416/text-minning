from gensim.models.word2vec import Word2Vec
from gensim.models.word2vec import LineSentence  
import multiprocessing  
import numpy as np
import jieba
import jieba.analyse
import codecs
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import tensorflow as tf
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
import sys
reload(sys)
sys.setdefaultencoding('utf-8')




def get_sample(text_path):
	text2 = codecs.open(text_path, 'r', 'utf-8').readlines()
	label = []
	feature = []
	for line in text2:
		ln = line.strip().encode("utf8").replace('''"''',"").split(',')
		label1 = "".join(ln[1].split(" ")[:3])
		label.append(label1)
		feature1 = [ln[0]]+ln[1].split(" ")[3:5]
		feature.append(feature1)
	label_dict,label2 = set_label(label)
	fea_dict,feature2 = set_feature(feature)
	return label_dict,label2,fea_dict,feature2



def set_label(label):
	label_set = set(label)
	label_dict = {}
	for i,v in enumerate(label_set):
		label_dict[v] = i
	for i,v in enumerate(label):
		label[i] = label_dict[v]
	return label_dict,np.array(label)


def set_feature(feature):
	all_fea = []
	out = []
	for i in feature:
		for k in i:
			all_fea.append(k)
	fea_set = set(all_fea)
	fea_dict = {}
	for i,v in enumerate(fea_set):
		fea_dict[v] = i
	for i in feature:
		list_0 = np.random.randint(0,1,(1,len(fea_set)))[0].tolist()
		for k in i:
			position = fea_dict[k]
			list_0[position] = 1
		out.append(list_0)
	return fea_dict,np.array(out)



def reset_feature(feature,fea_dict):
	out = []
	for i in feature:
		list_0 = np.random.randint(0,1,(1,len(fea_dict)))[0].tolist()
		for k in i:
			try:
				position = fea_dict[k]
				list_0[position] = 1
			except:
				print str(k) + "is not in feature list! "
				continue
		out.append(list_0)
	return np.array(out)



def select_feature(feature,label):
	out_fea = []
	clf = linear_model.Lasso(alpha=0.0001,fit_intercept= False)
	clf.fit(feature,convert_label(label))
	list_0 = np.random.randint(0,1,(1,len(feature[0])))[0].tolist()
	for i in clf.coef_:
		list_0 += i 
	num = []
	for v,k in enumerate(list_0):
		if k != 0:
			num.append(v)
	for i in feature:
		new_line = []
		for k in num:
			new_line.append(i[k])
		out_fea.append(new_line)
	return np.array(out_fea),num



def reselect_feature(feature,fea_index):
	out_fea = []
	for i in feature:
		new_line = []
		for k in fea_index:
			new_line.append(i[k])
		out_fea.append(new_line)
	return np.array(out_fea)



# def set_feature(feature,size = 200):
# 	model = Word2Vec(feature, size=size, window=5, min_count=1, workers=4)
# 	feat = []
# 	for i in feature:
# 		fea = np.random.randint(0,1,(1,size)).astype('float64')
# 		for k in i:
# 			fea1 = model.wv[k]
# 			fea += fea1
# 		feat.append(fea.tolist()[0])
# 	return np.array(feat)


def convert_label(p):
	new_label = []
	length = len(label_dict)
	list_0 = np.random.randint(0,1,(1,length))
	for _ ,v in enumerate(p):
		new_lab = list_0[0].tolist()
		new_lab[v] = 1
		new_label.append(new_lab)
	return new_label



renewable_dict = '/Users/zp/Desktop/nlp/dict.txt'
address_dict = '/Users/zp/Desktop/nlp/address_dict.txt'
jieba_stop_word = '/Users/zp/Desktop/nlp/stopword.txt'
jieba.load_userdict(renewable_dict)
jieba.load_userdict(address_dict)
jieba.analyse.set_stop_words(jieba_stop_word)



text_path = '/Users/zp/Desktop/baidu2/Data/CityData4.csv'

label_dict, label,fea_dict,feature = get_sample(text_path)
selected_fea,fea_index = select_feature(feature,label)

sentences = u'庆春路3号'
text = list(jieba.cut(sentences)) 
text_feature = reselect_feature(reset_feature([text],fea_dict),fea_index)

X_train, X_test, y_train, y_test = train_test_split(selected_fea, convert_label(label), test_size=0.3, random_state=2)


# sklearn
# from sklearn.naive_bayes import GaussianNB
# from sklearn.metrics import accuracy_score
# from sklearn.cross_validation import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
# gnb = GaussianNB()
# clf = DecisionTreeClassifier(criterion='entropy',max_depth= 10,random_state=4)
# rfc = RandomForestClassifier(n_estimators=10, criterion='entropy')
# model = gnb.fit(X_train, y_train)
# model = rfc.fit(X_train, y_train)
# out1 = model.predict(X_train)
# out2 = model.predict(X_test)
# accuracy_score(y_train, out1)
# accuracy_score(y_test, out2)


## 神经网络
train_x = X_train.reshape(-1,2,1449,1)
test_x = X_test.reshape(-1,2,1449,1)
 
# 定义神经网络模型
with tf.Graph().as_default():   
    conv_net = input_data(shape=[None,2,1449,1], name='input')
    conv_net = conv_2d(conv_net, 200, 2, activation='relu',restore = True)
    conv_net = max_pool_2d(conv_net ,2)
    conv_net = dropout(conv_net, 0.3)
    conv_net = conv_2d(conv_net, 300, 2, activation='relu',restore = True)
    conv_net = max_pool_2d(conv_net ,2)
    conv_net = conv_2d(conv_net, 100, 2, activation='relu',restore = True)
    conv_net = max_pool_2d(conv_net ,2)
    conv_net = fully_connected(conv_net, 16, activation='relu',restore = True)
    conv_net = dropout(conv_net, 0.5)
    
    # Finetuning Softmax layer (Setting restore=False to not restore its weights)
    conv_net = fully_connected(conv_net, 25, activation='softmax')
    conv_net = regression(conv_net, optimizer='adam', loss='categorical_crossentropy', name='output')
     
    model = tflearn.DNN(conv_net)
    model.load('/Users/zp/Desktop/test_model2/model2')
    # 训练
    model.fit({'input':train_x}, {'output':y_train}, n_epoch=13, 
              validation_set=({'input':test_x}, {'output':y_test}), 
              snapshot_step=10, show_metric=True, run_id='mnist')


model.save('/Users/zp/Desktop/test_model2/model2')


'''
a = list(jieba.cut(sentences)) 
a = [a,a]

model = Word2Vec(LineSentence(text2), size=200, window=5, min_count=1, workers=4)
model = Word2Vec(a, size=200, window=5, min_count=1, workers=4)
#`sg` defines the training algorithm. By default (`sg=0`), CBOW is used.Otherwise (`sg=1`), skip-gram is employed.
#`size` is the dimensionality of the feature vectors.
#`window` is the maximum distance between the current and predicted word within a sentence.
#`alpha` is the initial learning rate (will linearly drop to `min_alpha` as training progresses).
#`seed` = for the random number generator. Initial vectors for each
#`min_count` = ignore all words with total frequency lower than this.
#`max_vocab_size` = limit RAM during vocabulary building; if there are more unique
#`sample` = threshold for configuring which higher-frequency words are randomly downsampled;default is 1e-3, useful range is (0, 1e-5).
#`workers` = use this many worker threads to train the model (=faster training with multicore machines)
#`hs` = if 1, hierarchical softmax will be used for model training.If set to 0 (default), and `negative` is non-zero, negative sampling will be used.
#`negative` = if > 0, negative sampling will be used, the int for negative
#how many "noise words" should be drawn (usually between 5-20).Default is 5. If set to 0, no negative samping is used.
#`cbow_mean` = if 0, use the sum of the context word vectors. If 1 (default), use the mean.
#`hashfxn` = hash function to use to randomly initialize weights, for increased
#`iter` = number of iterations (epochs) over the corpus. Default is 5.
#`sorted_vocab` = if 1 (default), sort the vocabulary by descending frequency beforeassigning word indexes.
print "/".join ([key for key in (model.wv.vocab)])
model.save(path)
model.wv['与环镇北路交叉口']
model.most_similar(['延安路'])

model.wv.n_similarity( ws1, ws2)
model.reset_weights()
model.wv.save_word2vec_format(fname, fvocab=None, binary=False)
load_word2vec_format(cls, fname, fvocab=None, binary=False, encoding='utf8', unicode_errors='strict', limit=None, datatype=<type 'numpy.float32'>) 
from __builtin__.type . Deprecated. Use gensim.models.KeyedVectors.load_word2vec_format instead.


model2 = Word2Vec.load(path)

zzz = model.train(sentences,total_words =30,epochs=4)
zzz = model.train(sentences,total_examples =1,epochs=4)

(model = gensim.models.Word2Vec.load('../Trained_Word2Vec_Model/savedmoel_200'))

Clients_vectors = np.array([model[word] for word in (model.wv.vocab)])

Clients_vectors_2d = tsne.fit_transform(Clients_vectors)
'''