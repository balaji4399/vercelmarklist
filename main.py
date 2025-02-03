from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# CORS setup
origins = ["*"]  # Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Only allow GET requests
    allow_headers=["*"],
)
file_path = 'q-vercel-python.json'
with open(file_path, 'r') as f:
    students_marks_list = json.load(f)

# Convert the list of dictionaries to a dictionary
students_marks = {student['name']: student['marks'] for student in students_marks_list}
# Load student data (replace with your actual file loading)
# Handle the case where the file isn't found.  Provide some default data if needed.

@app.get("/api")
async def get_marks(name: list[str] = Query(None)): # Allows for multiple name parameters
    if name is None:
        raise HTTPException(status_code=400, detail="At least one name must be provided.")

    marks = []
    not_found = []
    for n in name:
      if n in students_marks:
        marks.append(students_marks[n])
      else:
        not_found.append(n)

    if not_found:
      error_message = f"Names not found: {', '.join(not_found)}"
      if marks: # some names were found
          return {"marks": marks, "message": error_message}
      else: # no names were found
          raise HTTPException(status_code=404, detail=error_message)

    return {"marks": marks}