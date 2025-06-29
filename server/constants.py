OLLAMA_URL = "http://ollama:11434/api/generate"
MODEL = "deepseek-r1:1.5b"
PROMPT = """
You are an AI recruiter. Compare the following resume to the job description.

- Give a detailed comparison of how well the resume fits the job.
- Identify strengths and weaknesses.
- Conclude with:
    1. A boolean: Does this resume match the job well? (Yes/No)
    2. A score from 0 to 100 indicating how strong the match is.

RESUME:
{}

JOB DESCRIPTION:
{}

End your response with:
Answer: <Yes/No>
Score: <0–100>
"""