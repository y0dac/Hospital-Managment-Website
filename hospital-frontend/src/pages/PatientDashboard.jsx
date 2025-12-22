import React, { useState } from "react";
import logo from "../assets/logo.png";
import doctorImg from "../assets/doctor.png";
import Appointments from "./appointment";
import surgery from '../assets/surgery.png'
import MedicalDashboard from "./Profile";
import DoctorList from "./Doctors.jsx"
export default function PatientDashboard() {
  const [activePage, setActivePage] = useState("home");

  const doctors = [
    { id: 1, name: "Dr. Ahmed", specialty: "Cardiology" },
    { id: 2, name: "Dr. Sara", specialty: "Neurology" },
    { id: 3, name: "Dr. Omar", specialty: "Orthopedics" },
  ];

  return (
    <div className="min-h-screen w-screen bg-gray-100">
      {/* Navbar */}
      <nav className="flex justify-between items-center bg-white px-6 py-4 shadow-md">
        <div className="flex items-center gap-4">
          <img src={logo} alt="Logo" className="w-full h-22" />
          <span className="font-bold text-xl">Al Haram Surgery</span>
        </div>

        <div className="flex gap-6">
          <button
            onClick={() => setActivePage("home")}
            className= "bg-transparent hover:text-blue-700 font-semibold"
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
            onClick={() => setActivePage("doctors")}
            className="hover:text-blue-700 font-semibold"
          >
            Doctors
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
            {/* Department Info */}
            <section className="bg-blue-700 flex items-center gap-6 rounded-lg">
              <img
                src={surgery}
                alt="Department"
                className="w-full md:w-1/2 rounded-lg"
              />
              <div className="md:w-1/2  flex flex-col gap-4">
                <h2 className="text-2xl font-bold">
                  Welcome to Al Haram Surgery Department
                </h2>
                <p>
                  We provide high-quality surgical care with experienced doctors
                  and modern facilities.
                </p>
                <div className="flex gap-4 mt-4">
                  <button
                    onClick={() => setActivePage("appointments")}
                    className="bg-white text-blue-700 font-semibold px-4 py-2 rounded-lg hover:bg-gray-200 transition"
                  >
                    Book Appointment
                  </button>
                  <button
                    className="bg-transparent border border-white px-4 py-2 rounded-lg hover:bg-white hover:text-blue-700 transition"
                  >
                    Learn More
                  </button>
                </div>
              </div>
            </section>

            {/* Doctors */}
            <section >
              <h2 className="text-xl font-bold text-blue-700 mb-4">
                Our Doctors
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                {doctors.map((doctor) => (
                  <div
                    key={doctor.id}
                    className="bg-white p-4 rounded-lg shadow-md flex flex-col items-center"
                  >
                    <img
                      src={doctorImg}
                      alt={doctor.name}
                      className="w-24 h-24 rounded-full mb-4"
                    />
                    <h3 className="font-semibold text-lg">{doctor.name}</h3>
                    <p className="text-gray-500">{doctor.specialty}</p>
                  </div>
                ))}
              </div>
            </section>
          </>
        )}

        {/* APPOINTMENTS */}
        {activePage === "appointments" && <Appointments />}

        {/* DOCTORS */}
        {activePage === "doctors" && <DoctorList/>}

        {/* PROFILE */}
        {activePage === "profile" && <MedicalDashboard />}
      </main>
    </div>
  );
}