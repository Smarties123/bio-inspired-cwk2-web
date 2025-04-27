import brain from "../assets/brain.png";   // add any placeholder svg/png

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 flex items-center gap-4 px-6 py-3 bg-white/80 backdrop-blur shadow">
      <img src={brain} alt="brain-logo" className="w-8 h-8" />
      <h1 className="text-xl font-bold tracking-wide">
        Bio-Inspired Pattern Memory Lab
      </h1>
    </nav>
  );
}
