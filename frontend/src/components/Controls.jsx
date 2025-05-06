import { useState, useEffect } from "react";
// import { emojis } from "../assets/sampleEmojis";

export default function Controls({ datasets, onSubmit }) {
  const [dataset, setDataset] = useState("mnist");
  const [selKey, setSelKey] = useState(null);
  const [noise,  setNoise]  = useState(10);

  useEffect(() => {
    const keys = Object.keys(datasets[dataset].samples);
    if (keys.length && !keys.includes(selKey)) setSelKey(keys[0]);
  }, [dataset, datasets]);

  const { label, samples } = datasets[dataset];

  const MODELS = [
    ["Cellular CA", "ca"],
    ["Hopfield PI",   "hopfield"],
    ["SOM-KNN",       "som"],
    ["Hybrid LAM Enhanced", "hybrid"]
  ];

  return (
    <aside className="flex flex-col gap-6">
      {/* dataset toggle */}
      <div className="flex gap-2">
        {Object.entries(datasets).map(([k,{label}])=>(
          <button key={k} onClick={()=>setDataset(k)}
            className={`px-3 py-1 rounded-full border ${
              dataset===k?"bg-indigo-600 text-white":"bg-white"
            }`}>
            {label}
          </button>
        ))}
      </div>

      {/* sample picker */}
      <div className="grid grid-cols-5 gap-2">
        {Object.entries(samples).map(([k,src])=>(
          <img key={k} src={src}
            onClick={()=>setSelKey(k)}
            className={`w-16 h-16 cursor-pointer border-4 rounded-xl ${
              selKey===k?"border-indigo-600":"border-transparent"
            }`} />
        ))}
      </div>

      {/* noise slider */}
      <label className="flex flex-col gap-1">
        Noise {noise}%
        <input type="range" min="0" max="100" value={noise}
               onChange={e=>setNoise(+e.target.value)} />
      </label>

      {/* run buttons */}
      <div className="grid grid-cols-2 gap-2">
        {MODELS.map(([txt,key])=>(
          <button key={key}
            className="rounded-xl py-2 font-semibold bg-gradient-to-br from-indigo-500 to-indigo-700 text-white hover:brightness-110 disabled:opacity-50"
            disabled={!selKey}
            onClick={()=>onSubmit({ key:selKey, noise, model:key, dataset })}>
            {txt}
          </button>
        ))}
      </div>
    </aside>
  );
}
