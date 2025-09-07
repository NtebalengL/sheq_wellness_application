
import StatsChart from '../components/StatsChart'

export default function Stats() {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Teen Pregnancy & Online Risks</h2>
      <StatsChart/>
      <p className="mt-4 text-sm text-slate-600">Sources: Stats SA, UNICEF, World Bank.</p>
    </div>
  )
}
