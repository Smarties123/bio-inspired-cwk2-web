import { useState } from "react";
import Controls from "./components/Controls";
import ImageCanvas from "./components/ImageCanvas";
import AccuracyChart from "./components/AccuracyChart";
import { digits } from "./assets/sampleDigits";
import { generateNoise, runCA, runHop, runFFN } from "./api";

export default function App() {
  const [orig, setOrig]       = useState(null);
  const [noisy, setNoisy]     = useState(null);
  const [recon, setRecon]     = useState(null);
  const [chartData, setChart] = useState([]);

  const handleSubmit = async ({digit, noise, model}) => {
    // build original png via backend util for consistency
    const payload = { image: digits[digit], noise };
    const {data: nres} = await generateNoise(payload);
    setOrig(digits[digit]);
    setNoisy(nres.reconstructed);

    let res;
    if (model === "ca")   res = await runCA(payload);
    if (model === "hop")  res = await runHop(payload);
    if (model === "ffn")  res = await runFFN(payload);

    const acc = res.data.accuracy;
    setRecon(res.data.reconstructed);
    setChart(prev=>[...prev.filter(i=>i.name!==model.toUpperCase()), {name:model.toUpperCase(), accuracy:acc}]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6 text-gray-800">
      <h1 className="text-3xl font-bold mb-6 text-center">Bio‑Inspired Memory Demo</h1>
      <div className="grid md:grid-cols-4 gap-6 max-w-5xl mx-auto">
        <Controls onSubmit={handleSubmit} className="col-span-1" />
        <div className="col-span-3 flex flex-col items-center gap-4">
          <div className="flex gap-4">
            {orig && <ImageCanvas label="Original" src={orig} />}
            {noisy && <ImageCanvas label="Noisy" src={noisy} />}
            {recon && <ImageCanvas label="Reconstructed" src={recon} />}
          </div>
          {chartData.length>0 && <AccuracyChart items={chartData} />}
        </div>
      </div>
    </div>
  );
}