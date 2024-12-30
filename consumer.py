
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
from pyspark.sql.functions import udf
import logging
import joblib
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

# Create a Spark session for structured streaming with Kafka
spark = SparkSession.builder \
    .appName("KafkaStructuredStreaming").getOrCreate()

# Set the log level to "ERROR" to reduce unnecessary log output
spark.sparkContext.setLogLevel("ERROR")


# Kafka connection details
kafka_server = "localhost:9092"
topic_name = "comments"

# Load the pre-trained model (e.g., sentiment analysis or classification model)
model = joblib.load('imdb_model.pkl')

# Reading data from Kafka stream
df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", kafka_server).option("subscribe", topic_name).load()

# Processing Kafka messages (key and value of the message)
# Here, we're only interested in the value (the tweet) from the Kafka message
parsed_df = df.selectExpr("CAST(value AS STRING) AS tweet")

# Function to predict the category based on the message content (e.g., sentiment)
def predict_category(message):
    try:
        prediction = model.predict([message])[0]
        return str(prediction)
    except Exception as e:
        return str(e)

# Register the UDF (User Defined Function) with Spark
predict_udf = udf(predict_category, StringType())

# Process the incoming data: compute tweet length and word count
# Here, we are not using it currently, but you can compute additional features like tweet length or word count if needed
# transformed_df = parsed_df.selectExpr("tweet", "length(tweet) AS tweet_length", "size(split(tweet, ' ')) AS word_count")

# Apply the UDF to predict the category for each tweet
transformed_df = parsed_df.withColumn("predicted_category", predict_udf(F.col("tweet")))

#def process_batch(batch_df, batch_id):
 #    batch_df.show(truncate=False)

# Using foreachBatch to process each batch of data from the Kafka stream
# This writes the results to the console, displaying them as they arrive
query = transformed_df.writeStream.outputMode("append").format("console").start()

# Wait for the stream processing to finish (it will run indefinitely unless terminated)
query.awaitTermination()
