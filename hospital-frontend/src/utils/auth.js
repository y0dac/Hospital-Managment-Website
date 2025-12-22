const ACCESS_TOKEN_KEY = "accessToken";
const REFRESH_TOKEN_KEY = "refreshToken";

export const saveTokens = (access, refresh) => {
  localStorage.setItem(ACCESS_TOKEN_KEY, access);
  localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
};

export const getAccessToken = () => localStorage.getItem(ACCESS_TOKEN_KEY);
export const getRefreshToken = () => localStorage.getItem(REFRESH_TOKEN_KEY);

export const removeTokens = () => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};
export const getUserId = () => {
  const token = getAccessToken();
  if (!token) return null;

  try {
    const payload = token.split(".")[1]; // JWT structure: header.payload.signature
    const decoded = JSON.parse(atob(payload));
    return decoded.user_id || decoded.id || null; // adjust depending on your backend
  } catch (err) {
    console.error("Failed to decode token:", err);
    return null;
  }
};