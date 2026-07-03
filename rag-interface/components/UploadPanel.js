"use client";

import { useState } from "react";
import { uploadFile } from "@/lib/api";
import { PanelHeader, RequestLine, Field, Button, StatusBanner, JsonView } from "./Primitives";

export default function UploadPanel({ projectId }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handleUpload() {
    if (!projectId) {
      setError("Set a project ID in the sidebar first.");
      return;
    }
    if (!file) {
      setError("Choose a .txt or .pdf file to upload.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await uploadFile(projectId, file);
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
        eyebrow="Stage 01"
        title="Upload a document"
        description="Sends the file to the project's asset store. Accepts .txt and .pdf, validated server-side against size and extension limits."
      />
      <RequestLine method="POST" path={`/api/v1/data/upload/${projectId || "{project_id}"}`} />

      <div className="flex flex-col gap-4 max-w-md">
        <Field label="File" hint="txt or pdf, size limit enforced by the server">
          <input
            type="file"
            accept=".txt,.pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="w-full rounded-md border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--text)] file:mr-3 file:rounded file:border-0 file:bg-[var(--panel-raised)] file:px-3 file:py-1.5 file:text-[var(--text)]"
          />
        </Field>

        <Button onClick={handleUpload} loading={loading} className="self-start">
          Upload file
        </Button>
      </div>

      {error && <StatusBanner status="error">{error}</StatusBanner>}
      {result && (
        <StatusBanner status="success">
          {result.signal} — file_id: {result.file_id}
        </StatusBanner>
      )}
      {result && <JsonView data={result} />}
    </div>
  );
}
