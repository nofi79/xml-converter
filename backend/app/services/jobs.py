import asyncio
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class Job:
    id: str
    total: int
    done: int = 0
    status: str = "queued"  # queued|running|done|error
    error: str | None = None
    result_zip: bytes | None = None

class JobStore:
    def __init__(self):
        self.jobs: Dict[str, Job] = {}

    def create(self, total: int) -> Job:
        jid = str(uuid.uuid4())
        job = Job(id=jid, total=total)
        self.jobs[jid] = job
        return job

    def get(self, jid: str) -> Job | None:
        return self.jobs.get(jid)

store = JobStore()