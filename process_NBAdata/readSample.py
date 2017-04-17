import csv

def getOneRecord():
	with open("nba.json","r") as f:
		sample  = f.readline()
	with open("sampledata.json","w") as f1:
		f1.writelines(sample)

def test(i):
	with open("test.txt","r") as f:
		for index, line in enumerate(f):
			if(index == i):
				sample  = f.readline()
				print(sample)

def write2csv():
	with open("test.csv", "a") as f:
		#filednames = ["a" , "b"]
		writer = csv.writer(f)
		# writer.writerow(["Iamtitle1", "iamtitle2", "iamtitle3"])
		# for i in range(5):
		# 	writer.writerow([i+1, chr(ord('a') + i), '08/%02d/07' % (i+1)])
		return writer

def rea4csv():
	with open("test.csv", "r") as f:
		reader = csv.reader(f)
		for row in reader:
			print(row)

def readJson1():
	wr = write2csv()
	title_list = ["t_name", "t_abbv", "t_score", "t_home", "t_won", 
					"t_ast",]
	wr.writerow()

def testBar():
	from progress.bar import Bar
	import time
	bar = Bar("processing...", max = 200)
	i = 0
	while i < 200:
		time.sleep(0.01)
		bar.next()
		i += 1

if __name__ == "__main__":
	#getOneRecord()
	# for i in range(4):
	# 	test(i)
	#write2csv()
	#rea4csv()
	#readJson1()
	testBar()