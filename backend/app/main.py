from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from .config import settings
from .services.zip_utils import unzip_all, zip_pairs
from .services.jobs import store
from .services.xsd_loader import SchemaRegistry
from .converters.r4010 import R4010Converter
from .converters.r4020 import R4020Converter
import asyncio

app = FastAPI(title="R4010/R4020 XML Converter")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

registry = SchemaRegistry()
conv_map = {
    "r4010": R4010Converter(registry),
    "r4020": R4020Converter(registry),
}

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/schemas")
async def list_schemas():
    return {"r4010": settings.XSD_R4010, "r4020": settings.XSD_R4020}

@app.post("/convert/{kind}")
async def convert_zip(kind: str, file: UploadFile = File(...)):
    if kind not in conv_map:
        raise HTTPException(400, "invalid kind")
    content = await file.read()
    pairs = unzip_all(content)
    total = len(pairs)
    job = store.create(total=total)

    async def worker():
        job.status = "running"
        conv = conv_map[kind]
        out_pairs = []
        for idx, (name, data) in enumerate(pairs, start=1):
            try:
                new_name, xml_bytes = conv.convert(name, data)
                out_pairs.append((new_name, xml_bytes))
            except Exception as e:
                # keep original if conversion fails
                out_pairs.append((name, data))
            finally:
                job.done = idx
                await asyncio.sleep(0)  # yield
        # Batch into groups of 50
        batched = []
        batch_size = settings.MAX_BATCH_SIZE
        for i in range(0, len(out_pairs), batch_size):
            sub = out_pairs[i:i+batch_size]
            # Each batch becomes its own zip entry (nested zip) to reflect lotes
            batch_zip = zip_pairs(sub)
            batched.append((f"lote_{i//batch_size + 1}.zip", batch_zip))
        job.result_zip = zip_pairs(batched)
        job.status = "done"

    asyncio.create_task(worker())
    return {"job_id": job.id, "total": total}

@app.get("/progress/{job_id}")
async def progress(job_id: str):
    job = store.get(job_id)
    if not job:
        raise HTTPException(404)
    return {"status": job.status, "done": job.done, "total": job.total}

@app.get("/download/{job_id}")
async def download(job_id: str):
    job = store.get(job_id)
    if not job:
        raise HTTPException(404)
    if job.status != "done" or not job.result_zip:
        raise HTTPException(409, "not ready")
    return StreamingResponse(iter([job.result_zip]), media_type="application/zip", headers={
        "Content-Disposition": f"attachment; filename=convertidos_{job_id}.zip"
    })