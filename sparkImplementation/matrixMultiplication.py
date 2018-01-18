from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.mllib.linalg.distributed import *

def as_block_matrix(rdd, rowsPerBlock=1024, colsPerBlock=1024):
        return IndexedRowMatrix(rdd.zipWithIndex().map(lambda xi: IndexedRow(xi[1], xi[0]))).toBlockMatrix(rowsPerBlock, colsPerBlock)

def rddTranspose(rdd):
        rddT1 = rdd.zipWithIndex().flatMap(lambda (x,i): [(i,j,e) for (j,e) in enumerate(x)])
        rddT2 = rddT1.map(lambda (i,j,e): (j, (i,e))).groupByKey().sortByKey()
        rddT3 = rddT2.map(lambda (i, x): sorted(list(x), cmp=lambda (i1,e1),(i2,e2) : cmp(i1, i2)))
        rddT4 = rddT3.map(lambda x: map(lambda (i, y): y , x))
        return rddT4.map(lambda x: list(x))

sc = SparkContext()
sqlContext = SQLContext(sc)
matrixA = sc.textFile("s3n://matrices-bucket/mat25000.txt").map(lambda line: line.split(",")).map(lambda i: [int(j)for j in i])
matrixB = sc.textFile("s3n://matrices-bucket/mat25000.txt").map(lambda line: line.split(",")).map(lambda i: [int(j)for j in i])
transposeB = rddTranspose(matrixB)
multipliedMatrix = as_block_matrix(matrixA).multiply(as_block_matrix(transposeB))
matrixC = sc.parallelize(multipliedMatrix.toLocalMatrix().toArray()).saveAsTextFile("s3n://matrices-bucket/matc25000")
