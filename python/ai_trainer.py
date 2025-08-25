import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib

# --- Step 1: Load and Prepare the Data ---
# We use pandas to load our CSV file. We give names to the columns for clarity.
# 'latin-1' is an encoding type that helps read special characters in the dataset.
print("Loading dataset...")
data = pd.read_csv('spam.csv', encoding='latin-1', sep='\t', header=None, names=['label', 'text'])
print("Dataset loaded successfully.")


# --- Step 2: Convert Text into Numbers ---
# An AI can't read words, so we convert the text into numerical data.
# TfidfVectorizer is a smart way to turn sentences into a list of numbers
# where each number represents the importance of a word.
print("Vectorizing text data...")
vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
X = vectorizer.fit_transform(data['text'])
y = data['label']
print("Text vectorized.")


# --- Step 3: Split Data for Training and Testing ---
# We can't test the AI on the same data it studied.
# So, we split our dataset: 80% for training (studying) and 20% for testing (the exam).
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data split complete.")


# --- Step 4: Train the AI Model ---
# We "show" the training data to our AI model (Multinomial Naive Bayes)
# so it can learn the patterns of spam vs. ham.
print("Training the AI model...")
model = MultinomialNB()
model.fit(X_train, y_train)
print("Model training complete.")


# --- Step 5: Test the AI Model's Accuracy ---
# We use the testing data (the "exam") that the model has never seen before
# to see how accurately it can predict if a message is spam or ham.
print("Testing the model...")
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print("---" * 10)
print(f"🎉 Model Accuracy: {accuracy * 100:.2f}%")
print("---" * 10)


# --- Step 6: Save the Trained Model and Vectorizer ---
# We save our "trained brain" (the model) and the vectorizer to files.
# This allows us to use them later in our detector without re-training every time.
print("Saving the model and vectorizer...")
joblib.dump(model, 'spam_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
print("Model and vectorizer saved. Your AI is ready to be used! ✅")