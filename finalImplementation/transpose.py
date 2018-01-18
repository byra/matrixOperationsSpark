

def main():
    import time
    from pyspark import SparkContext
    sc = SparkContext()
    matrixB = sc.textFile("s3n://another-test007/file.txt")
    matIntB = matrixB.map(lambda line: line.split(",")).map(lambda i: [int(j)for j in i])
    rddT1 = matIntB.zipWithIndex().flatMap(lambda (x,i): [(i,j,e) for (j,e) in enumerate(x)])
    rddT2 = rddT1.map(lambda (i,j,e): (j, (i,e))).groupByKey().sortByKey()
    rddT3 = rddT2.map(lambda (i, x): sorted(list(x), cmp=lambda (i1,e1),(i2,e2) : cmp(i1, i2)))
    rddT4 = rddT3.map(lambda x: map(lambda (i, y): y , x))
    rddT5 = rddT4.map(lambda x: list(x))
    rddT5.saveAsTextFile("s3n://another-test007/transposeMatrix")

if __name__=='__main__':
    main()
