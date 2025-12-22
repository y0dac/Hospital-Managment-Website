import { useEffect, useState } from "react";
import axios from "axios";
import { getAccessToken, getUserId } from "../utils/auth";

export default function Appointments() {
  const [current, setCurrent] = useState([]);
  const [finished, setFinished] = useState([]);
  const [loading, setLoading] = useState(true);
  const patientId = getUserId();

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const token = getAccessToken();

        const currentRes = await axios.get(
          `http://127.0.0.1:8000/surgery/appointment/patient/${patientId}/`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        const finishedRes = await axios.get(
          `http://127.0.0.1:8000/surgery/appointment/patient/finished/`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        setCurrent(currentRes.data);
        setFinished(finishedRes.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAppointments();
  }, [patientId]);

  if (loading) {
    return (
      <div className="p-6">
        <p className="text-gray-600 font-semibold">
          Loading appointments...
        </p>
      </div>
    );
  }

  return (
    <div className="w-screen space-y-10">
      {/* CURRENT APPOINTMENTS */}
      <section>
        <h2 className="text-xl font-bold text-blue-700 mb-4">
          Upcoming Appointments
        </h2>

        {current.length === 0 ? (
          <p className="text-gray-500">No upcoming appointments.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {current.map((appt) => (
              <div
                key={appt.id}
                className="bg-white p-4 rounded-lg shadow-md"
              >
                <p className="text-gray-700">
                  <span className="font-semibold">Date:</span> {appt.date}
                </p>
                <p className="text-gray-700">
                  <span className="font-semibold">Doctor:</span>{" "}
                  {appt.doctor?.name}
                </p>
                <p className="text-gray-700">
                  <span className="font-semibold">Reason:</span>{" "}
                  {appt.reason}
                </p>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* FINISHED APPOINTMENTS */}
      <section>
        <h2 className="text-xl font-bold text-blue-700 mb-4">
          Appointment History
        </h2>

        {finished.length === 0 ? (
          <p className="text-gray-500">No past appointments.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {finished.map((appt) => (
              <div
                key={appt.id}
                className="bg-white p-4 rounded-lg shadow-md border-l-4 border-blue-600"
              >
                <p className="text-gray-700">
                  <span className="font-semibold">Date:</span> {appt.date}
                </p>
                <p className="text-gray-700">
                  <span className="font-semibold">Doctor:</span>{" "}
                  {appt.doctor?.name}
                </p>
                <p className="text-gray-700">
                  <span className="font-semibold">Reason:</span>{" "}
                  {appt.reason}
                </p>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}