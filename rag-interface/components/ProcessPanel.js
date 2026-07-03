"use client";

import { useState } from "react";
import { processFile } from "@/lib/api";
import { PanelHeader, RequestLine, Field, TextInput, Button, StatusBanner, JsonView } from "./Primitives";

export default function ProcessPanel({ projectId }) {
  const [fileId, setFileId] = useState("");
  const [chunkSize, setChunkSize] = useState(100);
  const [overlapSize, setOverlapSize] = useState(20);
  const [doReset, setDoReset] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handleProcess() {
    if (!projectId) {
      setError("Set a project ID in the sidebar first.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await processFile(projectId, {
        fileId: fileId || undefined,
        chunkSize: Number(chunkSize),
        overlapSize: Number(overlapSize),
        doReset,
      });
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
        eyebrow="Stage 02"
        title="Process into chunks"
        description="Splits an uploaded file into overlapping text chunks ready for embedding. Leave file ID blank to process every file already uploaded to this project."
      />
      <RequestLine method="POST" path={`/api/v1/data/process/${projectId || "{project_id}"}`} />

      <div className="grid max-w-md grid-cols-2 gap-4">
        <div className="col-span-2">
          <Field label="File ID" hint="optional — omit to process all project files">
            <TextInput
              value={fileId}
              onChange={(e) => setFileId(e.target.value)}
              placeholder="e.g. a1b2c3.pdf"
            />
          </Field>
        </div>

        <Field label="Chunk size" hint="characters per chunk">
          <TextInput type="number" value={chunkSize} onChange={(e) => setChunkSize(e.target.value)} />
        </Field>

        <Field label="Overlap size" hint="characters shared between chunks">
          <TextInput type="number" value={overlapSize} onChange={(e) => setOverlapSize(e.target.value)} />
        </Field>

        <div className="col-span-2 flex items-center gap-2 pt-1">
          <input
            id="do-reset-process"
            type="checkbox"
            checked={doReset}
            onChange={(e) => setDoReset(e.target.checked)}
            className="h-4 w-4 accent-[var(--accent)]"
          />
          <label htmlFor="do-reset-process" className="text-sm text-[var(--text-muted)]">
            Reset — delete this project's existing chunks before processing
          </label>
        </div>

        <div className="col-span-2 pt-1">
          <Button onClick={handleProcess} loading={loading}>
            Process file(s)
          </Button>
        </div>
      </div>

      {error && <StatusBanner status="error">{error}</StatusBanner>}
      {result && (
        <StatusBanner status="success">
          {result.signal} — {result.Inserted_chunks} chunks from {result.Processed_files} file(s)
        </StatusBanner>
      )}
      {result && <JsonView data={result} />}
    </div>
  );
}
