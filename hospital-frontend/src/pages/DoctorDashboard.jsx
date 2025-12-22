import React, { useState } from "react";
import logo from "../assets/logo.png";
import patientImg from "../assets/doctor.png";
import surgery from "../assets/surgery.png";
import { getAccessToken } from "../utils/auth.js";


export default function DoctorDashboard() {
  const [activePage, setActivePage] = useState("home");
  const [showClockInModal, setShowClockInModal] = useState(false);
  const [endTime, setEndTime] = useState("");
  const [shiftLoading, setShiftLoading] = useState(false);
  const [shiftMessage, setShiftMessage] = useState("");

  const patients = [
    { id: 1, name: "John Mitchell", condition: "Knee Surgery" },
    { id: 2, name: "Sarah Connor", condition: "Cardiology" },
    { id: 3, name: "Michael Chen", condition: "Physical Therapy" },
  ];

const handleClockIn = async () => {
  try {
    setShiftLoading(true);

    const token = getAccessToken();
    if (!token) throw new Error("Not authenticated");

    if (!endTime) throw new Error("Please select an end time");

    const now = new Date();
    const startTimeStr = now.toTimeString().slice(0, 5); // "HH:MM"
    const dateStr = now.toISOString().split("T")[0]; // "YYYY-MM-DD"

    const payload = {
      start_time: startTimeStr,
      end_time: endTime,
      date: dateStr,
    };

    const response = await fetch(
      "http://127.0.0.1:8000/surgery/shift/register/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      }
    );

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.detail || "Failed to register shift");
    }

    alert("Shift registered successfully!");
    setShowClockInModal(false);
    setEndTime("");
  } catch (err) {
    console.error("Shift error:", err);
    alert(err.message);
  } finally {
    setShiftLoading(false);
  }
};



  return (
    <div className="min-h-screen w-screen bg-gray-100">
      {/* Navbar */}
      <nav className="flex justify-between items-center bg-white px-6 py-4 shadow-md">
        <div className="flex items-center gap-4">
          <img src={logo} alt="Logo" className="w-16 h-16" />
          <span className="font-bold text-xl">Al Haram Surgery</span>
        </div>
        <div className="flex gap-6">
          <button
            onClick={() => setActivePage("home")}
            className="hover:text-blue-700 font-semibold"
          >
            Home
          </button>
          <button
            onClick={() => setActivePage("appointments")}
            className="hover:text-blue-700 font-semibold"
          >
            Appointments
          </button>
          <button
            onClick={() => setActivePage("patients")}
            className="hover:text-blue-700 font-semibold"
          >
            Patients
          </button>
          <button
            onClick={() => setActivePage("profile")}
            className="hover:text-blue-700 font-semibold"
          >
            Profile
          </button>
        </div>
      </nav>

      {/* Page Content */}
      <main className="p-6 space-y-10">
        {/* HOME */}
        {activePage === "home" && (
          <>
            <section className="bg-blue-700 flex flex-col md:flex-row items-center gap-6 rounded-lg p-6 text-white">
              <img
                src={surgery}
                alt="Department"
                className="w-full md:w-1/2 rounded-lg"
              />
              <div className="md:w-1/2 flex flex-col gap-4">
                <h2 className="text-2xl font-bold">
                  Welcome to Al Haram Surgery Department
                </h2>
                <p>
                  Start your shift and manage your patients effectively.
                </p>
                <div className="flex gap-4 mt-4">
                  <button
                    onClick={() => setShowClockInModal(true)}
                    className="bg-white text-blue-700 font-semibold px-4 py-2 rounded-lg hover:bg-gray-200 transition"
                  >
                    Clock In
                  </button>
                  <button className="border border-white px-4 py-2 rounded-lg hover:bg-white hover:text-blue-700 transition">
                    Learn More
                  </button>
                </div>
              </div>
            </section>

            {/* Patients Preview */}
            <section>
              <h2 className="text-xl font-bold text-blue-700 mb-4">
                Your Patients
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                {patients.map((patient) => (
                  <div
                    key={patient.id}
                    className="bg-white p-4 rounded-lg shadow-md flex flex-col items-center"
                  >
                    <img
                      src={patientImg}
                      alt={patient.name}
                      className="w-24 h-24 rounded-full mb-4"
                    />
                    <h3 className="font-semibold text-lg">{patient.name}</h3>
                    <p className="text-gray-500">{patient.condition}</p>
                  </div>
                ))}
              </div>
            </section>
          </>
        )}

        {/* Clock In Modal */}
      {showClockInModal && (
  <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
    <div className="bg-white text-gray-900 rounded-lg shadow-lg p-6 w-80">
      <h3 className="text-lg font-bold mb-4 text-gray-900">Clock In</h3>
      <p className="mb-2 text-gray-700">
        Start Time: {new Date().toLocaleTimeString()}
      </p>
      <label className="block mb-2 text-gray-700">
        End Time:
        <input
          type="time"
          value={endTime}
          onChange={(e) => setEndTime(e.target.value)}
          className="w-full mt-1 border border-gray-300 rounded-lg px-2 py-1 text-gray-900"
        />
      </label>
      <div className="flex justify-end gap-2 mt-4">
        <button
          onClick={() => setShowClockInModal(false)}
          className="px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-100 text-gray-700"
        >
          Cancel
        </button>
        <button
          onClick={handleClockIn}
          className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
          disabled={shiftLoading}
        >
          {shiftLoading ? "Registering..." : "Confirm"}
        </button>
      </div>
    </div>
  </div>
)}

      </main>
    </div>
  );
}
