import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";
export default function AccuracyChart({ items }) {
  return (
    <BarChart width={400} height={250} data={items} className="mt-4">
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis domain={[0,100]} />
      <Tooltip />
      <Bar dataKey="accuracy" />
    </BarChart>
  );
}