import React from 'react'
import Pane from './components/Pane'

export default function App(){
  return (
    <div className="min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        <header className="mb-6">
          <h1 className="text-3xl font-extrabold" style={{color:'var(--smoke-blue)'}}>XML Converter • R4010 / R4020</h1>
          <p className="text-gray-600">Validate, auto-fill minimally, batch every 50 files, and download converted lots.</p>
        </header>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Pane kind="r4010" label="R4010" />
          <Pane kind="r4020" label="R4020" />
        </div>
      </div>
    </div>
  )
}