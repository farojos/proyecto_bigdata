from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.flume import FlumeUtils
from gensim.models import KeyedVectors
from gensim.test.utils import datapath, get_tmpfile
from pyspark.mllib.classification import SVMWithSGD, SVMModel
from pyspark.mllib.regression import LabeledPoint
import uuid
sc = SparkContext(appName="PythonStreamingFlumeWordCount")
def sendRecord(tup):
    if(not tup.isEmpty()):
	rdd_arr=  tup.collect()
	el = rdd_arr[0][1].split('\n')
	tmp_file = get_tmpfile("/home/cloudera/Desktop/test_word2vec.txt")
	model = KeyedVectors.load_word2vec_format(tmp_file)
	vectores = []
	normal_v = []
	for i in el:
		value = i[:1]
		text = i[2:]
		text_arr = text.split(' ')
		vector = [0]*50
		total = 1
		for j in text_arr:
			try: 
				vector+=model.get_vector(j)
				total+=1
			except:
				pass
		vector = vector/total
		label = LabeledPoint(int(value), vector)
		vectores.append(label)
		normal_v.append([int(value), vector])
	vectores.append(LabeledPoint(0.0, [0]*50))
        model = SVMWithSGD.train(sc.parallelize(vectores), iterations=100)
	#model.save(sc, "/home/cloudera/pythonSVMWithSGDModel")
	pred = []
	match_0=0
	nmatch_0=0
	match_1=0
	nmatch_1=0
        final = []
	for i in normal_v:
		pre = model.predict(i[1])
		if(i[0]==0):
			if(pre==i[0]):
				match_0+=1
			else:
				nmatch_0+=1
		else:
			if(pre==i[0]):
				match_1+=1
			else:
				nmatch_1+=1
		final.append([pre,i[0],i[1]])
	print('\n\n\n\n\n\n\n\n\n\n\n')
	print('\n\n\n\n\n\n\n\n\n\n\n')
	print([[match_0,nmatch_0],[nmatch_1,match_1]])	
	print('\n\n\n\n\n\n\n\n\n\n\n')
	print('\n\n\n\n\n\n\n\n\n\n\n')
	print(len(final))
	print('\n\n\n\n\n\n\n\n\n\n\n')
	print('\n\n\n\n\n\n\n\n\n\n\n')
	f = open('/home/cloudera/vectores'+str(uuid.uuid4())+'.txt','w')
	for i in final:
		for j in i:
			f.write('%s' % j)
		f.write('\n')
	f.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: flume_wordcount.py <hostname> <port>", file=sys.stderr)
        sys.exit(-1)
    uid = 1
    
    ssc = StreamingContext(sc, 30)

    hostname, port = sys.argv[1:]
    kvs = FlumeUtils.createStream(ssc, hostname, int(port))
    lines = kvs.map(lambda x: x[1])
    counts = lines.map(lambda word: (uid, word)) \
                  .reduceByKey(lambda a, b: a+'\n'+b) \
		  .foreachRDD(sendRecord)

    ssc.start()
    ssc.awaitTermination()

