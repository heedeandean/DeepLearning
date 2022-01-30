import pickle
from utils.Preprocess import Preprocess

f = open('../train_tools/dict/chatbot_dict.bin', 'rb')
word_index = pickle.load()