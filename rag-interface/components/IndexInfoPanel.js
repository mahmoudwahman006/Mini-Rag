"use client";

import { useState } from "react";
import { getIndexInfo } from "@/lib/api";
import { PanelHeader, RequestLine, Button, StatusBanner, JsonView } from "./Primitives";

export default function IndexInfoPanel({ projectId }) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handleFetch() {
    if (!projectId) {
      setError("Set a project ID in the sidebar first.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await getIndexInfo(projectId);
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
        eyebrow="Stage 04"
        title="Collection info"
        description="Reads the current state of this project's vector collection — vector count, config, and status."
      />
      <RequestLine method="GET" path={`/api/v1/nlp/index/info/${projectId || "{project_id}"}`} />

      <Button onClick={handleFetch} loading={loading}>
        Fetch collection info
      </Button>

      {error && <StatusBanner status="error">{error}</StatusBanner>}
      {result && <StatusBanner status="success">{result.Signal}</StatusBanner>}
      {result && <JsonView data={result.collection_info ?? result} />}
    </div>
  );
}
