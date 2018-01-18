from pyspark import SparkContext
sc = SparkContext()
file1 = sc.textFile("s3n://matrices-bucket/mat500.txt")
file2 = sc.textFile("s3n://matrices-bucket/mat500.txt")
rowA = 500
colA = 500
rowB = 500
colB = 500
strA = file1.map(lambda x: x.split(','))
strB = file2.map(lambda x: x.split(','))

matA = strA.map(lambda i: [int(j)for j in i])
matB = strB.map(lambda i: [int(j)for j in i])

keysA = matA.zipWithIndex().flatMap(lambda (x,i): [((i,k),("A",j,e)) for (j,e) in enumerate(x) for k in range(0, colB)])
keysB = matB.zipWithIndex().flatMap(lambda (x,i): [((k,j),("B",i,e)) for (j,e) in enumerate(x) for k in range(0, rowA)])

keysU = keysA.union(keysB)
keysG = keysU.groupByKey().sortByKey()

values = keysG.map(lambda i: [x[2] for x in list(i[1])])
matC = values.map(lambda x: sum([x[i]*x[i+rowB] for i in range(0, colA) ]))
matC.saveAsTextFile("s3n://matrices-bucket/matC500")
exit()
