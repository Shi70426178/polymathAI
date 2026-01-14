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
    const data = await res.json();

    // 🔥 Forward backend error properly
    throw {
      status: res.status,
      ...(data.detail || {}),
    };
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

/// ======================
// Auth
// ======================
export async function signup(username, email, password) {
  const res = await fetch(`${API_BASE}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Signup failed");
  }

  return res.json();
}


export async function login(email, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    throw new Error("Invalid credentials");
  }

  return res.json();
}