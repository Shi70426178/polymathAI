import { useState, useRef } from "react";
import Navbar from "./components/Navbar";
import UploadCard from "./components/UploadCard";
import ResultCard from "./components/ResultCard";
import { useEffect } from "react";
import { pageview } from "./utils/analytics";

import {
  uploadVideo,
  startProcess,
  getStatus,
  getResult,
} from "./services/api";

function App() {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");


  useEffect(() => {
  pageview(window.location.pathname);
}, []);

  // prevents multiple polling intervals
  const pollRef = useRef(null);

  async function handleGenerate(file, category) {
    if (loading) return;

    try {
      setLoading(true);
      setContent(null);
      setStatus("📤 Uploading your video…");

      // 1️⃣ Upload video
      const uploadData = await uploadVideo(file);
      const videoId = uploadData.video_id;

      // 2️⃣ Start background processing
      setStatus("⚙️ Processing video (this may take a minute)…");
      await startProcess(videoId);

      // clear any previous poll
      if (pollRef.current) {
        clearInterval(pollRef.current);
      }

      // 3️⃣ Poll status
      pollRef.current = setInterval(async () => {
        const data = await getStatus(videoId);

        if (data.status === "unknown") {
          setStatus("⏳ Initializing processing…");
          return;
        }

        if (data.status === "completed") {
          clearInterval(pollRef.current);
          pollRef.current = null;

          // 4️⃣ Fetch final result
          const result = await getResult(videoId);
          setContent(result);
          setStatus("✅ Done");
          setLoading(false);
        }

        if (data.status === "failed") {
          clearInterval(pollRef.current);
          pollRef.current = null;

          setStatus("❌ Processing failed");
          setLoading(false);
        }
      }, 3000);

    } catch (err) {
      console.error(err);
      setStatus("❌ Something went wrong. Please try again.");
      setLoading(false);

      if (pollRef.current) {
        clearInterval(pollRef.current);
        pollRef.current = null;
      }
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

        <UploadCard onGenerate={handleGenerate} loading={loading} />

        {loading && (
          <div className="processing-box">
            <div className="spinner" />
            <p className="muted">{status}</p>
          </div>
        )}

        <ResultCard content={content} />
      </main>

      <footer className="footer">
        Built for creators · PolymathAI
      </footer>
    </>
  );
}

export default App;
