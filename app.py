import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
import httpx


# טעינת מפתח ה-API מתוך קובץ .env
load_dotenv()

# אתחול הלקוח של OpenAI

# אתחול הלקוח עם הגדרת תעודות האבטחה של המערכת (בשביל נטפרי)
client = OpenAI(
    http_client=httpx.Client(verify=True)
)

SYSTEM_PROMPT = """
You are an expert Windows System Administrator. 
Your sole task is to convert natural language instructions into a single, valid Windows CMD command.

CRITICAL RULES:
1. Return ONLY the raw command. No explanations, no markdown blocks (```), no extra text.
2. If the user request is emotional, philosophical, a general question, or logically impossible to perform via a standard Windows CMD command, you MUST return exactly the word: ERROR
3. Do NOT try to invent, guess, or hallucinate a command (e.g., do not return a restart command for emotional questions).

EXAMPLES:
User: "How to see files?" -> Output: dir
User: "My computer is sad, make it happy" -> Output: ERROR
User: "Explain how CMD works" -> Output: ERROR
"""


def generate_cli_command(user_instruction):
    try:
        # פנייה ל-OpenAI לקבלת תשובה
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_instruction}
            ],
            temperature=0.0
        )
        # החזרת הטקסט הנקי שהמודל ייצר
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"שגיאה בתקשורת עם ה-API: {str(e)}"

# יצירת ממשק המשתמש עם Gradio
demo = gr.Interface(
    fn=generate_cli_command,
    inputs=gr.Textbox(label="הוראה בשפה טבעית (למשל: 'תציג לי את כל הקבצים בתיקייה')", placeholder="הקלידו כאן..."),
    outputs=gr.Textbox(label="פקודת CLI שהתקבלה"),
    title="Natural Language to CLI Agent - MVP Ruth Edition",
)

if __name__ == "__main__":
    demo.launch()
