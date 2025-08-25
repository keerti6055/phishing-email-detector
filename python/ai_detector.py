import joblib

# --- Step 1: Load the Saved AI Brain ---
# We load the vectorizer and the model that we created in our training script.
# This is like loading a saved game.
print("Loading the AI brain...")
vectorizer = joblib.load('vectorizer.pkl')
model = joblib.load('spam_model.pkl')
print("AI is ready! ✅")


# --- Step 2: Get Input from the User ---
user_input = input("\nPlease paste the email or message text here to scan:\n")


# --- Step 3: Use the AI to Make a Prediction ---
# 1. Convert the user's text into numbers using the SAME vectorizer.
vectorized_input = vectorizer.transform([user_input])

# 2. Give the numbers to the AI model to get its prediction.
prediction = model.predict(vectorized_input)


# --- Step 4: Show the Result ---
# The model will output either 'ham' (safe) or 'spam' (phishing).
result = prediction[0]

print("\n--- AI Analysis Complete ---")
if result == 'spam':
    print("🚨 Conclusion: This message is likely SPAM or PHISHING!")
else:
    print("✅ Conclusion: This message seems SAFE.")
print("----------------------------")
