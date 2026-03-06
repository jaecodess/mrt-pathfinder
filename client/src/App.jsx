import { useState, useEffect } from "react";
import StationSelect from "./components/StationSelect";
import RouteResult from "./components/RouteResult";
import AnimatedPath from "./components/AnimatedPath";

export default function App() {
  const [stations, setStations] = useState([]);
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/stations")
      .then((r) => r.json())
      .then(setStations);
  }, []);

  const findRoute = async () => {
    if (!start || !end) return setError("Please select both stations.");
    setError("");
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch("/api/route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ start, end }),
      });
      const data = await res.json();
      if (data.error) setError(data.error);
      else setResult(data);
    } catch {
      setError("Server error. Make sure Flask is running.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex flex-col items-center px-4 py-10">
      {/* Header */}
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold text-white tracking-tight">
          🚇 Singapore MRT Pathfinder
        </h1>
        <p className="mt-2 text-slate-400 text-sm">
          Powered by Dijkstra's Algorithm — finds the fastest route by travel time
        </p>
      </div>

      {/* Input Card */}
      <div className="w-full max-w-xl bg-slate-800 rounded-2xl p-6 shadow-xl border border-slate-700">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <StationSelect
            label="From"
            value={start}
            onChange={setStart}
            stations={stations}
            exclude={end}
          />
          <StationSelect
            label="To"
            value={end}
            onChange={setEnd}
            stations={stations}
            exclude={start}
          />
        </div>

        {error && (
          <p className="mt-3 text-red-400 text-sm text-center">{error}</p>
        )}

        <button
          onClick={findRoute}
          disabled={loading}
          className="mt-5 w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500
                     disabled:opacity-50 font-semibold text-white transition-all
                     active:scale-95 text-sm tracking-wide"
        >
          {loading ? "Calculating…" : "Find Shortest Route"}
        </button>
      </div>

      {/* Result */}
      {result && (
        <>
          <RouteResult result={result} />
          <AnimatedPath visited={result.visited} path={result.path} />
        </>
      )}

      <p className="mt-10 text-slate-600 text-xs">
        Travel times are approximate. Based on Singapore MRT network data.
      </p>
    </div>
  );
}
