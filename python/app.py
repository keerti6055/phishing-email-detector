from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

print("🚀 Loading AI model and vectorizer...")
vectorizer = joblib.load('vectorizer.pkl')
model = joblib.load('spam_model.pkl')
print("✅ AI components loaded successfully.")

suspicious_words = [
    "urgent", "action required", "immediate", "important", "alert", "warning",
    "account", "verify", "suspended", "locked", "disabled", "password", "username", "login",
    "payment", "invoice", "bank", "credit card", "refund", "unusual activity",
    "confirm your details", "click the link below", "security notice", "prize", "won", "claim"
]

@app.route('/scan', methods=['POST'])
def scan_email():
    data = request.get_json()
    if not data or 'email_text' not in data:
        return jsonify({'error': 'No email text provided'}), 400
        
    email_text = data['email_text']
    
    vectorized_input = vectorizer.transform([email_text])
    prediction = model.predict(vectorized_input)
    ai_result = prediction[0]

    # --- FINAL, SMARTER LOGIC ---
    # 1. If the AI says it's spam, we trust it completely.
    if ai_result == 'spam':
        final_conclusion = "SPAM"
    # 2. If the AI says it's safe, we check for keywords to be cautious, but we NEVER call it spam.
    else:
        danger_score = 0
        for word in suspicious_words:
            if word in email_text.lower():
                danger_score += 1
        
        # This is the key change. We no longer have a rule that leads to "SPAM".
        if danger_score > 0:
            final_conclusion = "CAUTION" # If any keywords are found, just be cautious.
        else:
            final_conclusion = "SAFE"    # If no keywords are found, it's safe.

    print(f"🔎 Scanned email. AI said '{ai_result}', Final Conclusion: '{final_conclusion}'")
    
    return jsonify({'result': final_conclusion})

if __name__ == '__main__':
    app.run(port=5000, debug=True)

