from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import re, requests
from constants import PROMPT, MODEL, OLLAMA_URL

class ResumeRequest(BaseModel):
    resume: str


# Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')


# Load job description
with open('job_description.txt', 'r', encoding='utf-8') as f:
    job_desc = f.read()
job_emb = embedder.encode(job_desc, convert_to_tensor=True)


def cosine_score(resume_text):
    resume_emb = embedder.encode(resume_text, convert_to_tensor=True)
    return util.cos_sim(resume_emb, job_emb).item()


def llm_score(resume_text: str):
    prompt = PROMPT.format(resume_text, job_desc)
    payload = {'model': MODEL, 'prompt': prompt, 'stream': False}

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        text = response.json()['response']

        match = re.search(r'Answer\s*:\s*(Yes|No)', text, re.IGNORECASE)
        score_match = re.search(r'Score\s*:\s*(\d{1,3})', text)

        decision = match.group(1).capitalize() if match else 'Unknown'
        score = int(score_match.group(1)) if score_match else 0

        return decision, score, text
    except Exception as e:
        return 'Error', 0, f'LLM error: {e}'