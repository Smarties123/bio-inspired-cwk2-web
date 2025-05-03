import { useEffect, useState } from "react";
import axios from "axios";

import Navbar        from "./components/Navbar";
import Controls      from "./components/Controls";
import ImageCanvas   from "./components/ImageCanvas";
import AccuracyChart from "./components/AccuracyChart";

const api = axios.create({ baseURL:"http://localhost:8000" });
const calls = {
  ca:       payload => api.post("/run_ca", payload),
  hopfield: payload => api.post("/run_hopfield", payload),
  som:      payload => api.post("/run_som", payload),
  hybrid:   payload => api.post("/run_hybrid", payload),
};

export default function App() {
  const [mnist,setMnist] = useState({});
  const [orig,setOrig]   = useState(null);
  const [noisy,setNoisy] = useState(null);
  const [recon,setRecon] = useState(null);
  const [chart,setChart] = useState([]);

  useEffect(()=>{
    axios.get("http://localhost:8000/sample_digits")
      .then(res=>setMnist(res.data));
  },[]);

  const datasets = {
    mnist: { label:"MNIST", samples: mnist },
    // emoji: { label:"Emojis 😊", samples: emojis },
  };

  const handle = async ({ key, noise, model, dataset }) => {
    const image = datasets[dataset].samples[key];
    // 1) Make noisy
    const { data: noiseRes } = await api.post("/generate_noise", { image, noise });
    setOrig(image);
    setNoisy(noiseRes.reconstructed);
  
    let res;
    if (model === "hopfield" || model === "som") {
      // these endpoints expect { init, noisy }
      res = await api.post(
        model === "hopfield" ? "/run_hopfield" : "/run_som",
        { init: image, noisy: noiseRes.reconstructed }
      );
    } else {
      // ca and hybrid still take { image, noise }
      res = await calls[model]({ image, noise });
    }
  
    setRecon(res.data.reconstructed);
    setChart(prev => [
      ...prev.filter(i => i.name !== model.toUpperCase()),
      { name: model.toUpperCase(), accuracy: res.data.accuracy }
    ]);
  };
  
  return (
    <>
      <Navbar />
      <main className="grid md:grid-cols-[340px_1fr] gap-6 p-6">
        <div className="flex flex-col gap-8">
          <Controls datasets={datasets} onSubmit={handle} />
          <div className="flex gap-4 justify-center">
            {orig  && <ImageCanvas label="Original"      src={orig} />}
            {noisy && <ImageCanvas label="Noisy"         src={noisy} />}
            {recon && <ImageCanvas label="Reconstructed" src={recon} />}
          </div>
          {chart.length>0 && <AccuracyChart items={chart} />}
        </div>


        {/* right: scrollable info panel */}
        <section className="overflow-y-auto max-h-[calc(100vh-4rem)] pr-4">
          <h2 className="text-2xl font-bold mb-4">How the models work</h2>

          <h3 className="font-semibold mt-3">Cellular Automata (CA)</h3>
          <p className="text-sm leading-relaxed">
            Each pixel in the image is treated as a cell on a 2D grid that updates
            in parallel according to a local rule. We use a weighted‐majority rule
            (CA-W) with a centre–surround kernel that mimics retinal receptive fields.
            At each time step, a cell computes the weighted sum of itself and its
            eight neighbours; if the sum exceeds a threshold, the cell turns “on”,
            otherwise “off.” This simple local voting rapidly removes isolated
            noise spikes while preserving fine strokes.
          </p>

          <h3 className="font-semibold mt-3">Hopfield Networks</h3>
          <p className="text-sm leading-relaxed">
            We implement a modern Hopfield–PI (pseudo-inverse) network as a
            content-addressable memory. The pseudo-inverse learning rule
            decorrelates stored patterns, yielding well-separated attractor basins.
            During recall, a noisy input vector is iteratively updated to descend
            the energy landscape and converge on the nearest stored pattern
            in just a few asynchronous steps.
          </p>

          <h3 className="font-semibold mt-3">Self-Organising Maps (SOM)</h3>
          <p className="text-sm leading-relaxed">
            A 2D lattice of prototype vectors is trained on the clean dataset. At
            recall time, instead of choosing only the single best‐matching unit,
            we average the K=5 nearest prototypes (SOM-KNN) to soften
            quantisation artefacts. This neighbourhood‐aware retrieval preserves
            more detail and improves robustness under noise.
          </p>

          <h3 className="font-semibold mt-3">Hybrid Localised Attractor Maps (LAM)</h3>
          <p className="text-sm leading-relaxed">
            The Hybrid2 model combines global and local repair in three passes:
            first a Hopfield-PI attractor step to stabilise coarse structure, then
            a weighted‐majority CA pass to fix local anomalies, and finally a
            second Hopfield-PI refinement. This alternating sequence leverages
            both distributed attractor dynamics and local self‐organisation to
            maximise recall accuracy under high noise levels.
          </p>

          <h3 className="font-semibold mt-4">Project info</h3>
          <p className="text-sm leading-relaxed">
            Built by Angelica P and Hemant S under the supervision of Professor Netta Cohen, University of Leeds, 2025.
            We compare the robustness of these bio-inspired memories on MNIST digits and 
            further models exploring larger colourful images can be found in the Github Repository.
          </p>
        </section>
      </main>
    </>
  );
}
