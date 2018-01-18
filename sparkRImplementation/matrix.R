rm(list=ls())
Sys.setenv(SPARK_HOME = "/usr/lib/spark")
Sys.setenv(HADOOP_HOME = "/usr/lib/spark")
.libPaths(c(file.path(Sys.getenv("SPARK_HOME"), "R", "lib"), .libPaths()))
library(SparkR)
sc <- sparkR.init()
sqlContext <- sparkRSQL.init(sc)

stringMatrixA <- SparkR:::map(SparkR:::textFile(sc,"s3n://another-test007/mat15000.txt"), function(string){
  strsplit(string, split = ",")
})

MatrixA <- SparkR:::map(stringMatrixA,function(x){
  SparkR:::lapply(x, function(y){
    strtoi(y)
  })
})


stringMatrixB <- SparkR:::map(SparkR:::textFile(sc,"s3n://another-test007/mat15000T.txt"), function(string){
  strsplit(string, split = ",")
})

MatrixB <- SparkR:::map(stringMatrixB,function(x){
  SparkR:::lapply(x, function(y){
    strtoi(y)
  })
})


c <- SparkR:::collect(SparkR:::lapply(MatrixA, function(x){SparkR:::lapply(MatrixB, function(y){
  sum(unlist(x)*unlist(y))
})}))

d <- SparkR:::lapply(c, function(x){
  SparkR:::collect(x)
})

SparkR:::saveAsTextFile(d,"s3n://another-test007/outputHDFS5000")







