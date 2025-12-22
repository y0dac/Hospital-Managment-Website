import { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import logo from "../assets/logo.png";

export default function Signup() {
  const [role, setRole] = useState("patient");
  const [form, setForm] = useState({
    ssn: "",
    name: "",
    password: "",
    birth_date: "",
    phone_number: "",
    sex: "",
    medical_license: "", // <- matches Django serializer
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    // Basic validation
    if (
      !form.ssn ||
      !form.name ||
      !form.password ||
      !form.birth_date ||
      !form.phone_number ||
      !form.sex
    ) {
      setError("Please fill all required fields");
      return;
    }

    if (role === "doctor" && !form.medical_license) {
      setError("Please provide your medical license number");
      return;
    }

    try {
      const url =
        role === "patient"
          ? "http://127.0.0.1:8000/surgery/register/patient/"
          : "http://127.0.0.1:8000/surgery/register/doctor/";

      // Payload now matches Django serializer field names
      const payload = { ...form };

      await axios.post(url, payload, {
        headers: { "Content-Type": "application/json" },
      });

      setSuccess("Registration successful! Redirecting to login...");
      setTimeout(() => (window.location.href = "/login"), 1500);
    } catch (err) {
      console.error(err.response?.data || err.message);

      // Show DRF validation errors if present
      if (err.response?.data) {
        const messages = Object.entries(err.response.data)
          .map(([key, val]) => `${key}: ${val}`)
          .join(" | ");
        setError(messages);
      } else {
        setError("Failed to register. Check your details.");
      }
    }
  };

  return (
    <div className="w-screen min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-400 to-blue-900">

      {/* Logo */}
      <img
        src={logo}
        alt="Al Haram Surgery Department"
        className="w-48 md:w-56 mb-8 opacity-90 drop-shadow-lg select-none"
      />

      {/* Signup Form */}
      <form
        onSubmit={handleSubmit}
        className="bg-black text-white p-10 rounded-2xl shadow-2xl w-full max-w-md border border-blue-600"
      >
        <h2 className="text-3xl font-bold mb-2 text-center text-blue-400">
          Signup
        </h2>
        <p className="text-center text-gray-400 mb-6">
          Create your patient or doctor account
        </p>

        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        {success && <p className="text-green-500 text-sm mb-4">{success}</p>}

        {/* Role Selector */}
        <div className="flex justify-center gap-6 mb-5">
          <label className="cursor-pointer text-gray-300">
            <input
              type="radio"
              checked={role === "patient"}
              onChange={() => setRole("patient")}
              className="mr-2"
            />
            Patient
          </label>
          <label className="cursor-pointer text-gray-300">
            <input
              type="radio"
              checked={role === "doctor"}
              onChange={() => setRole("doctor")}
              className="mr-2"
            />
            Doctor
          </label>
        </div>

        {/* Inputs */}
        <input
          name="ssn"
          placeholder="SSN"
          onChange={handleChange}
          className="w-full mb-4 p-3 rounded-lg bg-gray-900 text-white placeholder-gray-400 border border-gray-700 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30"
        />

        <input
          name="name"
          placeholder="Full Name"
          onChange={handleChange}
          className="w-full mb-4 p-3 rounded-lg bg-gray-900 text-white placeholder-gray-400 border border-gray-700 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30"
        />

        <input
          name="password"
          type="password"
          placeholder="Password"
          onChange={handleChange}
          className="w-full mb-4 p-3 rounded-lg bg-gray-900 text-white placeholder-gray-400 border border-gray-700 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30"
        />

        <input
          name="birth_date"
          type="date"
          onChange={handleChange}
          className="w-full mb-4 p-3 rounded-lg bg-gray-900 text-white border border-gray-700 focus:outline-none focus:border-blue-500"
        />

        <input
          name="phone_number"
          placeholder="Phone Number"
          onChange={handleChange}
          className="w-full mb-4 p-3 rounded-lg bg-gray-900 text-white placeholder-gray-400 border border-gray-700 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30"
        />

        <select
          name="sex"
          onChange={handleChange}
          className="w-full mb-4 p-3 rounded-lg bg-gray-900 text-white border border-gray-700 focus:outline-none focus:border-blue-500"
        >
          <option value="">Select Sex</option>
          <option value="M">Male</option>
          <option value="F">Female</option>
        </select>

        {/* Doctor-only field */}
        {role === "doctor" && (
          <input
            name="medical_license" // <- changed
            placeholder="Medical License Number"
            onChange={handleChange}
            className="w-full mb-4 p-3 rounded-lg bg-gray-900 text-white placeholder-gray-400 border border-gray-700 focus:outline-none focus:border-blue-500"
          />
        )}

        <button className="w-full bg-blue-800 py-3 rounded-lg font-semibold hover:bg-blue-700 transition">
          Sign Up
        </button>

        <p className="text-center text-gray-400 text-sm mt-6">
          Already have an account?{" "}
          <Link
            to="/login"
            className="text-blue-400 hover:underline font-semibold"
          >
            Login here
          </Link>
        </p>
      </form>
    </div>
  );
}
