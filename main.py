from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the marks data from q-vercel-python.json
file_path = os.path.join(os.path.dirname(__file__), 'q-vercel-python.json')
with open(file_path, 'r') as f:
    students_marks_list = json.load(f)

# Convert the list of dictionaries to a dictionary
students_marks = {student['name']: student['marks'] for student in students_marks_list}

@app.get("/api")
async def get_marks(request: Request):
    query_params = request.query_params
    names = query_params.getlist("name")
    if not names:
        raise HTTPException(status_code=400, detail="At least one name must be provided.")
    
    marks = []
    not_found = []
    for name in names:
        if name in students_marks:
            marks.append(students_marks[name])
        else:
            not_found.append(name)
    
    response = {"marks": marks}
    if not_found:
        response["message"] = f"Names not found: {', '.join(not_found)}"
    
    return json.dumps(response)