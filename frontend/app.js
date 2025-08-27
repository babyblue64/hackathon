const API_BASE = "http://localhost:8000"; // Adjust if hosted elsewhere

async function signup() {
  const payload = {
    username: document.getElementById("signup-username").value,
    email: document.getElementById("signup-email").value,
    mobile: parseInt(document.getElementById("signup-mobile").value),
    password: document.getElementById("signup-password").value,
    confirm_password: document.getElementById("signup-confirm").value,
  };

  try {
    const res = await fetch(`${API_BASE}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    document.getElementById("signup-result").textContent = data.detail || JSON.stringify(data);
  } catch (err) {
    document.getElementById("signup-result").textContent = "Signup failed.";
  }
}

async function login() {
  const payload = {
    email: document.getElementById("login-email").value,
    password: document.getElementById("login-password").value,
  };

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (data.access_token) {
      localStorage.setItem("access_token", data.access_token);
      document.getElementById("login-result").textContent = "Login successful!";
    } else {
      document.getElementById("login-result").textContent = data.detail || "Login failed.";
    }
  } catch (err) {
    document.getElementById("login-result").textContent = "Login error.";
  }
}

async function getProfile() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    document.getElementById("profile-result").textContent = "Please log in first.";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/users/me`, {
      method: "GET",
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await res.json();
    document.getElementById("profile-result").textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    document.getElementById("profile-result").textContent = "Failed to fetch profile.";
  }
}
