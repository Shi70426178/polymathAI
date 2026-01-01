const API_BASE =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "http://3.93.39.191:8000";

export async function uploadVideo(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload/video`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}

export async function extractAudio(videoId) {
  const res = await fetch(
    `${API_BASE}/process/extract-audio/${videoId}`,
    { method: "POST" }
  );

  if (!res.ok) throw new Error("Audio extraction failed");
  return res.json();
}

export async function generateContent(videoId) {
  const res = await fetch(
    `${API_BASE}/process/generate-content/${videoId}`,
    { method: "POST" }
  );

  if (!res.ok) throw new Error("Content generation failed");
  return res.json();
}
