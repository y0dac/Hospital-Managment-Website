import { createContext, useContext, useState, useEffect } from "react";
import { fetchUserProfile, setToken } from "../services/api.js";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [role, setRole] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      setToken(token);
      fetchUserProfile().then(({ data, role }) => {
        setUser(data);
        setRole(role);
        setLoading(false);
      });
    } else {
      setLoading(false);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, role, setRole }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
