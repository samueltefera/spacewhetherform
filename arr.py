a = [1,2,3]
b = [4,5,6]
c = []
for list1 in range(len(a)):
    d = a[list1] - b[list1]
    c.append(d)

print(c)