import { useEffect, useState } from "react";
import { getAccessToken } from "../utils/auth.js";
import { Edit, Clock, MapPin, Download, Upload, Pill, FileText, AlertCircle } from "lucide-react";

const MedicalDashboard = () => {
  const [profile, setProfile] = useState(null);
  const [role, setRole] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = getAccessToken();
        const res = await fetch("http://127.0.0.1:8000/surgery/me/", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!res.ok) throw new Error("Failed to fetch profile");

        const data = await res.json();
        setProfile(data.profile);
        setRole(data.role);
      } catch (err) {
        console.error("Dashboard fetch error:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) return <p>Loading profile...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!profile) return <p>No profile data found.</p>;

  // map backend fields to local variables
  const patientData = {
    name: profile.name,
    id: profile.id,
    dob: profile.birth_date,
    phone: profile.phonenumber,
    email: profile.email,
    sex: profile.sex,
    profilePic: profile.profile_pic
  };

  return (
    <div className="min-h-screen bg-gray-50">
   

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-12 gap-6">
          <div className="col-span-3">
            <div className="bg-white rounded-xl shadow-sm p-6 text-center">
              <div className="relative inline-block mb-4">
                <div className="w-24 h-24 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full mx-auto flex items-center justify-center text-white text-3xl font-bold">
                  {patientData.name[0]}
                </div>
              </div>
              <h2 className="text-xl font-bold text-gray-900 mb-1">{patientData.name}</h2>
              <p className="text-sm text-gray-500 mb-3">ID: {patientData.id}</p>
              <p className="text-gray-900 font-medium">DOB: {patientData.dob}</p>
              <p className="text-gray-900 font-medium">Phone: {patientData.phone}</p>
              <p className="text-gray-900 font-medium">Email: {patientData.email}</p>
              <p className="text-gray-900 font-medium">Sex: {patientData.sex}</p>
            </div>
          </div>

          <div className="col-span-9 space-y-6">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-bold text-gray-900">Welcome, {patientData.name}</h3>
              <p className="text-gray-600">Role: {role}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MedicalDashboard;
