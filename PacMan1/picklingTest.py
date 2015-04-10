from numpy import array
import csv
from joblib import load

matrix = open("PicklingTesting.p")
# print matrix

Q_new = load("PicklingTesting.p")
print Q_new
print type(Q_new)
print Q_new.size



# Q_new = []
# with open("PicklingTesting.p", 'rb') as csvfile:
# 	matrixreader = csv.reader(csvfile, delimiter = ' ')
# 	for row in matrixreader:
# 		Q_new.append(row)

# print Q_new


# line_filtered = []
# for line in matrix:
# 	# print line
# 	line_strip = list(line.strip(".[] \n"))
# 	for number in line_strip:
# 		if number == '0':
# 			line_filtered.append(number)
# 		else:
# 			pass
# 	# line3 = line2.remove(" ")
# 	M = list(line_filtered)

# print type(M)
# print M
# Q = array(M)#.reshape(8,8)
# Q = Q.reshape(8,8)
# print Q
# print type(Q)
# print Q.size



	# item = numpy.array(line).reshape(1,2)
	# print type(item)
	# print item.shape
	# M.append(line)

# Q = list(M[1:])
# print Q
# Q[0] = Q[0][1:]
# Q[-1] = Q[-1][:-1]
# print Q


# print type(Q)
# print Q[1]


# Q = numpy.array(Q).reshape(8,8)


# print Q
# print type(Q)

# print Q.shape