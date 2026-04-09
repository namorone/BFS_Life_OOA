import { isAccessTokenExpired } from "./jwt";

const AUTH_KEY = "bfs_auth";

/**
 * @returns {{ access_token: string, user: { id: number, email: string, full_name: string } } | null}
 */
export function getStoredAuth() {
  try {
    const raw = localStorage.getItem(AUTH_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (!parsed?.access_token || !parsed?.user) return null;
    if (isAccessTokenExpired(parsed.access_token)) {
      localStorage.removeItem(AUTH_KEY);
      return null;
    }
    return parsed;
  } catch {
    return null;
  }
}

export function setStoredAuth(auth) {
  localStorage.setItem(AUTH_KEY, JSON.stringify(auth));
}

export function clearStoredAuth() {
  localStorage.removeItem(AUTH_KEY);
}
