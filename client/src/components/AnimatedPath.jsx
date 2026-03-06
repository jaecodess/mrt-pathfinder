import { useEffect, useState } from "react";

export default function AnimatedPath({ visited, path }) {
  const [shown, setShown] = useState([]);
  const [phase, setPhase] = useState("exploring"); // "exploring" | "done"

  useEffect(() => {
    setShown([]);
    setPhase("exploring");
    let i = 0;
    const pathSet = new Set(path);

    const interval = setInterval(() => {
      if (i < visited.length) {
        setShown((prev) => [...prev, visited[i]]);
        i++;
      } else {
        clearInterval(interval);
        setPhase("done");
      }
    }, 60);

    return () => clearInterval(interval);
  }, [visited, path]);

  const pathSet = new Set(path);

  return (
    <div className="w-full max-w-xl mt-5 bg-slate-800 border border-slate-700 rounded-2xl p-5">
      <h2 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wider">
        Algorithm Visualization
      </h2>
      <p className="text-xs text-slate-500 mb-4">
        {phase === "exploring"
          ? `🔍 Exploring nodes… (${shown.length} / ${visited.length})`
          : `✅ Done! Explored ${visited.length} stations to find your ${path.length}-stop route.`}
      </p>
      <div className="flex flex-wrap gap-2">
        {shown.map((s) => (
          <span
            key={s}
            className={`px-2 py-1 rounded-lg text-xs font-medium transition-all ${
              pathSet.has(s)
                ? "bg-indigo-600 text-white"
                : "bg-slate-700 text-slate-400"
            }`}
          >
            {s}
          </span>
        ))}
      </div>
    </div>
  );
}
