const API_BASE_URL = "http://<ejemplo_de_ip_jjj>:8000";

const form = document.getElementById("shorten-form");
const originalUrlInput = document.getElementById("original-url");
const errorBox = document.getElementById("error-box");
const resultBox = document.getElementById("result-box");
const shortUrlOutput = document.getElementById("short-url-output");
const copyBtn = document.getElementById("btn-copy");
const copyStatus = document.getElementById("copy-status");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  hideElements();

  const originalUrl = originalUrlInput.value.trim();
  if (!originalUrl) return;

  try {
    const response = await fetch(`${API_BASE_URL}/shorten`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ original_url: originalUrl })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Error en el servidor");
    }

    const data = await response.json();
    shortUrlOutput.value = data.short_url;
    resultBox.classList.remove("hidden");
  } catch (err) {
    showError(`Error al acortar URL: ${err.message}`);
  }
});

copyBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(shortUrlOutput.value);
    copyStatus.classList.remove("hidden");
    setTimeout(() => copyStatus.classList.add("hidden"), 3000);
  } catch {
    showError("No se pudo copiar automáticamente");
  }
});

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.classList.remove("hidden");
}

function hideElements() {
  errorBox.classList.add("hidden");
  resultBox.classList.add("hidden");
}