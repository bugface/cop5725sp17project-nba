from sqlalchemy import create_engine
from time import sleep

def write():
	s = "this is line: "
	with open("test.txt", "w+") as f:
		for i in range(100000):
			f.writelines(s + str(i) + "\n")

def insert_into_database():
	SQLALCHEMY_DATABASE_URI = "oracle://alexgre:alex1988@cop5725sp17.clx2hx01phun.us-east-1.rds.amazonaws.com/ORCL"
	engine = create_engine(SQLALCHEMY_DATABASE_URI)
	data = None
	i = 0
	with engine.begin() as conn:
		with open("insert_for_Stats.txt", "r") as f:
			print("start...")
			for each in f:
				i += 1
				try:
					#remove \n and ; in each record
					data = each[:-2]
					conn.execute(data)
					if i % 1000 == 0:
						print("Finish {} records".format(i))
					if i % 20000 == 0:
						sleep(1)
				except:
					print(data)
			conn.execute("commit")
			print("done")

def read():
	with open("insert_for_Stats.txt", "r") as f:
		i = 0
		for each in f:
			print(each[:-2])
			i += 1
			if i > 10:
				break

def main():
	#read()
	#write()
	insert_into_database()

if __name__ == '__main__':
 	main()