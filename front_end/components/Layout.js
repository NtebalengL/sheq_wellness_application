import Link from 'next/link'
import { useState, useEffect } from 'react'
import { Sun, Moon, MessageCircle } from 'lucide-react'

export default function Layout({ children }) {
  const [theme, setTheme] = useState('light')

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])

  return (
    <div className="min-h-screen bg-gradient-to-b from-cyan-50 to-blue-50 dark:from-slate-900 dark:to-slate-950 text-slate-900 dark:text-slate-100">
      <header className="p-4 flex justify-between bg-white dark:bg-slate-900 shadow">
        <Link href="/"><h1 className="font-bold text-xl">SHEQ+</h1></Link>
        <div className="flex gap-4 items-center">
          <Link href="/about">About</Link>
          <Link href="/stats">Stats</Link>
          <Link href="/chat">Chat</Link>
          <Link href="/clinics">Clinics</Link>
          <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
            {theme === 'dark' ? <Sun /> : <Moon />}
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto p-4">{children}</main>

      <a href="https://wa.me/27787490431" 
         className="fixed bottom-4 right-4 bg-emerald-500 text-white p-3 rounded-full shadow-lg flex items-center gap-2">
        <MessageCircle className="w-4 h-4"/> Chat on WhatsApp
      </a>
    </div>
  )
}
