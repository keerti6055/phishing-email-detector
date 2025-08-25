# The suspicious email we want to check
email_text = input("Please paste the email text here to scan: \n")
# A list of suspicious words we are looking for
suspicious_words = [
    # Words creating urgency
    "urgent", "action required", "immediate", "important", "alert", "warning",

    # Words about accounts and verification
    "account", "verify", "suspended", "locked", "disabled", "password", "username", "login",

    # Financial words
    "payment", "invoice", "bank", "credit card", "refund", "unusual activity",

    # Common trick phrases
    "confirm your details", "click the link below", "security notice"
]
# Let's start the danger score at 0
danger_score = 0

print("--- Starting Phishing Scan ---")

# This code will look at each suspicious word one-by-one
# and check if it's inside our email text.
for word in suspicious_words:
    if word in email_text.lower(): # .lower() makes the check not case-sensitive
        print(f"Alert! Found a suspicious word: '{word}'")
        danger_score = danger_score + 1

print("--- Scan Complete ---")
print(f"Final Danger Score: {danger_score}")

if danger_score >= 3:
    print("Conclusion: 🚨 This email is highly suspicious! 🚨")
elif danger_score > 0:
    print("Conclusion: 🤔 This email seems a bit suspicious. Be careful.")
else:
    print("Conclusion: ✅ This email seems safe.")
