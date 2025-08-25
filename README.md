🛡️ Hybrid AI Phishing Detector
A real-time, intelligent browser extension that uses a hybrid AI and rule-based system to detect and flag phishing emails directly within the Gmail interface. This project combines a Python-powered backend with a user-centric Chrome extension to provide a seamless layer of security against phishing attacks.

✨ Live Demo
(demo.gif)

🚀 Key Features
Hybrid Detection Engine: Combines a Machine Learning model (Multinomial Naive Bayes) with a keyword-based scanner for a balanced and accurate analysis.

Real-Time Alerts: Injects color-coded security banners (SAFE, CAUTION, DANGER) directly into the Gmail UI as you open emails.

Personalized Trust List: A user-centric "Always Trust This Sender" feature allows each user to build their own dynamic whitelist, reducing false positives over time.

Client-Server Architecture: Built with a robust Python Flask backend for AI processing and a lightweight vanilla JavaScript frontend for browser integration.

High Accuracy: The AI model was trained on the widely-used spam.csv dataset, achieving over 98% accuracy during testing.

🛠️ Tech Stack
Backend: Python, Flask, Flask-CORS

Machine Learning: Scikit-learn, Pandas, Joblib

Frontend: Vanilla JavaScript (Chrome Extension API)

Version Control: Git & GitHub

⚙️ System Architecture
The project operates on a client-server model:

The Client (Chrome Extension): A content script (content.js) runs on the Gmail page. It detects when an email is opened, checks the sender against a personal trust list stored in the browser, and if the sender is unknown, it sends the email's content to the backend for analysis.

The Server (Python API): A Flask application (app.py) exposes a /scan endpoint. It receives the email text, processes it using the pre-trained AI model and hybrid logic, and returns a final verdict (SAFE, CAUTION, or SPAM).

🔧 Setup and Installation
To run this project locally, follow these steps:

1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/phishing-email-tracker.git
cd phishing-email-tracker

2. Set Up the Python Backend

# Navigate to the python directory
cd python

# It's recommended to use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the required libraries
pip install -r requirements.txt

# Run the Flask server
python app.py

Your server should now be running at http://127.0.0.1:5000. Leave this terminal open.

3. Set Up the Chrome Extension

Open Google Chrome and navigate to chrome://extensions.

Enable Developer mode in the top-right corner.

Click the "Load unpacked" button.

Select the extension folder from the project directory.

The extension should now be active!

4. How to Use

Make sure the Python server is running.

Open Gmail in your browser.

Click on any email. A security banner will appear at the top, indicating the safety level.

For emails marked as CAUTION or DANGER, you can choose to trust the sender, which will add them to your personal whitelist for the future.
