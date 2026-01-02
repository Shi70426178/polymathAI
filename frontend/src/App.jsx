import { useState } from "react";
import Navbar from "./components/Navbar";
import UploadCard from "./components/UploadCard";
import ResultCard from "./components/ResultCard";
import {
  uploadVideo,
  extractAudio,
  transcribe,
  generateContent,
} from "./services/api";

function App() {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleGenerate(file, category) {
    if (loading) return;

    try {
      setLoading(true);
      setContent(null);

      const uploadData = await uploadVideo(file);
      const videoId = uploadData.video_id;

      await extractAudio(videoId);
      await transcribe(videoId);

      const result = await generateContent(videoId, category);
      setContent(result.content);
    } catch (err) {
      console.error(err);
      alert("Something went wrong. Check server logs.");
    } finally {
      setLoading(false);
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

        <ResultCard content={content} />
      </main>

      <footer className="footer">
        Built for creators · PolymathAI
      </footer>
    </>
  );
}

export default App;
