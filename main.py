from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from supabase import create_client, Client

url = "https://rfhfjcrdxfofgycpirkv.supabase.co" 
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJmaGZqY3JkeGZvZmd5Y3Bpcmt2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE4MzkzNDIsImV4cCI6MjA1NzQxNTM0Mn0.XNcm1ZEMoDacqKGR-397eoJr_bvmiX6TN_JaJrHmmd8"
supabase: Client = create_client(url, key)

app = FastAPI()

class QuizQuestion(BaseModel):
    id: int
    type: str
    difficulty: str
    category: str
    question: str
    correct_answer: str
    
@app.get("/")
def root():
    return {"message": "Trivia Quiz API using Supabase!"}

@app.get("/questions/", response_model=List[QuizQuestion])

def get_all_questions():
    response = supabase.table("quiz_questions").select("*").execute()
    return response.data


@app.get("/questions/{question_id}", response_model=QuizQuestion)
def get_question(question_id: int):
    response = supabase.table("quiz_questions").select("*").eq("ID", question_id).single().execute()
    if response.data:
        return response.data
    raise HTTPException(status_code=404, detail="Question not found")

@app.post("/questions/", response_model=QuizQuestion)
def create_question(q: QuizQuestion):
    existing = supabase.table("quiz_questions").select("ID").eq("ID", q.id).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Question ID already exists")
    response = supabase.table("quiz_questions").insert(q.dict()).execute()
    return response.data[0]

@app.put("/questions/{question_id}", response_model=QuizQuestion)
def update_question(question_id: int, q: QuizQuestion):
    response = supabase.table("quiz_questions").update(q.dict()).eq("ID", question_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Question not found")
    return response.data[0]

@app.delete("/questions/{question_id}")
def delete_question(question_id: int):
    response = supabase.table("quiz_questions").delete().eq("ID", question_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted", "question": response.data[0]}
