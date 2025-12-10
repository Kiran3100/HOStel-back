# Auto-generated placeholder file for hostel-management-saas.

from fastapi import FastAPI

app = FastAPI(title="Hostel Management SaaS")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
