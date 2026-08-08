from fastapi import FastAPI

app = FastAPI(
    title="Narrative Disinformation Simulator & Detector",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Narrative Disinformation Simulator API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }