#coding = utf-8
import time,copy

from src.build_tree import *
from src.pruning import *
from src.parse_data import *

threshold_ratio = 0.01
#percentage*data是训练集，剩余的是验证集（用来剪枝）
def train(attr_file, train_file, test_file,percentage):
	time1=time.time();
	print("-----------------percentage:"+ str(percentage)+"-------------------")
	attribute_info = get_attr(attr_file)
	examples = get_examples(train_file)
	test_examples = get_examples(test_file)
	traindata=random.sample(examples,int(len(examples)*percentage))
	for vld in traindata:
		examples.remove(vld)
	attributes = build_attr(attribute_info, traindata, 1)
	parent_ex = copy.deepcopy(traindata)
	time2 = time.time()
	#print ("build_attributes:" + str(time2-time1))

	tree = build_tree(traindata, parent_ex, attributes, len(examples)*threshold_ratio)
	time3 = time.time()
	#print ("build_tree:" + str(time3-time2))
	print("noPruning Tree Size=" + str(tree.size()))

	print("noPruning Accuracy=" + str(cal_accuracy(test_examples, tree)))
	time4 = time.time()
	#print ("no Pruning test:" + str(time4-time3))

	tree = post_pruning(examples, attributes, tree)
	time5 = time.time()
	#print ("Pruning time:" + str(time5-time4))
	print("Pruning Tree Size=" + str(tree.size()))

	print("Pruning Accuracy=" + str(cal_accuracy(test_examples, tree)))
	time6 = time.time()
	#print ("Pruning test:" + str(time6-time5))
	return tree





