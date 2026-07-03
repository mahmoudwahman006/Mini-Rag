"use client";

import { useState } from "react";
import { searchIndex } from "@/lib/api";
import { PanelHeader, RequestLine, Field, TextInput, Button, StatusBanner, JsonView } from "./Primitives";

export default function SearchPanel({ projectId }) {
  const [text, setText] = useState("");
  const [limit, setLimit] = useState(5);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handleSearch() {
    if (!projectId) {
      setError("Set a project ID in the sidebar first.");
      return;
    }
    if (!text.trim()) {
      setError("Enter a query to search for.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await searchIndex(projectId, { text, limit: Number(limit) });
      setResult(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const items = Array.isArray(result) ? result : result?.results;

  return (
    <div>
      <PanelHeader
        eyebrow="Stage 05"
        title="Search the collection"
        description="Embeds the query text and runs a similarity search against this project's vector collection."
      />
      <RequestLine method="POST" path={`/api/v1/nlp/index/search/${projectId || "{project_id}"}`} />

      <div className="grid max-w-md grid-cols-3 gap-4">
        <div className="col-span-2">
          <Field label="Query text">
            <TextInput value={text} onChange={(e) => setText(e.target.value)} placeholder="What does the file say about…" />
          </Field>
        </div>
        <Field label="Limit">
          <TextInput type="number" value={limit} onChange={(e) => setLimit(e.target.value)} />
        </Field>
        <div className="col-span-3 pt-1">
          <Button onClick={handleSearch} loading={loading}>
            Search
          </Button>
        </div>
      </div>

      {error && <StatusBanner status="error">{error}</StatusBanner>}

      {items && Array.isArray(items) && (
        <ul className="mt-4 flex flex-col gap-2">
          {items.map((item, i) => (
            <li key={i} className="rounded-md border border-[var(--border)] bg-[var(--panel-raised)] p-3">
              <div className="font-[family-name:var(--font-mono)] text-[10px] uppercase tracking-[0.1em] text-[var(--text-muted)]">
                score: {item.score ?? item.similarity ?? "—"}
              </div>
              <div className="mt-1 text-sm text-[var(--text)]">{item.text ?? item.chunk_text ?? JSON.stringify(item)}</div>
            </li>
          ))}
        </ul>
      )}

      {result && !items && <JsonView data={result} />}
    </div>
  );
}
