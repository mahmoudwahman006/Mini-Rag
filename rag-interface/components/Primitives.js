"use client";

// The mono "request line" reinforces that each panel maps to one
// real HTTP call — this is a technical console, not a form builder.
export function RequestLine({ method, path }) {
  const methodColor = method === "GET" ? "text-[var(--accent)]" : "text-[var(--warning)]";
  return (
    <div className="mb-6 flex items-center gap-2 rounded-md border border-[var(--border)] bg-[var(--panel-raised)] px-3 py-2 font-[family-name:var(--font-mono)] text-xs">
      <span className={`font-medium ${methodColor}`}>{method}</span>
      <span className="text-[var(--text-muted)]">{path}</span>
    </div>
  );
}

export function PanelHeader({ eyebrow, title, description }) {
  return (
    <div className="mb-6">
      <div className="font-[family-name:var(--font-mono)] text-[11px] uppercase tracking-[0.14em] text-[var(--accent)]">
        {eyebrow}
      </div>
      <h1 className="mt-1 text-xl font-medium text-[var(--text)]">{title}</h1>
      {description && <p className="mt-1.5 max-w-xl text-sm text-[var(--text-muted)]">{description}</p>}
    </div>
  );
}

export function Field({ label, hint, children }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="font-[family-name:var(--font-mono)] text-[10px] uppercase tracking-[0.12em] text-[var(--text-muted)]">
        {label}
      </label>
      {children}
      {hint && <span className="text-xs text-[var(--text-muted)]">{hint}</span>}
    </div>
  );
}

export function TextInput(props) {
  return (
    <input
      {...props}
      className="w-full rounded-md border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--text)] placeholder:text-[var(--text-muted)] focus:border-[var(--accent)]"
    />
  );
}

export function Button({ children, loading, variant = "primary", ...props }) {
  const base = "rounded-md px-4 py-2 text-sm font-medium transition-colors disabled:opacity-50";
  const styles =
    variant === "primary"
      ? "bg-[var(--accent)] text-[var(--bg)] hover:bg-[var(--accent-dim)]"
      : "border border-[var(--border)] text-[var(--text)] hover:bg-[var(--panel-raised)]";
  return (
    <button {...props} disabled={props.disabled || loading} className={`${base} ${styles}`}>
      {loading ? "Working…" : children}
    </button>
  );
}

// Errors and empty states speak in the interface's voice: what happened,
// what to do about it. No apologies, no vagueness.
export function StatusBanner({ status, children }) {
  if (!status) return null;
  const styles = {
    success: "border-[var(--accent)]/40 bg-[var(--accent)]/10 text-[var(--accent)]",
    error: "border-[var(--error)]/40 bg-[var(--error)]/10 text-[var(--error)]",
    info: "border-[var(--border)] bg-[var(--panel-raised)] text-[var(--text-muted)]",
  };
  return (
    <div className={`mt-4 rounded-md border px-3 py-2.5 font-[family-name:var(--font-mono)] text-xs ${styles[status]}`}>
      {children}
    </div>
  );
}

export function JsonView({ data }) {
  return (
    <pre className="mt-4 max-h-96 overflow-auto rounded-md border border-[var(--border)] bg-[var(--bg)] p-3 font-[family-name:var(--font-mono)] text-xs text-[var(--text)]">
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}
