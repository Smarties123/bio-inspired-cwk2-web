import { useState } from "react";
import { digits } from "../assets/sampleDigits";

export default function Controls({ onSubmit }) {
  const [digit, setDigit] = useState("zero");
  const [noise, setNoise] = useState(10);
  return (
    <div className="flex flex-col gap-4 p-4 bg-gray-50 rounded-2xl shadow">
      <select className="p-2 rounded border" value={digit} onChange={e=>setDigit(e.target.value)}>
        {Object.keys(digits).map(d=> <option key={d}>{d}</option>)}
      </select>
      <label className="flex flex-col gap-1">
        Noise: {noise}%
        <input type="range" min="0" max="100" value={noise} onChange={e=>setNoise(e.target.value)} />
      </label>
      <div className="flex gap-2">
        {[
          ["Cellular Automata","ca"],
          ["Hopfield","hop"],
          ["Autoencoder","ffn"]
        ].map(([txt,key])=>
          <button key={key} className="flex-1 bg-blue-600 hover:bg-blue-700 text-white rounded-xl p-2"
                  onClick={()=>onSubmit({digit,noise,model:key})}>{txt}</button>)
        }
      </div>
    </div>
  );
}