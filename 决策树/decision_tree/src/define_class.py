#coding = utf-8
class Tree(object):
	def is_leaf(self):
		pass
	def size(self):
		pass
	def search(example, tree):
		node = tree
		val = None
		while node!=None and not node.is_leaf():
			search_val = example.attributes[node.attribute.index]
			if search_val != "?":
				node = node.search(search_val)
			else:
				node = node.search(Tree.search_unknown(example, node))
		if node==None:
			return None
		return node.classification

	def search_unknown(example, subroot):
		return subroot.attribute.most_frequent()

class Node(Tree):
	def __init__(self, attribute, children = None):
		self.attribute = attribute
		if not children:
			self.children = []
		else:
			self.children = children
	def size(self):
		node_num = 1
		for child in self.children:
			node_num += child[1].size()
		return node_num
	def add_child(self, value, node):
		self.children.append((value, node))
	def search(self, val):
		for child in self.children:
			if child[0] == val:
				return child[1]
			elif child[0].find(':') != -1:
				rg = child[0]
				start = int(rg[0:rg.index(':')])
				end = int(rg[rg.index(':') + 1:])
				if int(val) in range(start, end):
					return child[1]
		return None
	def is_leaf(self):
		return 0
#叶子节点
class Classification_Node(Tree):
	def __init__(self, classification):
		self.classification = classification
	def is_leaf(self):
		return 1
	def size(self):
		return 1

#封装属性的类
class Attribute(object):
	def __init__(self, name, vals, index, numeric):
		self.name = name
		self.vals = vals
		self.index = index
		self.numeric = numeric
		self.frequent = None  #属性值中频率最大的
	def frequency(self, value):
		for val in self.vals:
			if val[0] == value:
				return val[1]
		return -1
    #获取属性值中频率最大的
	def most_frequent(self):
		if self.frequent:
			return self.frequent
		max_frequency = -1
		max_val = None
		for val in self.vals:
			if (val[1] > max_frequency):
				max_frequency = val[1]
				max_val = val[0]
		self.frequent = max_val
		return self.frequent
	def __eq__(self, other):
		return self.name == other.name
#封装数据的类
class Example(object):
	def __init__(self, name, attribute_vector):
		self.name = name
		self.attributes = attribute_vector
