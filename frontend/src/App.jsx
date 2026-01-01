import { useState } from "react";
import Navbar from "./components/Navbar";
import UploadCard from "./components/UploadCard";
import ResultCard from "./components/ResultCard";

const API_BASE =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "http://3.93.39.191:8000";

function App() {
  const [content, setContent] = useState(null);

  async function handleGenerate(file, category) {
  try {
    setContent(null);

    // 1️⃣ Upload video
    const formData = new FormData();
    formData.append("file", file);

    const uploadRes = await fetch(`${API_BASE}/upload/video`, {
      method: "POST",
      body: formData,
    });

    if (!uploadRes.ok) throw new Error("Upload failed");

    const uploadData = await uploadRes.json();
    const videoId = uploadData.video_id;

    // 2️⃣ Extract audio
    await fetch(`${API_BASE}/process/extract-audio/${videoId}`, {
      method: "POST",
    });

    // 3️⃣ Transcribe
    await fetch(`${API_BASE}/process/transcribe/${videoId}`, {
      method: "POST",
    });

    // 4️⃣ Generate content (CATEGORY INCLUDED)
    const genRes = await fetch(
      `${API_BASE}/process/generate-content/${videoId}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category }),
      }
    );

    if (!genRes.ok) throw new Error("Generation failed");

    const data = await genRes.json();
    setContent(data.content);

  } catch (err) {
    console.error(err);
    alert("Backend error — check server logs");
  }
}


  return (
    <>
      <Navbar />

      <main className="container">
        <section className="hero">
          <h1>Turn your videos into smart captions & hashtags</h1>
          <p>
            PolymathAI understands your video content and writes titles,
            descriptions, and hashtags — intelligently.
          </p>
        </section>

        <UploadCard onGenerate={handleGenerate} />
        <ResultCard content={content} />
      </main>

      <footer className="footer">
        Built for creators · PolymathAI
      </footer>
    </>
  );
}

export default App;
