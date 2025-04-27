import { useEffect, useState } from "react";
import axios from "axios";

import Navbar        from "./components/Navbar";
import Controls      from "./components/Controls";
import ImageCanvas   from "./components/ImageCanvas";
import AccuracyChart from "./components/AccuracyChart";
import { emojis }    from "./assets/sampleEmojis";

import { generateNoise, runCA, runHop, runFFN } from "./api";

export default function App() {
  const [mnist, setMnist] = useState({});
  const [orig,  setOrig]  = useState(null);
  const [noisy, setNoisy] = useState(null);
  const [recon, setRecon] = useState(null);
  const [chartData, setChart] = useState([]);

  /* fetch 10 sample digits once */
  useEffect(() => {
    axios.get("http://localhost:8000/sample_digits").then(res => {
      setMnist(res.data);
    });
  }, []);

  const datasets = {
    mnist: { label: "MNIST Digits", samples: mnist },
    emoji: { label: "Emojis 😄",    samples: emojis },
  };

  const handleSubmit = async ({ key, noise, model, dataset }) => {
    const image = datasets[dataset].samples[key];
    const payload = { image, noise };

    const { data: nres } = await generateNoise(payload);
    setOrig(image);
    setNoisy(nres.reconstructed);

    let res;
    if (model === "ca")  res = await runCA(payload);
    if (model === "hop") res = await runHop(payload);
    if (model === "ffn") res = await runFFN(payload);

    setRecon(res.data.reconstructed);
    setChart(prev => [
      ...prev.filter(i => i.name !== model.toUpperCase()),
      { name: model.toUpperCase(), accuracy: res.data.accuracy },
    ]);
  };

  return (
    <>
      <Navbar />
      <main className="grid md:grid-cols-[340px_1fr] gap-6 p-6">
        <div className="flex flex-col gap-8">
          <Controls datasets={datasets} onSubmit={handleSubmit} />
          <div className="flex gap-4 justify-center">
            {orig  && <ImageCanvas label="Original"      src={orig}  />}
            {noisy && <ImageCanvas label="Noisy"         src={noisy} />}
            {recon && <ImageCanvas label="Reconstructed" src={recon} />}
          </div>
          {chartData.length > 0 && <AccuracyChart items={chartData} />}
        </div>

        {/* right: scrollable info panel */}
        <section className="overflow-y-auto max-h-[calc(100vh-4rem)] pr-4">
          <h2 className="text-2xl font-bold mb-4">How the models work</h2>
          <h3 className="font-semibold mt-3">Cellular Automata</h3>
          <p className="text-sm leading-relaxed">
            A simple totalistic 2-D rule…
          </p>
          <h3 className="font-semibold mt-3">Hopfield Networks</h3>
          <p className="text-sm leading-relaxed">
            Classic content-addressable memory…
          </p>
          <h3 className="font-semibold mt-3">Feed-Forward Autoencoder</h3>
          <p className="text-sm leading-relaxed">
            Trained to minimise reconstruction loss…
          </p>
          <h3 className="font-semibold mt-4">Project info</h3>
          <p className="text-sm leading-relaxed">
            Built by … University of …, 2025.  Compare robustness of
            bio-inspired memories on MNIST digits and emojis.
          </p>
        </section>
      </main>
    </>
  );
}
