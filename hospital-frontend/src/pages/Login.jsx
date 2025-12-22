import { useState } from "react";
import axios from "axios";
import { saveTokens } from "../utils/auth";
import { fetchUserProfile, setToken } from "../services/api";
import { Link, useNavigate } from "react-router-dom";
import logo from "../assets/logo.png";

export default function Login() {
  const [form, setForm] = useState({ ssn: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      // Login
      const res = await axios.post("http://127.0.0.1:8000/api/token/", form);
      saveTokens(res.data.access, res.data.refresh);
      setToken(res.data.access);

      // Fetch profile (patient or doctor)
      const { role } = await fetchUserProfile();

      // Navigate based on role
      if (role === "doctor") navigate("/doctor-dashboard");
      else navigate("/patient-dashboard");
    } catch (err) {
      console.error(err);
      setError("Invalid SSN or password");
    }
  };

  return (
    <div className="w-screen min-h-screen flex flex-col items-center justify-center bg-linear-to-br from-blue-400 to-blue-900">
      <img
        src={logo}
        alt="Al Haram Surgery Department"
        className="w-64 md:w-72 mb-10 opacity-90 drop-shadow-xl select-none"
      />
      <form
        onSubmit={handleSubmit}
        className="bg-black text-white p-10 rounded-2xl shadow-2xl w-full max-w-md border border-blue-600"
      >
        <h2 className="text-3xl font-bold mb-6 text-center text-blue-400">
          Login
        </h2>
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        <input
          name="ssn"
          placeholder="SSN"
          autoComplete="username"
          onChange={handleChange}
          className="w-full mb-4 p-3 rounded-lg bg-gray-900 text-white placeholder-gray-400 border border-gray-700 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30"
        />
        <input
          name="password"
          type="password"
          placeholder="Password"
          autoComplete="current-password"
          onChange={handleChange}
          className="w-full mb-6 p-3 rounded-lg bg-gray-900 text-white placeholder-gray-400 border border-gray-700 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30"
        />
        <button className="w-full bg-blue-800 py-3 rounded-lg font-semibold hover:bg-blue-700 transition">
          Login
        </button>
        <p className="text-center text-gray-400 text-sm mt-6">
          Don't have an account?{" "}
          <Link to="/signup" className="text-blue-400 hover:underline font-semibold">
            Sign up now
          </Link>
        </p>
      </form>
    </div>
  );
}
