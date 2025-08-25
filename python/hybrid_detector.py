import joblib
import sys # We need this library to read multi-line input

# --- Part 1: Load the AI Brain ---
vectorizer = joblib.load('vectorizer.pkl')
model = joblib.load('spam_model.pkl')

# --- Part 2: The Rule-Based Engine ---
suspicious_words = [
    "urgent", "action required", "immediate", "important", "alert", "warning",
    "account", "verify", "suspended", "locked", "disabled", "password", "username", "login",
    "payment", "invoice", "bank", "credit card", "refund", "unusual activity",
    "confirm your details", "click the link below", "security notice", "prize", "won", "claim"
]

# --- Part 3: The Hybrid Logic ---
print("🚀 Starting Hybrid Phishing Detector...")
print("Paste your email below. When you are finished, type 'SCAN' on a new line and press Enter.")
print("------------------------------------------------------------------------------------")

# This is our new, smarter input loop
lines = []
while True:
    line = sys.stdin.readline()
    if "SCAN" in line.upper(): # Check if the line contains 'SCAN'
        break
    lines.append(line)

# Join all the pasted lines into a single block of text
user_input = "".join(lines)

if not user_input.strip():
    print("\nNo input received. Exiting.")
else:
    # Step A: First, get the AI's opinion
    vectorized_input = vectorizer.transform([user_input])
    prediction = model.predict(vectorized_input)
    ai_result = prediction[0]

    # Step B: Apply the hybrid logic
    print("\n--- Analysis Complete ---")
    if ai_result == 'spam':
        print("🚨 AI Conclusion: This message is likely SPAM or PHISHING!")
    else:
        print("🤔 AI Conclusion: This message seems safe, but checking with rule-based system for extra security...")
        
        danger_score = 0
        found_words = []
        
        for word in suspicious_words:
            if word in user_input.lower():
                danger_score += 1
                found_words.append(word)
                
        if danger_score > 0:
            print(f"🚦 Rule-Based System Found {danger_score} Red Flag(s): {', '.join(found_words)}")
            print("🚨 Final Conclusion: This message is SUSPICIOUS despite the AI's initial assessment.")
        else:
            print("✅ Final Conclusion: Both AI and Rule-Based systems agree. This message seems SAFE.")

    print("----------------------------")
