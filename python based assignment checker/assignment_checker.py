import os
import re
import tkinter as tk
from tkinter import messagebox, ttk
import threading

try:
    from google import genai
    from google.genai import types
    HAS_GEMINI = True
    client = genai.Client(api_key="enter your api key")
except ImportError:
    HAS_GEMINI = False

def call_gemini(prompt, callback):
    if not HAS_GEMINI:
        callback("Error: google-genai library is not installed.\nPlease run: pip install google-genai")
        return
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                top_p=1.0,
                top_k=1,
                max_output_tokens=2048,
            )
        )
        callback(response.text)
    except Exception as e:
        callback(f"Gemini API Error: {str(e)}")

class AssignmentCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Assignment Checker System (AI-Powered)")
        self.root.geometry("700x700")

        self.frames = {}
        for F in (MainMenu, Module1Grammar, Module2Plagiarism, Module3ShortAnswer, Module4Math, Module5Programming):
            page_name = F.__name__
            frame = F(parent=self.root, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="🎓 AI-Powered Assignment Checker", font=("Helvetica", 18, "bold"))
        label.pack(pady=30)
        
        buttons = [
            ("1. Grammar & Spelling Check", "Module1Grammar"),
            ("2. Plagiarism/AI-Generation Check", "Module2Plagiarism"),
            ("3. Dynamic Short Answer Auto-Grading", "Module3ShortAnswer"),
            ("4. Dynamic Math Answer Checker", "Module4Math"),
            ("5. Dynamic Programming Auto-Grader", "Module5Programming"),
            ("6. Exit System", None)
        ]
        
        for text, page in buttons:
            if page:
                btn = tk.Button(self, text=text, width=45, height=2, font=("Helvetica", 11),
                                command=lambda p=page: controller.show_frame(p))
            else:
                btn = tk.Button(self, text=text, width=45, height=2, font=("Helvetica", 11),
                                command=controller.root.quit, fg="red")
            btn.pack(pady=8)

class Module1Grammar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="✍ MODULE 1: AI Grammar & Spelling Check", font=("Helvetica", 16, "bold")).pack(pady=15)
        
        tk.Label(self, text="Enter text to check:", font=("Helvetica", 11)).pack(pady=(5, 5))
        self.text_input = tk.Text(self, height=8, width=70, font=("Helvetica", 10))
        self.text_input.pack(pady=5)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        self.check_btn = tk.Button(btn_frame, text="✅ Check Grammar (AI)", bg="#4CAF50", fg="white", font=("Helvetica", 11, "bold"),
                                   command=self.check_grammar)
        self.check_btn.pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="🔙 Back to Menu", font=("Helvetica", 11),
                  command=lambda: controller.show_frame("MainMenu")).pack(side=tk.LEFT, padx=10)
        
        self.result_text = tk.Text(self, height=14, width=70, font=("Helvetica", 10), state=tk.DISABLED, bg="#f4f4f4")
        self.result_text.pack(pady=10)

    def check_grammar(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text.")
            return

        self.display_result("Evaluating grammar with Gemini AI. Please wait...")
        self.check_btn.config(state=tk.DISABLED)
        
        prompt = f"""You are an expert English teacher. Analyze the following text for grammar, spelling, and punctuation errors. 
Provide:
1. Total mistakes found.
2. An overall corrected version of the text.
3. A bulleted list of the specific corrections made and why.
Text to analyze:
\"\"\"{text}\"\"\""""
        
        threading.Thread(target=call_gemini, args=(prompt, self.on_result), daemon=True).start()

    def on_result(self, result):
        self.display_result(result)
        self.check_btn.config(state=tk.NORMAL)

    def display_result(self, result):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)

