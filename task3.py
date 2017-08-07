 #coding:utf-8
from pylab import *
import Paper
import csv
from ILearner import Svr
import numpy as np
import ast

# 文件路径
paperPath = "F:\\比赛数据\\task3\\papers.txt"
trainPath = "F:\\比赛数据\\task3\\train.csv"
validationPath="F:\\比赛数据\\task3\\validation.csv"
output3Path="F:\\比赛数据\\task3\\output3.txt"

tempPath="F:\\比赛数据\\task3\\temp3.txt"

def Test():
	while True:
		aut = raw_input("author Name:")
		if aut=="-1":
			break
		res,total = GroupReferedPaperByYear(aut)
		for k,v in res.items():
			print "%d %d"%(k,len(v))
		print total

def GroupReferedPaperByYear(author):
	res={}
	total=0
	papers = Paper.Paper.getPaperByAut(author)
	for paper in papers:
		for refed in paper.Referenced:
			total=total+1
			if res.has_key(refed.Time):
				res[refed.Time].append(refed)
			else:
				res[refed.Time] = [refed]
	return res,total

def ParsePaperTxt():
	with open(name=unicode(paperPath,'utf8'),mode="rU") as f:
		for eachLine in f:
			if eachLine.startswith('#index'):
				i = int(eachLine[6:])
				p=Paper.Paper.getPaperById(i)
			elif eachLine.startswith("#@"):
				p.Author = eachLine[2:-1].split(',')
				for aut in p.Author:
					Paper.Paper.addAutPaper(aut,p)
			elif eachLine.startswith("#*"):
				p.Title = eachLine[2:-1]
			elif eachLine.startswith("#t"):
				p.Time = int(eachLine[2:-1])
			elif eachLine.startswith("#c"):
				p.Journal = eachLine[2:-1]
			elif eachLine.startswith("#%"):
				t = Paper.Paper.getPaperById(int(eachLine[2:-1]))
				p.References.append(t)
				t.Referenced.append(p)
			else:
				pass

def Work():
	# todo : 计算误差，选择模型，保存模型
	with open(name=unicode(validationPath,'utf8'),mode="r") as csvf:
		with open(name=unicode(output3Path,'utf8'),mode="w") as out:
			reader=csv.reader(csvf)
			firstRow=True
			for row in reader:
				if firstRow:
					firstRow=False
					out.write("<task3>\nauthorname\tcitation\n")
					continue
				res,total = GroupReferedPaperByYear(row[0])
				keys=res.keys()
				keys.sort()
				X=keys
				ty=[len(res[k]) for k in X]
				y=[sum(ty[0:i+1]) for i in range(len(X))]
				A=0
				if len(y)>0:
					svr = Svr(kernel='linear')
					svr.train(np.array(X).reshape(len(X),1), np.array(y).reshape(len(y),))
					Xp = [[2017]]
					yp = svr.predict(Xp)
					A=int(yp[0])*6
				out.write("%s\t%d\n"%(row[0], A))
			out.write("</task3>\n")

def SaveTrainResult():
	with open(name=unicode(trainPath,'utf8'),mode="r") as trainf:
		reader=csv.reader(trainf)
		first=True
		with open(name=unicode(tempPath,'utf8'),mode="w") as outf:
			for row in reader:
				if first:
					first=False
					continue
				res,total=GroupReferedPaperByYear(row[0])
				keys=res.keys()
				keys.sort()
				X=keys
				ty=[len(res[k]) for k in X]
				y=[sum(ty[0:i+1]) for i in range(len(X))]
				A=0
				if len(y)>0:
					svr = Svr(kernel='linear')
					svr.train(np.array(X).reshape(len(X),1), np.array(y).reshape(len(y),))
					Xp = [[2017]]
					yp = svr.predict(Xp)
					A = int(yp[0])
				outf.write("%r\t%r\t%r\t%r\t%r\t\n"%(row[0],X,y,row[1],A))

def Analsis():
	with open(name=unicode(tempPath,'utf8'),mode="r") as outf:
		for row in outf:
			dom = row.split('\t')
			X = ast.literal_eval(dom[1])
			y = ast.literal_eval(dom[2])
			yp = ast.literal_eval(dom[2])
			X.append(2017)
			y.append(int(ast.literal_eval(dom[3])))
			yp.append(ast.literal_eval(dom[4]))
			if int(ast.literal_eval(dom[3]))==0 or ast.literal_eval(dom[4])==0:
				continue
			plt.title(dom[0])
			plt.plot(X,y,'bo',label='real')
			plt.plot(X,yp,'r+',label='predict')
			plt.legend()
			plt.show()


def main():
	#ParsePaperTxt()
	#Test()
	#Work()
	#SaveTrainResult()
	Analsis()

if __name__ == "__main__":
	main()


"""
rng=np.random.RandomState(0)
X=rng.rand(1000,1)*2*3.14159
Xp = rng.rand(100,1)*6*3.14159-2*3.14159
y=np.sin(X).ravel()
svr = Svr('rbf',10,0.1)
svr.train(X,y)
yp=svr.predict(Xp)
plt.figure()
plt.scatter(X,y,c='r',label='SVR',zorder=2)
plt.scatter(Xp,yp,c='b',label='Predict',zorder=1)
plt.xlabel('data')
plt.ylabel('target')
plt.title('SVR versus Kernel Ridge')
plt.legend()
plt.show()
"""