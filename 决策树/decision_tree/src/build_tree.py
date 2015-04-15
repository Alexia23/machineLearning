#coding = utf-8
import copy,random,math,time

from src.define_class import *

#递归建树，每次选择信息增益最大的属性划分，为多叉树-----改进ID3算法后的C4.5算法
#选择当前信息增益最大的属性对决策树进行分裂，并根据该属性可能的取值建立对应的分支。
def build_tree(traindata,parents_data, attr,threshold):
    if len(traindata)==0:
        return Classification_Node(node_classify(attr[-1],parents_data))
    elif same_classify(traindata):
        return Classification_Node(traindata[0].attributes[-1])
    elif len(traindata) < threshold:
        return Classification_Node(node_classify(attr[-1],traindata))
    elif len(attr) == 0:
        return Classification_Node(node_classify(attr[-1], traindata))
    else:
        #timep = time.time()
        attribute = most_important_attr(attr,traindata)
        #timep1 = time.time()
        #print(str(timep1-timep))
        tree=Node(attribute)
        index = attribute.index
        numeric = attribute.numeric
        attribute_copy = copy.deepcopy(attr)
        attribute_copy.remove(attribute)
        for v in attribute.vals:
            traindata_spilt = get_data(index, v[0], traindata,numeric)
            child = build_tree(traindata_spilt,traindata,attribute_copy,threshold)
            tree.add_child(v[0],child)
        return tree

#计算熵值
def boolean_entropy(percentage):
	if percentage==0 or percentage==1:
		return 0
	else:
		return -(percentage * math.log(percentage,2) + (1-percentage) * math.log((1-percentage),2))

#计算信息增益
def cal_info_gain(attr, traindata):
	gain = 1
	total = len(traindata)
	for v in attr.vals:
		split_value = get_data(attr.index,v[0],traindata,attr.numeric,attr.frequency)
		label_in_split_value = get_data(len(traindata[0].attributes)-1,traindata[0].attributes[-1],
										split_value)
		split_num = len(split_value)
		pro = split_num*1.0/total
		if pro>0:
			gain-=pro*boolean_entropy(len(label_in_split_value)/split_num)
	return gain

#找到信息增益最大的属性
def most_important_attr(attrs,traindata):
    max = -1
    max_attr=attrs[0]
    for i in range(0, len(attrs)-1):
        gain = cal_info_gain(attrs[i],traindata)
        if gain > max:
            max = gain
            max_attr = attrs[i]
    return max_attr

#判断训练数据是不是都是相同的label值，比如说该题就都是>50K,或者<=50K
def same_classify(traindata):
    one_classify=traindata[0].attributes[-1]
    flag = 1
    for i in traindata:
        if i.attributes[-1]!=one_classify:
            flag = 0
            break
    return flag

#根据属性的某个值将训练集中是这个值的数据提取出来，如果是？，则如果是？，默认是最初训练集该属性概率最大的值
#建树所需，一层一层划分
def get_data(index, value, example_list, is_numeric = False, most_frequent = None):
	examples = []
	if is_numeric:
		start = int(value[0:value.index(':')])
		end = int(value[value.index(':') + 1:])
		for example in example_list:
			if example.attributes[index] == '?':
				if value == most_frequent:
					examples.append(example)				
			elif int(example.attributes[index]) in range(start, end):
				examples.append(example)
	else:
		for example in example_list:		
			if example.attributes[index] == value:
				examples.append(example)
			elif example.attributes[index] == '?':
				if value == most_frequent:
					examples.append(example)			
	return examples

#找到traindata中attr属性中频率最大的值
def node_classify(attr,traindata):
	count={}
	max = 0
	max_set= []
	for val in attr.vals:
		count[val[0]] = 0
	for i in traindata:
		count[i.attributes[attr.index]] += 1
	for pair in count.items():
		if pair[1] > max:
			max = pair[1]
			max_set =[]
			max_set.append(pair[0])
		elif pair[1]==max:
			max_set.append(pair[0])
	return max_set[random.randint(0,len(max_set)-1)]

#example沿着tree向下搜索，直到找到叶子节点
def example_classify(example, tree):
	return Tree.search(example, tree)

#计算测试数据的准确率
def cal_accuracy(examples, tree):
	total = 0
	right = 0
	for example in examples:
		result = example_classify(example, tree)
		if result == example.attributes[-1]:
			right  = right +1
		total = total +1
	if total==0:
		return 0
	return right/total
