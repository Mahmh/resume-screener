import React, { useState } from 'react'

export default function App() {
    const [resumeText, setResumeText] = useState("")
    const [jobText, setJobText] = useState("")
    const [output, setOutput] = useState<any>(null)
    const [loading, setLoading] = useState(false)

    const handleFile = (
        e: React.ChangeEvent<HTMLInputElement>,
        setText: (v: string) => void
    ) => {
        const file = e.target.files?.[0]
        if (!file) return

        const reader = new FileReader()
        reader.onload = () => setText(reader.result as string)
        reader.readAsText(file)
    }

    const handleSubmit = async () => {
        if (!resumeText || !jobText)
            return alert("Both resume and job description are required.")
        setOutput(null)
        setLoading(true)
        try {
            const res = await fetch("http://localhost:8000/evaluate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ resume: resumeText, job: jobText })
            })
            const data = await res.json()
            setOutput(data)
        } catch (err) {
            console.error(err)
            alert("Error evaluating resume.")
        }
        setLoading(false)
    }

    return (
        <div className="container">
            <h1>Resume Matcher</h1>

            <div className="input-panel">
                <h2>Resume</h2>
                <textarea
                    value={resumeText}
                    onChange={e => setResumeText(e.target.value)}
                    placeholder="Paste resume text here..."
                    rows={6}
                />
                <input
                    type="file"
                    accept=".txt"
                    onChange={e => handleFile(e, setResumeText)}
                />

                <h2>Job Description</h2>
                <textarea
                    value={jobText}
                    onChange={e => setJobText(e.target.value)}
                    placeholder="Paste job description here..."
                    rows={6}
                />
                <input
                    type="file"
                    accept=".txt"
                    onChange={e => handleFile(e, setJobText)}
                />

                <br/>

                <button onClick={handleSubmit} disabled={loading} id='eval-btn'>
                    {loading ? "Evaluating..." : "Evaluate Resume"}
                </button>
            </div>

            <div className="output-panel">
                {output && (
                    <>
                        <h2>Result</h2>
                        <p>
                            <strong>Final Score:</strong> {output.final_score}
                        </p>
                        <h3>AI Analysis</h3>
                        <pre>{output.llm_analysis}</pre>
                    </>
                )}
            </div>
        </div>
    )
}