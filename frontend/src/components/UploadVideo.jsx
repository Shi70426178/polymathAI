import { useState } from "react";

const API_BASE =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "http://100.48.225.236:8000";

const CATEGORIES = [
  "vlog",
  "lifestyle",
  "comedy",
  "motivation",
  "gaming",
  "education",
  "podcast",
  "tech",
];

export default function UploadVideo() {
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState("vlog");
  const [status, setStatus] = useState("");
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(false);

  async function uploadVideo() {
    if (!file) {
      setStatus("Please select a video");
      return null;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_BASE}/upload/video`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      setStatus("Upload failed");
      return null;
    }

    const data = await res.json();
    return data.video_id;
  }

  async function runFullPipeline() {
    if (loading) return;

    try {
      setLoading(true);
      setContent(null);
      setStatus("Starting pipeline...");

      const videoId = await uploadVideo();
      if (!videoId) return;

      setStatus("Extracting audio...");
      await fetch(`${API_BASE}/process/extract-audio/${videoId}`, {
        method: "POST",
      });

      setStatus("Transcribing...");
      await fetch(`${API_BASE}/process/transcribe/${videoId}`, {
        method: "POST",
      });

      setStatus("Generating AI content...");
      const res = await fetch(
        `${API_BASE}/process/generate-content/${videoId}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ category }),
        }
      );

      const data = await res.json();
      setContent(data.content);
      setStatus("All done ✅");
    } catch (e) {
      console.error(e);
      setStatus("Something went wrong ❌");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <input
        type="file"
        accept="video/*"
        disabled={loading}
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <label>
        Category:&nbsp;
        <select
          value={category}
          disabled={loading}
          onChange={(e) => setCategory(e.target.value)}
        >
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>
              {c.charAt(0).toUpperCase() + c.slice(1)}
            </option>
          ))}
        </select>
      </label>

      <br /><br />

      <button onClick={runFullPipeline} disabled={loading}>
        {loading ? "Processing..." : "🚀 Run Full Pipeline"}
      </button>

      <p>{status}</p>

      {content && (
        <div style={{ marginTop: 20 }}>
          <h3>{content.title}</h3>
          <p>{content.description}</p>
          <p>{content.hashtags.join(" ")}</p>
        </div>
      )}
    </div>
  );
}
