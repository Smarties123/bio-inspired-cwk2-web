export default function ImageCanvas({ label, src }) {
    return (
      <div className="flex flex-col items-center">
        <span className="text-sm mb-1">{label}</span>
        <img className="border rounded-xl w-32 h-32" src={src} alt={label} />
      </div>
    );
  }