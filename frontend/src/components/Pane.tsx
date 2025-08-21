import React, {useEffect, useState} from 'react'
import FileDrop from './FileDrop'
import ProgressBar from './ProgressBar'
import { startConvert, poll, download } from '../api'

export default function Pane({kind,label}:{kind:'r4010'|'r4020', label:string}){
  const [file,setFile] = useState<File|null>(null)
  const [job,setJob] = useState<string|undefined>()
  const [total,setTotal] = useState<number>(0)
  const [done,setDone] = useState<number>(0)
  const [status,setStatus] = useState<string>('idle')

  useEffect(()=>{
    if(!job) return;
    let stop=false;
    async function tick(){
      const s = await poll(job);
      setStatus(s.status); setDone(s.done); setTotal(s.total)
      if(s.status==='done') return;
      if(!stop) setTimeout(tick, 400);
    }
    tick();
    return ()=>{stop=true}
  },[job])

  const start = async ()=>{
    if(!file) return;
    setStatus('starting');
    const r = await startConvert(kind, file);
    setJob(r.job_id); setTotal(r.total); setDone(0); setStatus('running');
  }

  const canConvert = !!file && (status==='idle' || status==='done' || status==='error');

  return (
    <div className="card flex flex-col gap-4">
      <div className="text-xl font-bold" style={{color:'var(--smoke-blue)'}}>{label}</div>
      <FileDrop onSelect={setFile} />
      <button className="btn" disabled={!canConvert} onClick={start}>Convert</button>
      {(status==='running' || status==='starting') && <ProgressBar done={done} total={total} />}
      {status==='done' && (
        <div className="flex items-center gap-2">
          <span className="text-green-700 font-medium">Conversão finalizada.</span>
          <button className="btn" onClick={()=> job && download(job)}>Download ZIP</button>
        </div>
      )}
    </div>
  )
}