class Module2Plagiarism(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="🕵️ MODULE 2: AI Plagiarism & Generation Check", font=("Helvetica", 16, "bold")).pack(pady=15)
        tk.Label(self, text="Paste your assignment text below:", font=("Helvetica", 11)).pack(pady=5)
        
        self.text_input = tk.Text(self, height=8, width=70, font=("Helvetica", 10))
        self.text_input.pack(pady=5)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        self.check_btn = tk.Button(btn_frame, text="🔍 Check Originality (AI)", bg="#2196F3", fg="white", font=("Helvetica", 11, "bold"),
                                   command=self.check_plagiarism)
        self.check_btn.pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="🔙 Back to Menu", font=("Helvetica", 11),
                  command=lambda: controller.show_frame("MainMenu")).pack(side=tk.LEFT, padx=10)
        
        self.result_text = tk.Text(self, height=14, width=70, font=("Helvetica", 10), state=tk.DISABLED, bg="#f4f4f4")
        self.result_text.pack(pady=10)

    def check_plagiarism(self):
        student_text = self.text_input.get("1.0", tk.END).strip()
        if not student_text:
            messagebox.showwarning("Input Error", "Please enter some text.")
            return

        self.display_result("Analyzing text originality with Gemini AI. Please wait...")
        self.check_btn.config(state=tk.DISABLED)
        
        prompt = f"""As an AI detection and plagiarism expert, evaluate the following text.
Tell me:
1. Is it likely written by an AI (like ChatGPT/Gemini), or human-written?
2. Does it look like it was plagiarized or copied from common general internet sources?
3. Provide a brief justification for your assessment.
Text to analyze:
\"\"\"{student_text}\"\"\""""
        
        threading.Thread(target=call_gemini, args=(prompt, self.on_result), daemon=True).start()

    def on_result(self, result):
        self.display_result(result)
        self.check_btn.config(state=tk.NORMAL)

    def display_result(self, result):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)

class Module3ShortAnswer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="📝 MODULE 3: Dynamic Short Answer Auto-Grading", font=("Helvetica", 16, "bold")).pack(pady=15)
        
        tk.Label(self, text="Topic or Question:", font=("Helvetica", 11, "bold")).pack()
        self.topic_input = tk.Entry(self, width=65, font=("Helvetica", 11))
        self.topic_input.pack(pady=5)
        self.topic_input.insert(0, "Explain the process of photosynthesis.")
            
        tk.Label(self, text="Student's Answer:", font=("Helvetica", 11, "bold")).pack(pady=5)
        self.text_input = tk.Text(self, height=6, width=70, font=("Helvetica", 10))
        self.text_input.pack(pady=5)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        self.check_btn = tk.Button(btn_frame, text="💯 Grade Answer (AI)", bg="#FF9800", fg="white", font=("Helvetica", 11, "bold"),
                                   command=self.check_answer)
        self.check_btn.pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="🔙 Back to Menu", font=("Helvetica", 11),
                  command=lambda: controller.show_frame("MainMenu")).pack(side=tk.LEFT, padx=10)
        
        self.result_text = tk.Text(self, height=12, width=70, font=("Helvetica", 10), state=tk.DISABLED, bg="#f4f4f4")
        self.result_text.pack(pady=10)

    def check_answer(self):
        topic = self.topic_input.get().strip()
        student_ans = self.text_input.get("1.0", tk.END).strip()
        
        if not topic or not student_ans:
            messagebox.showwarning("Input Error", "Please enter both a question and an answer.")
            return

        self.display_result("Grading answer with Gemini AI. Please wait...")
        self.check_btn.config(state=tk.DISABLED)
        
        prompt = f"""You are a strict but fair professor. Evaluate the student's answer based on the given question/topic.
Question: {topic}
Student Answer: {student_ans}

Please provide:
1. A Score out of 100%.
2. A brief evaluation of what they got right and what they missed.
3. What the ideal answer should have included."""

        threading.Thread(target=call_gemini, args=(prompt, self.on_result), daemon=True).start()

    def on_result(self, result):
        self.display_result(result)
        self.check_btn.config(state=tk.NORMAL)
        
    def display_result(self, result):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)

