from __future__ import print_function

import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(-1)

    bootstrapServers = sys.argv[1]
    subscribeType = sys.argv[2]
    topics = sys.argv[3]

    spark = SparkSession\
        .builder\
        .appName("tweeterSentiment")\
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    lines = spark\
        .readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", bootstrapServers)\
        .option(subscribeType, topics)\
        .load()\
        .selectExpr("CAST(value AS STRING)")

    words = lines.select(
        explode(
            split(lines.value, ' ')
        ).alias('word')
    )

    query = words\
            .selectExpr("to_json(struct(*)) AS value")\
            .writeStream\
            .format("kafka")\
            .option("kafka.bootstrap.servers", "localhost:9092")\
            .option("topic", "tweet_sentiments_result")\
            .option("checkpointLocation", "file:/Users/kunal/Documents/Courses/BD\ 6350/Assignments/tweets")\
            .start()\
            .awaitTermination()
