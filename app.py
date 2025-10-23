from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import joblib
import pandas as pd
from pathlib import Path


# --- Resolve model path ---
BASE = Path(__file__).resolve().parent
candidate_paths = [
    BASE / "model" / "regression.joblib",
    BASE / "models" / "regression.joblib",
    BASE / "ML" / "Supervised" / "Regression" / "model" / "regression.joblib",
    BASE.parent / "ML" / "Supervised" / "Regression" / "model" / "regression.joblib",
]
MODEL_PATH = next((p for p in candidate_paths if p.exists()), None)
if MODEL_PATH is None:
    raise FileNotFoundError(
        f"regression.joblib not found in expected locations. Tried: {[str(p) for p in candidate_paths]}"
    )

# load model
pipe = joblib.load(str(MODEL_PATH))


# --- FastAPI app ---
app = FastAPI(title="House Price regression API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Serve a small static demo (web/index.html)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
static_dir = BASE / "web"
if static_dir.exists():
    # mount under /static so API routes aren't shadowed
    app.mount("/static", StaticFiles(directory=str(static_dir), html=True), name="static")

    @app.get("/")
    def root():
        index = static_dir / "index.html"
        return FileResponse(str(index))


# --- Pydantic schemas ---
class Record(BaseModel):
    Area: Optional[float] = Field(None)
    Room: Optional[float] = Field(None)


class Batch(BaseModel):
    records: List[Record]


@app.get("/health")
def health():
    return {"status": "ok", "model_path": str(MODEL_PATH)}


@app.post("/predict")
def predict(batch: Batch):
    """Typed endpoint: accepts {"records": [{...}, ...]} where each record follows Record schema."""
    try:
        rows = [ {k: v for k, v in r.model_dump().items() if v is not None} for r in batch.records ]
        if not rows:
            raise HTTPException(status_code=400, detail="No records provided")
        df = pd.DataFrame(rows)
        preds = pipe.predict(df)
        return {"predictions": [float(p) for p in preds]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict_raw")
def predict_raw(batch: List[Dict[str, Any]]):
    """Flexible endpoint: accept a JSON array of dicts (arbitrary keys) and attempt prediction.
    Useful for mobile/web clients that send JSON directly matching model columns.
    """
    try:
        if not isinstance(batch, list) or len(batch) == 0:
            raise HTTPException(status_code=400, detail="Expecting a non-empty list of records")
        df = pd.DataFrame(batch)
        preds = pipe.predict(df)
        return {"predictions": [float(p) for p in preds]}
    except HTTPException:
        raise
    except Exception as e:
        detail = str(e)
        try:
            if hasattr(pipe, 'named_steps'):
                detail += "; pipeline steps: " + ",".join(pipe.named_steps.keys())
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=detail)


if __name__ == "__main__":
    print("This module is meant to be run with an ASGI server, e.g.:")
    print("uvicorn app:app --reload")
