export default function StationSelect({ label, value, onChange, stations, exclude }) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-xs text-slate-400 font-medium uppercase tracking-wider">
        {label}
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="bg-slate-700 border border-slate-600 text-white rounded-lg px-3 py-2
                   text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
      >
        <option value="">Select station…</option>
        {stations
          .filter((s) => s !== exclude)
          .map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
      </select>
    </div>
  );
}
