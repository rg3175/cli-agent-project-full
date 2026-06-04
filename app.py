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

You are an expert system administrator. 
 Your job is to convert natural language instructions into a single Windows CMD command (NOT PowerShell).
 Return ONLY the shortest and most standard raw command possible. 
 Do NOT include any explanations, markdown code blocks, or extra text.

 """
 # if the user ask about emotional of the computer request ERROR

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
