#coding = utf-8
import sys

from src.define_class import *


#读取训练和测试文件的每一个样例，封装到到class里面
def get_examples(example_file_path):
	file = open(example_file_path)
	lines = file.readlines()
	file.close()
	examples = []
	index = 1
	for line in lines:
		vals = line[:line.index('.')].split(',')
		ex_vals = []
		name = "Example " + str(index)
		for val in vals:
			ex_vals.append(val.strip())
		examples.append(Example(name, ex_vals))
		index += 1
	return examples

#读取属性文件
def get_attr(attribute_file_path):
	file = open(attribute_file_path)
	lines = file.readlines()
	file.close()
	attribute_info = []
	index = 0
	for line in lines:
		name = line[0:line.index(':')]
		vals = line[line.index(':')+2:line.index('.')].split(',')
		attr_vals=[]
		for i in range(0,len(vals)):
			attr_vals.append(vals[i].strip())
		attribute_info.append((name,attr_vals,index))
		index += 1
	return attribute_info

#计算在训练集中某属性最大频率的值，如果是？就默认是该属性最大频率的值
def build_attr(attribute_info, examples, classified = 0):
	attributes = []
	if classified:
		attribute_indexes = range(0, len(attribute_info))
	else:
		attribute_indexes = range(0, len(attribute_info) - 1)
	for index in attribute_indexes:
		attr = attribute_info[index]
		attribute_values = calc_frequencies(attr[1], attr[2], examples)
		attributes.append(Attribute(attr[0], attribute_values, attr[2], attr[1][0] == "continuous"))
	return attributes

#计算属性各个值的频率，如果是“continuous”，则需要找出最大值和最小值，划分成n段
def calc_frequencies(values, index, examples):
    count={}
    pairs=[]
    split_num = 50
    sum_valid=0
    if values[0]=="continuous":
        numbers=[]
        for testdata in examples:
            if testdata.attributes[index]!='?':
                numbers.append(int(testdata.attributes[index]))
        numbers.sort()
        maxv = numbers[-1]
        minv = numbers[0]
        split_one =int((maxv-minv)/split_num)+1
        for num in numbers:
            sum_valid=sum_valid+1
            for i in range(split_num):
                start = minv+i*split_one
                end = start+split_one
                if num >=start  and num <end:
                    if count.get(str(start)+':'+str(end)) == None:
                        count[str(start)+':'+str(end)] =1
                    else:
                        count[str(start)+':'+str(end)]+=1
    else:
        for testdata in examples:
            if testdata.attributes[index]!='?':
                sum_valid = sum_valid+1
                if count.get(testdata.attributes[index])==None:
                    count[testdata.attributes[index]]=1
                else:
                    count[testdata.attributes[index]] += 1
    for pair in count.items():
        pairs.append((pair[0],pair[1]*1.0/sum_valid))
    return pairs

