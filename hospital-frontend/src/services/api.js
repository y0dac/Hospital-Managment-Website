import axios from "axios";
import { getAccessToken, saveTokens, removeTokens } from "../utils/auth";

const BASE_URL = "http://127.0.0.1:8000";

export const setToken = (token) => {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
};

// Create an axios instance
const api = axios.create({
  baseURL: `${BASE_URL}/surgery/`,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add JWT token to headers automatically
api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ===== Authentication =====
export const login = async (ssn, password) => {
  const res = await axios.post(`${BASE_URL}/api/token/`, { ssn, password });
  saveTokens(res.data.access, res.data.refresh);
  return res.data;
};

export const signup = async (payload, role) => {
  const url =
    role === "patient"
      ? `${BASE_URL}/register/patient/`
      : `${BASE_URL}/register/doctor/`;
  const res = await axios.post(url, payload);
  return res.data;
};

// ===== Fetch Profile =====
export const fetchUserProfile = async () => {
  try {
    const resPatient = await api.get("patient/profile/");
    return { ...resPatient.data, role: "patient" };
  } catch {
    const resDoctor = await api.get("doctor/profile/");
    return { ...resDoctor.data, role: "doctor" };
  }
};

// ===== Logout =====
export const logout = () => {
  removeTokens();
};

// ===== Other API calls =====
// You can add more functions here later, e.g. appointments, surgery, scans, etc.

export default api;
