export const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000";

async function handleResponse(res) {
  const data = await res.json().catch(() => ({ error: "Non-JSON response from server" }));
  if (!res.ok) {
    throw new Error(data.error || `Server error: ${res.status}`);
  }
  return data;
}

function networkError() {
  return new Error("Cannot reach backend server — is it running on port 5000?");
}

export async function analyzeResume(file) {
  const form = new FormData();
  form.append("resume", file);
  try {
    const res = await fetch(`${BASE_URL}/api/analyze`, { method: "POST", body: form });
    return handleResponse(res);
  } catch (e) {
    if (e instanceof TypeError) throw networkError();
    throw e;
  }
}

export async function improveBullet(bulletText) {
  try {
    const res = await fetch(`${BASE_URL}/api/improve-bullet`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ bullet_text: bulletText }),
    });
    return handleResponse(res);
  } catch (e) {
    if (e instanceof TypeError) throw networkError();
    throw e;
  }
}

export async function matchJobDescription(file, jobDescription) {
  const form = new FormData();
  form.append("resume", file);
  form.append("job_description", jobDescription);
  try {
    const res = await fetch(`${BASE_URL}/api/match`, { method: "POST", body: form });
    return handleResponse(res);
  } catch (e) {
    if (e instanceof TypeError) throw networkError();
    throw e;
  }
}

export async function extractKeywords(jobDescription) {
  try {
    const res = await fetch(`${BASE_URL}/api/extract-keywords`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_description: jobDescription }),
    });
    return handleResponse(res);
  } catch (e) {
    if (e instanceof TypeError) throw networkError();
    throw e;
  }
}

export async function analyzeMarket(file) {
  const form = new FormData();
  form.append("resume", file);
  try {
    const res = await fetch(`${BASE_URL}/api/market-analysis`, { method: "POST", body: form });
    return handleResponse(res);
  } catch (e) {
    if (e instanceof TypeError) throw networkError();
    throw e;
  }
}
