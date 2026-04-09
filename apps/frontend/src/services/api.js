/**
 * Єдиний HTTP-клієнт до бекенду. Усі нові виклики API додавайте тут через `request`
 * (або дрібні обгортки над ним), щоб автоматично отримувати:
 * — Bearer зі сховища;
 * — очищення простроченого токена при читанні (див. getStoredAuth);
 * — редірект на /login при 401 на не-auth шляхах.
 * Не викликайте `fetch` до API напряму з інших модулів.
 */
import { clearStoredAuth, getStoredAuth } from "../auth/storage";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

function redirectToLoginAfterAuthFailure() {
  clearStoredAuth();
  const path = `${window.location.pathname}${window.location.search}`;
  const returnTo = path && path !== "/login" ? `?returnTo=${encodeURIComponent(path)}` : "";
  window.location.replace(`/login${returnTo}`);
}

function normalizeErrorDetail(detail) {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((entry) => {
        if (typeof entry === "string") return entry;
        if (entry?.msg) return entry.msg;
        return JSON.stringify(entry);
      })
      .join(" ");
  }
  if (detail && typeof detail === "object" && detail.message) {
    return detail.message;
  }
  return "Request failed";
}

export async function request(path, options = {}) {
  const auth = getStoredAuth();
  const headers = { ...options.headers };

  if (options.body && !(options.body instanceof FormData) && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  if (auth?.access_token) {
    headers.Authorization = `Bearer ${auth.access_token}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });

  if (!response.ok) {
    if (response.status === 401 && !path.startsWith("/auth/")) {
      redirectToLoginAfterAuthFailure();
    }

    let message = `Request failed with status ${response.status}`;
    try {
      const data = await response.json();
      message = normalizeErrorDetail(data.detail) || message;
    } catch {
      // ignore json parse errors
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
    return response.json();
  }

  return null;
}

export async function login(credentials) {
  return request("/auth/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
}

export async function register(payload) {
  return request("/auth/register", {
    method: "POST",
    body: JSON.stringify({
      name: payload.name,
      email: payload.email,
      password: payload.password,
    }),
  });
}

export async function fetchDashboardStats() {
  return request("/dashboard/stats");
}

export async function fetchCategories() {
  return request("/categories");
}

export async function createItem(form) {
  const multipart = new FormData();

  const payload = {
    name: form.name,
    category_id: form.categoryId ? Number(form.categoryId) : null,
    purchase_date: form.purchaseDate || null,
    purchase_price: form.purchasePrice ? Number(form.purchasePrice) : null,
    description: form.description || null,
    warranty: form.hasWarranty
      ? {
          provider: form.warrantyProvider || null,
          expiry_date: form.warrantyExpiryDate,
          notes: form.warrantyNotes || null,
        }
      : null,
  };

  multipart.append("payload", JSON.stringify(payload));
  if (form.photo) {
    multipart.append("photo", form.photo);
  }

  return request("/items", {
    method: "POST",
    body: multipart,
  });
}
