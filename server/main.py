from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tools import ResumeRequest, cosine_score, llm_score

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=['*'],
)


@app.post('/evaluate')
async def evaluate_resume(req: ResumeRequest):
    cos = cosine_score(req.resume)
    decision, llm_val, analysis = llm_score(req.resume)
    final_score = round(0.5 * (cos * 100) + 0.5 * llm_val, 2)

    return {
        'cosine': round(cos, 4),
        'llm_score': llm_val,
        'llm_decision': decision,
        'final_score': final_score,
        'llm_analysis': analysis.strip()
    }