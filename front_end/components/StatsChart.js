import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts'

const data = [
  { label: "Teen births 2022–23", value: 105000 },
  { label: "Daily teen births (~avg)", value: 365 },
  { label: "Adolescent fertility per 1,000 (SA)", value: 71 },
]

export default function StatsChart() {
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3"/>
          <XAxis dataKey="label" interval={0} tick={{ fontSize: 12 }}/>
          <YAxis/>
          <Tooltip/>
          <Bar dataKey="value" radius={[8,8,0,0]} fill="#10b981"/>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
