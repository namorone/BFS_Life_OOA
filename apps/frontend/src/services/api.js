const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {
      // ignore json parse errors
    }
    throw new Error(message);
  }

  return response.json();
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
