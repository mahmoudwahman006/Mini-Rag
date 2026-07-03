"use client";

import { useState } from "react";
import { pushIndex } from "@/lib/api";
import { PanelHeader, RequestLine, Button, StatusBanner, JsonView } from "./Primitives";

export default function IndexPushPanel({ projectId }) {
  const [doReset, setDoReset] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handlePush() {
    if (!projectId) {
      setError("Set a project ID in the sidebar first.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await pushIndex(projectId, { doReset });
      setResult(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <PanelHeader
        eyebrow="Stage 03"
        title="Embed and push to the vector store"
        description="Reads this project's chunks in pages, embeds each page with Cohere, and pushes the vectors into the collection."
      />
      <RequestLine method="POST" path={`/api/v1/nlp/index/push/${projectId || "{project_id}"}`} />

      <div className="max-w-md">
        <div className="flex items-center gap-2">
          <input
            id="do-reset-push"
            type="checkbox"
            checked={doReset}
            onChange={(e) => setDoReset(e.target.checked)}
            className="h-4 w-4 accent-[var(--accent)]"
          />
          <label htmlFor="do-reset-push" className="text-sm text-[var(--text-muted)]">
            Reset — recreate the collection before indexing
          </label>
        </div>

        <div className="pt-4">
          <Button onClick={handlePush} loading={loading}>
            Push to vector store
          </Button>
        </div>
      </div>

      {error && <StatusBanner status="error">{error}</StatusBanner>}
      {result && (
        <StatusBanner status="success">
          {result.Signal} — {result.InsertedRecordsCount} records inserted
        </StatusBanner>
      )}
      {result && <JsonView data={result} />}
    </div>
  );
}
