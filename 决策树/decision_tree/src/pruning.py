#coding = utf-8
from src.define_class import *
from src.build_tree import *

#课件上所讲的贪婪剪枝算法，将数据分为训练集和验证集，
#剪枝每一个点之后，计算它对验证集的测试准确率的影响，如果变高就剪掉
def post_pruning(examples, attributes, node):
	if len(examples)==0:
		return node
	if node.is_leaf():
		return node
	all_leaf = True
	for child in node.children:
		if not child[1].is_leaf():
			all_leaf = False
    #如果这个点所有的孩子都是叶子节点，
    # 则把这个点变成一个叶子节点观察是否会对验证集的准确率造成影响
	if all_leaf:
		new_node = Classification_Node(node_classify(attributes[-1], examples))
		if cal_accuracy(examples, new_node) > cal_accuracy(examples, node):
			node = new_node
	else:
        #如果该点存在孩子不是叶子节点，那将验证点进行分离进行递归剪枝
		for child in node.children:
			example_set = get_data(node.attribute.index,
			child[0], examples, attributes[node.attribute.index].numeric)
			value = child[0]
			pruned_node =  post_pruning(example_set, attributes, child[1])
			node.children.remove(child)
			node.children.append((value, pruned_node))
	return node
