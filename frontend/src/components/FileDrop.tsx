import React, {useRef, useState} from 'react'

export default function FileDrop({onSelect}:{onSelect:(file:File)=>void}){
  const ref = useRef<HTMLInputElement>(null);
  const [name,setName] = useState<string>('');
  return (
    <div className="border-2 border-dashed rounded-xl p-6 text-center" style={{borderColor:'var(--smoke-blue)'}} onClick={()=>ref.current?.click()}>
      <input ref={ref} type="file" accept=".zip" className="hidden" onChange={e=>{
        const f = e.target.files?.[0]; if(f){ setName(f.name); onSelect(f); }
      }} />
      <div className="font-medium">Drop or click to choose a .zip with XMLs</div>
      <div className="text-xs text-gray-600 mt-1">Max recommended 10k files per run</div>
      {name && <div className="mt-2 text-sm">Selected: <b>{name}</b></div>}
    </div>
  )
}