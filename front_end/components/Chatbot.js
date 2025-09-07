import { useState, useRef, useEffect } from 'react'
import { SendHorizontal } from 'lucide-react'

export default function ChatBot() {
  const [messages, setMessages] = useState([
    { role: 'bot', text: "Hi! I'm your anonymous helper. Ask me about relationships, consent, sex, periods, or digital safety." }
  ])
  const [input, setInput] = useState("")
  const listRef = useRef(null)

  const send = () => {
    if (!input.trim()) return
    const userMsg = { role: 'user', text: input.trim() }
    setMessages(m => [...m, userMsg])
    setInput("")
    const reply = generateReply(userMsg.text)
    setTimeout(() => setMessages(m => [...m, { role: 'bot', text: reply }]), 400)
  }

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages])

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Ask the Bot (Anonymous)</h2>
      <div ref={listRef} className="h-80 overflow-y-auto border rounded-xl p-4 space-y-3 bg-white dark:bg-slate-800">
        {messages.map((m, i) => (
          <div key={i} className={`p-2 rounded-xl max-w-[80%] ${m.role === 'user' ? 'ml-auto bg-emerald-100 dark:bg-emerald-900' : 'bg-slate-200 dark:bg-slate-700'}`}>
            {m.text}
          </div>
        ))}
      </div>
      <div className="mt-3 flex gap-2">
        <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()} placeholder="Type your question..." className="flex-1 border rounded-lg p-2"/>
        <button onClick={send} className="bg-emerald-500 text-white px-3 rounded-lg"><SendHorizontal className="w-4 h-4"/></button>
      </div>
    </div>
  )
}

function generateReply(text) {
  const t = text.toLowerCase()
  if (t.includes("sex")) return "Sex should always be safe and consensual. You never have to do anything you don’t want."
  if (t.includes("pregnan")) return "If you think you might be pregnant, take a test at a clinic. They offer confidential advice."
  if (t.includes("abuse")) return "If you feel unsafe, call 10111 or Childline 116. You're not alone."
  return "I can share general advice on relationships, consent, periods, and staying safe online."
}
