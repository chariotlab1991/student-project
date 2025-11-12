from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, countDistinct, avg, expr

spark = SparkSession.builder.appName("edtech").getOrCreate()

df = spark.read.csv("data/events.csv", header=True, inferSchema=True)

agg = (df.groupBy("student_id","course_id")
       .agg(sum("seconds_spent").alias("secs_total"),
            countDistinct("ts").alias("active_days"),
            avg("score_delta").alias("avg_quiz_delta"),
            expr("sum(case when event_type='quiz_submit' then 1 else 0 end)").alias("quiz_count")))

agg.toPandas().to_csv("data/agg_events.csv", index=False)
spark.stop()
