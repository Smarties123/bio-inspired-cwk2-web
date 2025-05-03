import axios from "axios";
// const api = axios.create({ baseURL: "http://localhost:8000" });
const api = axios.create({
      baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});
export const generateNoise = (payload) => api.post("/generate_noise", payload);
export const runCA  = (payload) => api.post("/run_ca", payload);
export const runHop = (payload) => api.post("/run_hopfield", payload);
export const runFFN = (payload) => api.post("/run_ffn", payload);