# 🎓 AI-Powered Student Assignment Checker

Welcome to the **AI-Powered Student Assignment Checker**! This is a simple, highly dynamic desktop application built with Python. It uses the intelligence of the **Google Gemini API** to automatically check and grade student assignments across five different categories. 

This project evolved from static keyword matching to a fully intelligent, AI-driven assistant that actually reads, understands, and evaluates student answers mathematically, logically, and grammatically.

---

## ✨ Features and Modules

The application is divided into 5 smart modules:

### 1. ✍️ Grammar & Spelling Check
Instead of just finding basic typos, this module acts like an **expert English teacher**. You can paste any text, and the AI will:
- Give a total count of mistakes.
- Provide a newly corrected version of the text.
- Explain *why* specific grammar or punctuation corrections were made so the student can learn from it.

### 2. 🕵️ Plagiarism & AI-Generation Check
Worried about students using ChatGPT or copying their homework? Paste their assignment here. The AI will:
- Check if the text sounds like it was written by an AI or a human.
- Check if it feels copied from general internet sources.
- Give a detailed explanation of its assessment.

### 3. 📝 Dynamic Short Answer Auto-Grading
You can type **any question** (e.g., "Explain the theory of relativity") and paste the student's answer. The AI will dynamically:
- Score the answer out of 100%.
- Tell you exactly what they got right and what they missed.
- Provide the ideal framework for what a perfect answer should have looked like.

### 4. ➗ Dynamic Math Answer Checker
Tired of static math checkers that don't understand different ways to write formulas? You can enter any math problem (e.g., "Expand $(x+1)^2$") and the student's answer. The AI will:
- Verify mathematical equivalence (it knows that $x^2 + 2x + 1$ is the same as $1 + 2x + x^2$).
- Walk you through the **step-by-step correct solution**.

### 5. 💻 Dynamic Programming Auto-Grader
Type in a coding prompt (like "Write a Python function to check for prime numbers") and paste the student's code. Instead of doing dummy text-matching, the AI acts as a **Senior Computer Science Professor** and will:
- Tell you if the code actually fulfills the requirements (Pass/Fail).
- Point out syntax errors, logic flaws, or bugs.
- Suggest ways to optimize the code!

---

## 🛠️ How to Install and Run

### Step 1: Open Terminal and Navigate to the Project
First, open your terminal (Command Prompt or PowerShell on Windows) and tell it to go to the desktop folder where the app is located. Just copy and paste this command and hit Enter:

```bash
cd "C:\Users\nawaz\OneDrive\Desktop\ankit"
```

### Step 2: Install the AI Library
Next, you need to install the official Google Gemini AI library so the app can communicate with the AI. Copy and paste this command and hit Enter:

```bash
pip install google-genai
```

### Step 3: Run the App!
Finally, start the application! Copy and paste this command and hit Enter:

```bash
python assignment_checker.py
```

*A window will pop up automatically. Click on any module and start grading!*

---

## 🔑 A Note on API Keys
This app connects to **Google's Gemini 2.5 Flash** model via an API key configured inside `assignment_checker.py`. 
- The API key is securely baked into the code and handled through the `genai.Client()` setup.
- The app sends student answers to Gemini, gets the grading/evaluations back, and instantly displays them beautifully on the user interface using Python's `tkinter` library.

Enjoy accurate, dynamic, and lightning-fast assignment grading! 🚀
