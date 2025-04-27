export default function ImageCanvas({ label, src }) {
    return (
      <div className="flex flex-col items-center">
        <span className="text-sm mb-1">{label}</span>
        <img className="border rounded-xl w-40 h-40" src={src} alt={label} />
      </div>
    );
  }