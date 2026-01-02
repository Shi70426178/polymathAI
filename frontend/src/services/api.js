const API_BASE =
  import.meta.env.VITE_API_BASE ||
  (window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "http://3.93.39.191:8000");

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
  const res = await fetch(`${API_BASE}/process/extract-audio/${videoId}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Audio extraction failed");
}

export async function transcribe(videoId) {
  const res = await fetch(`${API_BASE}/process/transcribe/${videoId}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Transcription failed");
}

export async function generateContent(videoId, category) {
  const res = await fetch(
    `${API_BASE}/process/generate-content/${videoId}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ category }),
    }
  );

  if (!res.ok) throw new Error("Content generation failed");
  return res.json();
}
