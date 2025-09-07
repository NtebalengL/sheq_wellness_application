export default function FAQ() {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">FAQ</h2>
      <details className="p-3 border rounded-lg">
        <summary>How do I have sex for the first time safely?</summary>
        <p className="mt-2">Your first time should always be consensual and safe. Condoms and contraception reduce risks. 
          <sub><a href="/faq">Learn more</a></sub>
        </p>
      </details>
      <details className="p-3 border rounded-lg">
        <summary>What if I think I’m pregnant?</summary>
        <p className="mt-2">Take a test at a clinic. Confidential help is available. 
          <sub><a href="/faq">Learn more</a></sub>
        </p>
      </details>
    </div>
  )
}

