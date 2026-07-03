"use client";

const STAGES = [
  { id: "upload", index: "01", label: "Upload", hint: "txt / pdf" },
  { id: "process", index: "02", label: "Process", hint: "chunking" },
  { id: "push", index: "03", label: "Index", hint: "embed + push" },
  { id: "info", index: "04", label: "Info", hint: "collection" },
  { id: "search", index: "05", label: "Search", hint: "query" },
];

export default function Sidebar({ active, onSelect, projectId, onProjectIdChange }) {
  return (
    <aside className="flex h-full w-64 shrink-0 flex-col border-r border-[var(--border)] bg-[var(--panel)]">
      <div className="px-5 pt-6 pb-4">
        <div className="font-[family-name:var(--font-mono)] text-[11px] uppercase tracking-[0.18em] text-[var(--text-muted)]">
          RAG Pipeline
        </div>
        <div className="mt-0.5 text-base font-medium">Console</div>
      </div>

      <div className="px-5 pb-4">
        <label className="block font-[family-name:var(--font-mono)] text-[10px] uppercase tracking-[0.14em] text-[var(--text-muted)]">
          Project ID
        </label>
        <input
          value={projectId}
          onChange={(e) => onProjectIdChange(e.target.value)}
          placeholder="e.g. proj_01"
          className="mt-1.5 w-full rounded-md border border-[var(--border)] bg-[var(--bg)] px-2.5 py-1.5 font-[family-name:var(--font-mono)] text-sm text-[var(--text)] placeholder:text-[var(--text-muted)] focus:border-[var(--accent)]"
        />
      </div>

      {/* Pipeline rail: the vertical connector is the through-line of the
          actual data flow (upload -> process -> index -> info -> search) */}
      <nav className="relative flex-1 px-3 pt-2">
        <div className="absolute left-[27px] top-3 bottom-3 w-px bg-[var(--border)]" aria-hidden="true" />
        <ul className="relative flex flex-col gap-1">
          {STAGES.map((stage) => {
            const isActive = active === stage.id;
            return (
              <li key={stage.id}>
                <button
                  onClick={() => onSelect(stage.id)}
                  className={`group relative flex w-full items-center gap-3 rounded-md px-2 py-2.5 text-left transition-colors ${
                    isActive ? "bg-[var(--panel-raised)]" : "hover:bg-[var(--panel-raised)]/60"
                  }`}
                >
                  <span
                    className={`relative z-10 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border font-[family-name:var(--font-mono)] text-[10px] ${
                      isActive
                        ? "border-[var(--accent)] bg-[var(--accent)] text-[var(--bg)]"
                        : "border-[var(--border)] bg-[var(--panel)] text-[var(--text-muted)]"
                    }`}
                  >
                    {stage.index}
                  </span>
                  <span className="flex flex-col">
                    <span className={`text-sm ${isActive ? "text-[var(--text)]" : "text-[var(--text-muted)]"}`}>
                      {stage.label}
                    </span>
                    <span className="font-[family-name:var(--font-mono)] text-[10px] text-[var(--text-muted)]">
                      {stage.hint}
                    </span>
                  </span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="border-t border-[var(--border)] px-5 py-4 font-[family-name:var(--font-mono)] text-[10px] text-[var(--text-muted)]">
        API_BASE: {process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000"}
      </div>
    </aside>
  );
}
