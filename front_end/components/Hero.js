import Image from 'next/image'
import { MessageCircle } from 'lucide-react'
import Link from 'next/link'

export default function Hero() {
  return (
    <div className="grid md:grid-cols-2 gap-8 items-center">
      <div>
        <h1 className="text-3xl md:text-5xl font-extrabold">
          Anonymous <span className="text-emerald-600">advice</span> & judgement-free <span className="text-sky-600">answers</span>
        </h1>
        <p className="mt-4 text-lg text-slate-700 dark:text-slate-300">
          Talk about relationships, consent, sex, periods, and safety in private. No signup needed.
        </p>
        <div className="mt-6 flex gap-4">
          <Link href="/chat" className="bg-emerald-500 text-white px-4 py-2 rounded-lg flex items-center gap-2">
            <MessageCircle className="w-4 h-4"/> Ask the Bot
          </Link>
          <Link href="/about" className="border px-4 py-2 rounded-lg">What is SHEQ+?</Link>
        </div>
      </div>
      <div className="aspect-square w-full max-w-md mx-auto">
        <Image src="/ai-teen-hero.png" alt="Teen illustration" width={400} height={400} className="rounded-3xl"/>
      </div>
    </div>
  )
}