class Module4Math(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="➗ MODULE 4: Dynamic Math Answer Checker", font=("Helvetica", 16, "bold")).pack(pady=15)
        
        tk.Label(self, text="Math Problem:", font=("Helvetica", 11, "bold")).pack()
        self.prob_input = tk.Entry(self, width=65, font=("Helvetica", 11))
        self.prob_input.pack(pady=5)
        self.prob_input.insert(0, "Expand (x+1)^2")
            
        tk.Label(self, text="Student's Answer:", font=("Helvetica", 11, "bold")).pack(pady=5)
        self.entry_input = tk.Entry(self, width=65, font=("Helvetica", 11))
        self.entry_input.pack(pady=5)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        self.check_btn = tk.Button(btn_frame, text="🧮 Check Math (AI)", bg="#9C27B0", fg="white", font=("Helvetica", 11, "bold"),
                                   command=self.check_math)
        self.check_btn.pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="🔙 Back to Menu", font=("Helvetica", 11),
                  command=lambda: controller.show_frame("MainMenu")).pack(side=tk.LEFT, padx=10)
        
        self.result_text = tk.Text(self, height=12, width=70, font=("Helvetica", 10), state=tk.DISABLED, bg="#f4f4f4")
        self.result_text.pack(pady=10)

    def check_math(self):
        prob_name = self.prob_input.get().strip()
        student_expr = self.entry_input.get().strip()
        
        if not prob_name or not student_expr:
            messagebox.showwarning("Input Error", "Please enter both a problem and an answer.")
            return

        self.display_result("Evaluating mathematical equivalence with Gemini AI. Please wait...")
        self.check_btn.config(state=tk.DISABLED)
        
        prompt = f"""You are a mathematics professor. Evaluate if the student's answer correctly solves the problem. 
Math Problem: {prob_name}
Student's Answer: {student_expr}

Is this mathematically correct and equivalent to the proper solution? 
Respond with:
1. Verdict: CORRECT or INCORRECT
2. Explanation of the step-by-step correct solution."""

        threading.Thread(target=call_gemini, args=(prompt, self.on_result), daemon=True).start()

    def on_result(self, result):
        self.display_result(result)
        self.check_btn.config(state=tk.NORMAL)

    def display_result(self, result):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)

class Module5Programming(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="💻 MODULE 5: Dynamic Programming Auto-Grader", font=("Helvetica", 16, "bold")).pack(pady=15)
        
        tk.Label(self, text="Programming Prompt / Requirements:", font=("Helvetica", 11, "bold")).pack()
        self.prob_input = tk.Entry(self, width=65, font=("Helvetica", 11))
        self.prob_input.pack(pady=5)
        self.prob_input.insert(0, "Write a Python function to check if a number is prime.")
            
        tk.Label(self, text="Student's Code:", font=("Helvetica", 11, "bold")).pack(pady=5)
        self.text_input = tk.Text(self, height=8, width=70, font=("Helvetica", 10))
        self.text_input.pack(pady=5)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        self.check_btn = tk.Button(btn_frame, text="▶ Check Code (AI)", bg="#E91E63", fg="white", font=("Helvetica", 11, "bold"),
                                   command=self.check_program)
        self.check_btn.pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="🔙 Back to Menu", font=("Helvetica", 11),
                  command=lambda: controller.show_frame("MainMenu")).pack(side=tk.LEFT, padx=10)
        
        self.result_text = tk.Text(self, height=12, width=70, font=("Helvetica", 10), state=tk.DISABLED, bg="#f4f4f4")
        self.result_text.pack(pady=10)

    def check_program(self):
        prompt_req = self.prob_input.get().strip()
        student_code = self.text_input.get("1.0", tk.END).strip()
        
        if not prompt_req or not student_code:
            messagebox.showwarning("Input Error", "Please enter both a prompt and the code.")
            return

        self.display_result("Reviewing code logic and correctness with Gemini AI. Please wait...")
        self.check_btn.config(state=tk.DISABLED)
        
        prompt = f"""You are a senior computer science professor reviewing a student's code.
Assignment Requirements: {prompt_req}

Student's Code:
```
{student_code}
```

Please evaluate this code. Provide:
1. Does the code fulfill the requirements? (Pass/Fail)
2. Mention any bugs, syntax errors, or logic flaws.
3. Suggest an approach to improve or optimize it (if applicable)."""

        threading.Thread(target=call_gemini, args=(prompt, self.on_result), daemon=True).start()

    def on_result(self, result):
        self.display_result(result)
        self.check_btn.config(state=tk.NORMAL)

    def display_result(self, result):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = AssignmentCheckerApp(root)
    root.mainloop()
