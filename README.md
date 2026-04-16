# PhishShield AI — Real-Time Phishing Detection System

# Overview

PhishShield AI is an end-to-end machine learning system for real-time phishing website detection. It analyzes URLs during browsing, provides instant alerts, and includes a dashboard for monitoring and analytics.


# Key Highlights
Trained on 11,000+ phishing URLs
Achieves 96.4% accuracy and 95.9% F1-score
Processes requests in real-time via API (~milliseconds latency)
Logs and analyzes 100% of scanned URLs

# Features
Machine learning-based phishing detection (Random Forest)
Real-time browser monitoring using Chrome Extension
FastAPI backend for prediction API
Streamlit dashboard for analytics and manual scanning
URL logging with filtering and insights

# Tech Stack

Python, FastAPI, Scikit-learn, Pandas, Streamlit, JavaScript (Chrome Extension)

# Workflow
User visits a website
Chrome Extension captures the URL
Request sent to FastAPI backend
Model predicts phishing or safe
Result displayed instantly and logged

# Project Structure
backend/ – API and prediction logic
model/ – Training and saved model
extension/ – Chrome extension files
dashboard/ – Streamlit analytics dashboard
dataset/ – Raw and processed data

# Model Performance
Accuracy: 96.4%
Precision: 94.7%
Recall: 97.1%
F1 Score: 95.9%

# Conclusion
A scalable and automated phishing detection system that integrates machine learning, real-time API processing, and browser-level protection.
