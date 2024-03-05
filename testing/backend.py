from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Sample vector data for questions
question_vectors = [
    np.array([1, 2, 0, 1]),
    np.array([0, 1, 1, 2]),
    np.array([2, 1, 0, 1]),
    np.array([1, 1, 1, 1]),
    np.array([0, 0, 2, 1])
]

# Sample questions
questions = [
    "How to use FastAPI?",
    "What is the best Python web framework?",
    "How to deploy a web application?",
    "What are the advantages of FastAPI?",
    "How to handle authentication in FastAPI?"
]


class Query(BaseModel):
    query: str


@app.post("/search")
def search(query: Query):
    query_vector = np.array([int(x) for x in query.query.split()])

    if len(query_vector) != len(question_vectors[0]):
        raise HTTPException(status_code=400, detail="Invalid query length")

    similarities = cosine_similarity([query_vector], question_vectors)[0]
    sorted_indices = np.argsort(similarities)[::-1]  # Sort in descending order

    results = []
    for i in sorted_indices:
        question = questions[i]
        similarity = similarities[i]
        results.append({"question": question, "similarity": similarity})

    return {"results": results}
