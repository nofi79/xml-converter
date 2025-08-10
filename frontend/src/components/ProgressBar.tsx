import React from 'react'

export default function ProgressBar({done,total}:{done:number,total:number}){
  const pct = total>0 ? Math.round((done/total)*100) : 0;
  return (
    <div className="w-full">
      <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
        <div className="h-3" style={{width: `${pct}%`, backgroundColor: 'var(--smoke-blue)'}}></div>
      </div>
      <div className="text-sm mt-1">{done}/{total} files • {pct}%</div>
    </div>
  )
}