import { useState } from "react";

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

export default function UploadCard({ onGenerate }) {
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState("vlog");

  return (
    <div className="card upload-card">
      <h2>Upload your video</h2>
      <p className="muted">
        PolymathAI understands spoken content and generates captions.
      </p>

      <label className="upload-box">
        <input
          type="file"
          accept="video/*"
          hidden
          onChange={(e) => setFile(e.target.files[0])}
        />
        {file ? (
          <span className="file-name">{file.name}</span>
        ) : (
          <span>Drag & drop or click to upload</span>
        )}
      </label>

      <div className="row">
        <label>
          Category
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>
                {c.charAt(0).toUpperCase() + c.slice(1)}
              </option>
            ))}
          </select>
        </label>
      </div>

      <button
  className="primary-btn"
  disabled={!file}
  onClick={() => {
    console.log("Generate clicked", file, category);
    onGenerate(file, category);
  }}
>
  🚀 Generate with AI
</button>


      <p className="tiny muted">Free for short videos</p>
    </div>
  );
}
