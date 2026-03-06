export default function RouteResult({ result }) {
  const { path, duration, stops } = result;

  return (
    <div className="w-full max-w-xl mt-6">
      {/* Stats */}
      <div className="grid grid-cols-3 gap-3 mb-5">
        {[
          { label: "Travel Time", value: `${duration} min` },
          { label: "Stops", value: stops },
          { label: "Stations", value: path.length },
        ].map(({ label, value }) => (
          <div
            key={label}
            className="bg-slate-800 border border-slate-700 rounded-xl p-4 text-center"
          >
            <p className="text-2xl font-bold text-indigo-400">{value}</p>
            <p className="text-xs text-slate-400 mt-1">{label}</p>
          </div>
        ))}
      </div>

      {/* Path Timeline */}
      <div className="bg-slate-800 border border-slate-700 rounded-2xl p-5">
        <h2 className="text-sm font-semibold text-slate-300 mb-4 uppercase tracking-wider">
          Route
        </h2>
        <div className="relative">
          {path.map((station, i) => (
            <div key={station} className="flex items-start gap-3 mb-3 last:mb-0">
              {/* Timeline dot + line */}
              <div className="flex flex-col items-center pt-1">
                <div
                  className={`w-3 h-3 rounded-full flex-shrink-0 ${
                    i === 0
                      ? "bg-green-400"
                      : i === path.length - 1
                      ? "bg-red-400"
                      : "bg-indigo-500"
                  }`}
                />
                {i < path.length - 1 && (
                  <div className="w-0.5 h-6 bg-slate-600 mt-1" />
                )}
              </div>
              {/* Station name */}
              <div>
                <p
                  className={`text-sm font-medium ${
                    i === 0 || i === path.length - 1
                      ? "text-white"
                      : "text-slate-300"
                  }`}
                >
                  {station}
                </p>
                {i === 0 && (
                  <span className="text-xs text-green-400">Start</span>
                )}
                {i === path.length - 1 && (
                  <span className="text-xs text-red-400">End</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
