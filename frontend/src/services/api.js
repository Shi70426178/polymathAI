const API_BASE =
  import.meta.env.VITE_API_BASE ||
  (window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "/api");

// ======================
// Upload
// ======================
export async function uploadVideo(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload/video`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Upload failed");
  }

  return res.json();
}

// ======================
// Start background processing
// ======================
export async function startProcess(videoId) {
  const res = await fetch(`${API_BASE}/process/start/${videoId}`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to start processing");
  }
}

// ======================
// Poll status
// ======================
export async function getStatus(videoId) {
  const res = await fetch(`${API_BASE}/process/status/${videoId}`);

  if (!res.ok) {
    throw new Error("Failed to get status");
  }

  return res.json();
}

// ======================
// Fetch final result
// ======================
export async function getResult(videoId) {
  const res = await fetch(`${API_BASE}/process/result/${videoId}`);

  if (!res.ok) {
    throw new Error("Result not ready");
  }

  return res.json();
}
