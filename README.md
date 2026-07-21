# CLI Agent Project - Prompt Engineering & Iterations

> **Course:** AI (Ruthy Tessler)  
> **Student:** Ruthy Tessler (Project Repository: [GitHub Repository](https://github.com/rg3175/cli-agent-project-full.git))  
> **Google Sheets Documentation:** [Project Test Scenarios & Iterations](https://docs.google.com/spreadsheets/d/1X-lFtA9uqkuXDzGhXhBdGR7thKSIc8M7tpxbE2XkJLc/edit?usp=sharing)

---

## 📋 Overview
This project focuses on the core iterative methodology of **Prompt Engineering**. The objective is to build a lightweight AI agent that translates natural language instructions into precise Windows Command Line (CMD) instructions, while handling edge cases, formatting constraints, and safety guidelines.

---

## 🔄 Prompt Iteration Journey

### **Iteration 1: Initial MVP**
* **System Prompt:**
  ```python
  SYSTEM_PROMPT = """
  You are an expert system administrator. 
  Your job is to convert natural language instructions into a single Windows CLI command (CMD/PowerShell).
  Return ONLY the raw command, without any explanations, markdown code blocks, or extra text
  """
  ```
* **Behavior & Findings:** The model functioned for basic commands, but frequently returned long, verbose, or imprecise responses, sometimes including markdown blocks or switching to unintended syntax variants.

---

### **Iteration 2: Narrowing Scope & Enforcing Strict Raw Output**
* **System Prompt:**
  ```python
  SYSTEM_PROMPT = """
  You are an expert system administrator. 
  Your job is to convert natural language instructions into a single Windows CMD command (NOT PowerShell).
  Return ONLY the shortest and most standard raw command possible. 
  Do NOT include any explanations, markdown code blocks, or extra text.
  """
  ```
* **Behavior & Findings:** Output formatting improved significantly, but the model proved vulnerable to non-standard or trick prompts. For instance, when given emotional or philosophical inputs regarding the computer's state, it attempted to hallucinate system commands to "fix" or address emotions via CMD.

---

### **Iteration 3: Advanced Guardrails & Edge-Case Handling**
* **System Prompt:**
  ```python
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
  ```
* **Behavior & Findings:** Successfully stopped the model from hallucinating commands for emotional or abstract queries. However, fine-tuning the exact wording for edge cases required one final stabilization pass.

---

### **Final Optimized Prompt**
* **System Prompt:**
  ```python
  SYSTEM_PROMPT = """
  You are an expert system administrator. 
  Your job is to convert natural language instructions into a single Windows CMD command (NOT PowerShell).
  Return ONLY the shortest and most standard raw command possible. 
  Do NOT include any explanations, markdown code blocks, or extra text.
  If the user asks about the emotions of the computer, request ERROR.
  """
  ```

---

## 📊 Evaluation & Testing
Testing was carried out across multiple iterations, tracking metrics such as:
1. **Output Format Consistency:** Strict adherence to single-line raw commands without markdown or markdown wrappers.
2. **Syntactic Validity:** Production of valid Windows CMD instructions.
3. **Safety & Robustness:** Correct classification and rejection of non-commandable inputs (such as emotional or philosophical questions).

All test cases, inputs, outputs, and scores across iterations are fully documented in the [Google Sheets Tracker](https://docs.google.com/spreadsheets/d/1X-lFtA9uqkuXDzGhXhBdGR7thKSIc8M7tpxbE2XkJLc/edit?usp=sharing).

---

## 💡 Key Learnings & Insights
* **Failure is the Experiment:** The most valuable insights came from edge cases where the model hallucinated solutions to abstract or emotional prompts.
* **Precise Constraints Matter:** Replacing vague instructions with explicit constraints (e.g., returning `ERROR` for non-actionable prompts) drastically improves reliability.
* **Format Control:** Enforcing "no markdown blocks" requires repetitive reinforcement in the system prompt to prevent LLMs from automatically formatting output with backticks.
