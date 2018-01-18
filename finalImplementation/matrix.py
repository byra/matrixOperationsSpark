def main():
    from pyspark import SparkContext
    import numpy as np
    sc = SparkContext()
    file1 = sc.textFile("s3n://matrices-bucket/mat500Tanspose.txt")
    file2 = sc.textFile("s3n://matrices-bucket/mat500.txt")
    strA = file1.map(lambda x: x.split(','))
    strB = file2.map(lambda x: x.split(','))
    matA = strA.map(lambda i: [int(j)for j in i])
    matB = strB.map(lambda i: [int(j)for j in i])
    zipMats = matA.zip(matB)
    interRDD = zipMats.map(lambda x: np.outer(x[0],x[1]))
    interRDD.reduce(lambda a,b: np.array(a)+np.array(b))
    output = open("s3://matrices-bucket/myfile.txt", "w")
    np.savetxt(output, delimiter=',', newline='\n')
    exit()


if __name__=='__main__':
    main()
