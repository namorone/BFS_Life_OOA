/**
 * Decode JWT payload (no signature verification — for client-side expiry UX only).
 * @param {string} token
 * @returns {Record<string, unknown> | null}
 */
export function decodeJwtPayload(token) {
  if (!token || typeof token !== "string") return null;
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  try {
    const base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    const padded = base64.padEnd(base64.length + ((4 - (base64.length % 4)) % 4), "=");
    const json = atob(padded);
    return JSON.parse(json);
  } catch {
    return null;
  }
}

/** @param {string} token */
export function getAccessTokenExpiryMs(token) {
  const payload = decodeJwtPayload(token);
  if (!payload?.exp || typeof payload.exp !== "number") return null;
  return payload.exp * 1000;
}

/** @param {string} token */
export function isAccessTokenExpired(token) {
  const expMs = getAccessTokenExpiryMs(token);
  if (expMs == null) return true;
  return Date.now() >= expMs;
}
