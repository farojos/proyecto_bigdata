from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
glove_file = datapath('/home/cloudera/Desktop/glove.6B.50d.txt')
tmp_file = get_tmpfile("/home/cloudera/Desktop/test_word2vec.txt")
from gensim.scripts.glove2word2vec import glove2word2vec
glove2word2vec(glove_file, tmp_file)
