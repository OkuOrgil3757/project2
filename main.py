from fastapi import FastAPI, HTTPException
import pandas as pd
import os

app = FastAPI()

CSV_FILE = "quiz_questions.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=["id", "type", "difficulty", "category", "question", "correct_answer"])
        df.to_csv(CSV_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(CSV_FILE, index=False)
    return df

@app.get("/questions")
def get_all_questions():
    df = load_data()
    return df.to_dict(orient="records")

@app.post("/questions")
def create_question(type: str, difficulty: str, category: str, question: str, correct_answer: str):
    df = load_data()
    new_id = int(df["id"].max()) + 1 if not df.empty else 1
    df.loc[len(df)] = [new_id, type, difficulty, category, question, correct_answer]
    save_data(df)
    return {"id": new_id, "question": question}

@app.put("/questions/{question_id}")
def update_question(question_id: int, type: str, difficulty: str, category: str, question: str, correct_answer: str):
    df = load_data()
    if question_id not in df["id"].values:
        raise HTTPException(status_code=404, detail="Question not found")
    df.loc[df["id"] == question_id, ["type", "difficulty", "category", "question", "correct_answer"]] = [
        type, difficulty, category, question, correct_answer
    ]
    save_data(df)
    return {"message": "Question updated successfully"}

@app.delete("/questions/{question_id}")
def delete_question(question_id: int):
    df = load_data()
    if question_id not in df["id"].values:
        raise HTTPException(status_code=404, detail="Question not found")
    df = df[df["id"] != question_id]
    save_data(df)
    return {"message": "Question deleted successfully"}
