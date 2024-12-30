# Kafka Sentiment Analysis Pipeline

This project demonstrates a complete data pipeline for sentiment analysis using Kafka for real-time message streaming, a Naive Bayes model for text classification, and Apache Spark for real-time processing.

---

## Overview

The pipeline is divided into three components:

1. **Producer** (`producer.py`): Reads data from a CSV file and sends it to a Kafka topic.
2. **Model Training** (`modelFit.py`): Trains a Naive Bayes classifier on text data and saves the model.
3. **Consumer** (`consumer.py`): Reads messages from Kafka, applies the pre-trained model for predictions, and displays the results in real time.

---

## Requirements

Make sure you have the following installed:

- Python 3.8+
- Apache Kafka
- Apache Spark
- Required Python libraries (install via `pip`):
  ```bash
  pip install confluent-kafka pandas scikit-learn joblib pyspark

---

## Usage

### 1. **Prepare Kafka**

Start the Kafka broker and create a topic named `comments`:

`kafka-topics.sh --create --topic comments --bootstrap-server localhost:9092`

### 2. **Producer**

The producer reads reviews from `imdb.csv` and sends them to the Kafka topic.

#### Run:

`python producer.py`

### 3. **Model Training**

Train a sentiment analysis model and save it for later use.

#### Run:

`python modelFit.py`

### 4. **Consumer**

The consumer reads messages from Kafka, applies the trained model, and predicts the sentiment for each message.

#### Run:

`python consumer.py`
