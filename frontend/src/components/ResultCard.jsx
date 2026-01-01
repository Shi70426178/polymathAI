export default function ResultCard({ content }) {
  if (!content) return null;

  return (
    <div className="card result-card">
      <h3>✨ PolymathAI suggests</h3>

      <h4>{content.title}</h4>
      <p>{content.description}</p>

      <div className="hashtags">
        {content.hashtags.map((tag) => (
          <span key={tag} className="tag">
            {tag}
          </span>
        ))}
      </div>

      <div className="row">
        <button
          className="secondary-btn"
          onClick={() =>
            navigator.clipboard.writeText(
              `${content.title}\n\n${content.description}\n\n${content.hashtags.join(" ")}`
            )
          }
        >
          Copy All
        </button>

        <button
          className="secondary-btn"
          onClick={() =>
            navigator.clipboard.writeText(content.hashtags.join(" "))
          }
        >
          Copy Hashtags
        </button>
      </div>
    </div>
  );
}
