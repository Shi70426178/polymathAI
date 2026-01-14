import { useState, useRef } from "react";
import Navbar from "./components/Navbar";
import UploadCard from "./components/UploadCard";
import ResultCard from "./components/ResultCard";
import { useEffect } from "react";
import { pageview } from "./utils/analytics";
import AuthModal from "./components/AuthModal";
import LoginForm from "./components/LoginForm";
import SignupForm from "./components/SignupForm";
import { getUserFromToken, logout } from "./utils/auth";
import PricingModal from "./components/PricingModal";


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

  const [pricingOpen, setPricingOpen] = useState(false);

  const [user, setUser] = useState(getUserFromToken());

  const [authOpen, setAuthOpen] = useState(false);
  const [authMode, setAuthMode] = useState("login"); // or "signup"


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

    let uploadData;

    // 🔒 Upload + daily limit handling
    try {
      uploadData = await uploadVideo(file);
    } catch (err) {
      if (err.code === "DAILY_LIMIT_REACHED") {
        setStatus(
          "🚫 Free limit reached for today. Come back tomorrow or upgrade to Premium."
        );
      } else {
        setStatus("❌ Upload failed. Please try again.");
      }

      setLoading(false);
      return; // ⛔ stop pipeline
    }

    const videoId = uploadData.video_id;

    // 2️⃣ Start background processing
    setStatus("⚙️ Processing video (this may take a minute)…");
    await startProcess(videoId);

    // clear any previous poll
    if (pollRef.current) {
      clearInterval(pollRef.current);
    }

    // 3️⃣ Poll processing status
    pollRef.current = setInterval(async () => {
      const data = await getStatus(videoId);

      if (data.status === "unknown") {
        setStatus("⏳ Initializing processing…");
        return;
      }

      if (data.status === "completed") {
        clearInterval(pollRef.current);
        pollRef.current = null;

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

  function handleLogout() {
  logout();
  setUser(null);
}

  return (
    <>
   <Navbar
  user={user}
  onLogin={() => {
    setAuthMode("login");
    setAuthOpen(true);
  }}
  onSignup={() => {
    setAuthMode("signup");
    setAuthOpen(true);
  }}
  onLogout={handleLogout}
  onPricing={() => setPricingOpen(true)}
/>





      <main className="container">
        <section className="hero">
          <h1>Turn your videos into smart captions & hashtags</h1>
          <p>
            PolymathAI understands your video content and writes titles,
            descriptions, and hashtags — intelligently.
          </p>
        </section>

        <UploadCard onGenerate={handleGenerate} loading={loading} />

        {status && (
  <div className="processing-box">
    {loading && <div className="spinner" />}
    <p className="muted">{status}</p>
  </div>
)}


        <ResultCard content={content} />
        <AuthModal open={authOpen} onClose={() => setAuthOpen(false)}>
  {authMode === "login" ? (
    <LoginForm
  onSwitch={() => setAuthMode("signup")}
  onSuccess={(token) => {
    setUser(getUserFromToken());
    setAuthOpen(false);
  }}
/>

  ) : (
    <SignupForm
      onSwitch={() => setAuthMode("login")}
      onSuccess={() => setAuthOpen(false)}
    />
  )}
</AuthModal>

<PricingModal
  open={pricingOpen}
  onClose={() => setPricingOpen(false)}
/>

      </main>

      <footer className="footer">
        Built for creators · PolymathAI
      </footer>
    </>
  );
}

export default App;
