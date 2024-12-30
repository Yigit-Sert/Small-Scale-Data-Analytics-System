import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
import joblib

# Read the CSV file
df = pd.read_csv("imdb.csv")

# Inspect the data
print(df.head())

# Separate the text and labels
X = df['review']  # Text data
y = df['sentiment']  # Labels (positive, negative)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Data preparation is complete!
# We create a pipeline: first convert the text data into numerical features, then train the Naive Bayes classifier
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)

# Evaluate the results
print(classification_report(y_test, y_pred))

# Save the trained model to a file
joblib.dump(model, 'imdb_model.pkl')
