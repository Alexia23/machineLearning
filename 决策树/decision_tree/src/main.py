#coding = utf-8
from src.train import *
train_percentage=[0.05,0.2,0.4,0.6,0.8,0.95]
if __name__ == "__main__":
    for i in range(len(train_percentage)):
        tree = train("data/adult.attr", "data/adult.data", "data/adult.test",train_percentage[i])

