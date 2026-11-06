AI Interview Coach

An LLM-powered mock interview web app that conducts a realistic interview, one question at a time, and then gives you structured feedback on how you did. Built with Streamlit and the Google Gemini API as a final-year B.Tech project.

 Features
Conversational interviewer: asks one question at a time, reacts briefly to your answer, then moves on to the next question.
Role-based interviews: Software Developer, Data Analyst, Data Scientist, AI/ML Engineer, HR / Behavioural.
Adjustable difficulty: Easy, Medium or Hard.
Custom length: choose 3 to 10 questions per interview.
Optional question bank: upload a CSV and the interviewer will pick or adapt questions from it.
Structured feedback report at the end of the interview, with:
Overall score out of 10
Strengths
Areas to improve
Question-by-question comments
Communication and confidence tips
Suggested topics to practice next
🛠️ Tech Stack
Component	Technology
Language	Python 3.9+
Web UI	Streamlit
LLM	Google Gemini (gemini-2.5-flash by default)
LLM SDK	google-genai
Data handling	pandas
Project Structure
ai-interview-coach/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── questions.csv       # (Optional) sample question bank
└── README.md
Getting Started
1. Clone the repository
bash
git clone https://github.com/<your-username>/ai-interview-coach.git
cd ai-interview-coach
2. (Recommended) Create a virtual environment
bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
bash
pip install -r requirements.txt

requirements.txt:

streamlit
pandas
google-genai
4. Get a Gemini API key

Create a free key at https://aistudio.google.com/apikey.

You can provide it in either of two ways:

Option A: Paste it in the app's sidebar when it opens.

Option B: Set it as an environment variable so it is filled in automatically:

bash
# Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"

# macOS / Linux
export GEMINI_API_KEY="your_api_key_here"
5. Run the app
bash
streamlit run app.py

The app opens in your browser at http://localhost:8501.

How to Use
Open the sidebar and enter your Gemini API key.
Choose the target role, difficulty and number of questions.
(Optional) Upload a question bank CSV.
Click 🚀 Start new interview.
Answer each question in the chat box.
When you are finished, click 📝 End interview & get feedback to see your report.
Question Bank CSV Format

The CSV needs at least one column whose name contains the word "question" (case-insensitive). Other columns are ignored.

Example questions.csv:

csv
question,category
What is the difference between a list and a tuple in Python?,Python
Explain overfitting and how to prevent it.,Machine Learning
Tell me about a time you handled a conflict in a team.,HR

Up to 30 random questions from the file are shared with the interviewer for each session.

How It Works
Prompt building: the app creates a system prompt from your chosen role, difficulty and question count (plus sample questions, if a CSV is uploaded).
Interview loop: the full chat history is sent to Gemini on every turn, so the interviewer remembers earlier answers. Streamlit's session_state stores the conversation.
Feedback generation: when you end the interview, the whole transcript is sent to Gemini with a separate "expert interview coach" prompt that returns a structured markdown report.
Security Note

Never commit your API key to GitHub. Use the sidebar field or an environment variable. If you use a .env file, add it to .gitignore.
Future Improvements:
Voice-based answers (speech-to-text) and spoken questions (text-to-speech)
Save and compare interview history and scores over time
Resume-based personalised questions
Export the feedback report as PDF
Support for more roles and domain-specific question banks
