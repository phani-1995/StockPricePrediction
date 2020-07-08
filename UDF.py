from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, StringType
from pyspark.sql.functions import udf, col

sc = SparkContext.getOrCreate()
sql=SparkSession(sc)
print(sc)

data=sql.read.csv('HistoricalQuotes.csv',header=True)
data.show(5)

def clear_string(value : str) -> str:
    value = value.replace('$', '')
    return float(value)
clear_string_udf = udf(lambda value: clear_string(value), DoubleType())

data= data.withColumn("Date", data["Date"].cast("string")
                                        ).withColumn(" Close/Last", clear_string_udf(col(" Close/Last"))
                                        ).withColumn(" Volume", clear_string_udf(col(" Volume"))
                                        ).withColumn(" Open", clear_string_udf(col(" Open"))
                                        ).withColumn(" High", clear_string_udf(col(" High"))
                                        ).withColumn(" Low", clear_string_udf(col(" Low")))

data.printSchema()