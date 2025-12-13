from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.bias_analysis import run_bias_analysis
from utils.smote import run_smote

import shutil, os, pandas as pd, uuid

# -------------------- APP SETUP --------------------
app = FastAPI(title="CSV Bias & SMOTE API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------- HELPERS --------------------
def create_output_dir(base_name: str):
    out_dir = os.path.join(OUTPUT_DIR, base_name)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir

def detect_target(df: pd.DataFrame):
    possible = [c for c in df.columns if df[c].nunique() <= 20]
    if not possible:
        raise ValueError("No suitable target column found.")
    return possible[-1]

def compute_sample_weights(df, sensitive, target):
    freq = (
        df.groupby([sensitive, target])
        .size()
        .reset_index(name="count")
    )
    total = freq["count"].sum()
    freq["weight"] = total / (freq["count"] * len(freq))
    return freq

def generate_weighted_datasets(df, target, sensitive_cols, out_dir):
    for col in sensitive_cols:
        freq = compute_sample_weights(df, col, target)
        weighted = df.merge(freq, on=[col, target], how="left")
        weighted.to_csv(
            os.path.join(out_dir, f"weighted_{col}.csv"),
            index=False,
        )

# -------------------- API ENDPOINTS --------------------
@app.post("/process")
async def process_csv(file: UploadFile = File(...)):
    uid = uuid.uuid4().hex
    base_name = f"{os.path.splitext(file.filename)[0]}_{uid}"

    upload_path = os.path.join(UPLOAD_DIR, f"{base_name}.csv")

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = pd.read_csv(upload_path)

    out_dir = create_output_dir(base_name)

    target = detect_target(df)
    sensitive_cols = run_bias_analysis(df, target, out_dir)
    run_smote(df, target, out_dir)
    generate_weighted_datasets(df, target, sensitive_cols, out_dir)

    files = sorted(os.listdir(out_dir))

    return {
        "folder": base_name,
        "files": [
            f"/download/{base_name}/{f}" for f in files
        ],
    }

@app.get("/download/{folder}/{filename}")
def download_file(folder: str, filename: str):
    file_path = os.path.join(OUTPUT_DIR, folder, filename)
    return FileResponse(file_path, filename=filename)