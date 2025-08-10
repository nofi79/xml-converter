const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function startConvert(kind: 'r4010'|'r4020', zip: File){
  const fd = new FormData();
  fd.append('file', zip);
  const r = await fetch(`${BASE}/convert/${kind}`, { method: 'POST', body: fd });
  if(!r.ok) throw new Error('Failed to start');
  return r.json() as Promise<{job_id: string, total: number}>;
}

export async function poll(job_id: string){
  const r = await fetch(`${BASE}/progress/${job_id}`);
  if(!r.ok) throw new Error('Progress error');
  return r.json() as Promise<{status: string, done: number, total: number}>;
}

export function download(job_id: string){
  const url = `${BASE}/download/${job_id}`;
  const a = document.createElement('a');
  a.href = url; a.download = '';
  document.body.appendChild(a); a.click(); a.remove();
}