// lib/api.js
// Thin wrapper around the 5 RAG backend endpoints.
// Base URL comes from env so it can point at localhost during dev
// and at a real host in production.

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

async function handleResponse(res) {
  let body;
  try {
    body = await res.json();
  } catch {
    body = null;
  }
  if (!res.ok) {
    const message = body?.signal || body?.Signal || `Request failed with status ${res.status}`;
    const err = new Error(message);
    err.status = res.status;
    err.body = body;
    throw err;
  }
  return body;
}

// 1) Upload file (txt or pdf) for a project
// POST /api/v1/data/upload/{project_id}   multipart/form-data, field name: "file"
export async function uploadFile(projectId, file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/api/v1/data/upload/${encodeURIComponent(projectId)}`, {
    method: "POST",
    body: formData,
  });
  return handleResponse(res);
}

// 2) Process (chunk) a previously uploaded file
// POST /api/v1/data/process/{project_id}
// body: { file_id?: string, chunk_size: number, overlap_size: number, do_reset: 0 | 1 }
export async function processFile(projectId, { fileId, chunkSize, overlapSize, doReset }) {
  const res = await fetch(`${BASE_URL}/api/v1/data/process/${encodeURIComponent(projectId)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      file_id: fileId || undefined,
      chunk_size: chunkSize,
      overlap_size: overlapSize,
      do_reset: doReset ? 1 : 0,
    }),
  });
  return handleResponse(res);
}

// 3) Push processed chunks into the vector DB (embedding + indexing)
// POST /api/v1/nlp/index/push/{project_id}
// body: { do_reset: 0 | 1 }
export async function pushIndex(projectId, { doReset }) {
  const res = await fetch(`${BASE_URL}/api/v1/nlp/index/push/${encodeURIComponent(projectId)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ do_reset: doReset ? 1 : 0 }),
  });
  return handleResponse(res);
}

// 4) Get vector DB collection info for a project
// GET /api/v1/nlp/index/info/{project_id}
export async function getIndexInfo(projectId) {
  const res = await fetch(`${BASE_URL}/api/v1/nlp/index/info/${encodeURIComponent(projectId)}`, {
    method: "GET",
  });
  return handleResponse(res);
}

// 5) Semantic search over a project's collection
// POST /api/v1/nlp/index/search/{project_id}
// body: { text: string, limit: number }
export async function searchIndex(projectId, { text, limit }) {
  const res = await fetch(`${BASE_URL}/api/v1/nlp/index/search/${encodeURIComponent(projectId)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, limit }),
  });
  return handleResponse(res);
}
