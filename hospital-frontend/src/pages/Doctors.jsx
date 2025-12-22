import React, { useState, useEffect } from 'react';
import { Search, Mail, Phone, User } from 'lucide-react';
import { getAccessToken } from '../utils/auth.js'; // if you use JWT

export default function DoctorList() {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchDoctors();
  }, []);

  const fetchDoctors = async () => {
    setLoading(true);
    setError(null);

    try {
      const token = getAccessToken();
      const res = await fetch('http://127.0.0.1:8000/surgery/get/alldoctors/', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error('Failed to fetch doctors');

      const data = await res.json();
      setDoctors(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const filteredDoctors = doctors.filter(
    (doc) =>
      doc.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (doc.bio && doc.bio.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  if (loading)
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="inline-block h-12 w-12 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
          <p className="mt-4 text-gray-600">Loading doctors...</p>
        </div>
      </div>
    );

  if (error)
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
          <h3 className="text-red-800 font-semibold mb-2">Error Loading Doctors</h3>
          <p className="text-red-600">{error}</p>
          <button
            onClick={fetchDoctors}
            className="mt-4 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Our Doctors</h1>
          <p className="text-gray-600">Find and connect with our medical professionals</p>
        </div>

        {/* Search */}
        <div className="mb-6 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
          <input
            type="text"
            placeholder="Search by name or specialty..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Doctor Count */}
        <p className="text-gray-600 mb-4">
          {filteredDoctors.length} {filteredDoctors.length === 1 ? 'doctor' : 'doctors'} found
        </p>

        {/* Doctors Grid */}
        {filteredDoctors.length === 0 ? (
          <div className="text-center py-12">
            <User className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-600 mb-2">No doctors found</h3>
            <p className="text-gray-500">Try adjusting your search</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredDoctors.map((doctor) => {
              const profilePic = doctor.profile_pic
                ? `http://127.0.0.1:8000${doctor.profile_pic}`
                : null;

              return (
                <div
                  key={doctor.id}
                  className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden"
                >
                  {/* Profile Picture */}
                  <div className="bg-gradient-to-br from-blue-500 to-blue-600 h-32 flex items-center justify-center">
                    {profilePic ? (
                      <img
                        src={profilePic}
                        alt={doctor.name}
                        className="h-24 w-24 rounded-full border-4 border-white object-cover"
                      />
                    ) : (
                      <div className="h-24 w-24 rounded-full border-4 border-white bg-white flex items-center justify-center">
                        <User className="h-12 w-12 text-blue-600" />
                      </div>
                    )}
                  </div>

                  {/* Info */}
                  <div className="p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">{doctor.name}</h3>
                    {doctor.bio && <p className="text-gray-600 text-sm mb-4 line-clamp-2">{doctor.bio}</p>}

                    <div className="space-y-2 mb-4">
                      {doctor.email && (
                        <div className="flex items-center text-sm text-gray-600">
                          <Mail className="h-4 w-4 mr-2 text-blue-600" />
                          <span className="truncate">{doctor.email}</span>
                        </div>
                      )}

                      {doctor.phonenumber && (
                        <div className="flex items-center text-sm text-gray-600">
                          <Phone className="h-4 w-4 mr-2 text-blue-600" />
                          <span>{doctor.phonenumber}</span>
                        </div>
                      )}

                      {doctor.clocked_in !== undefined && (
                        <div className="flex items-center text-sm">
                          <span
                            className={`inline-block h-2 w-2 rounded-full mr-2 ${
                              doctor.clocked_in ? 'bg-green-500' : 'bg-gray-400'
                            }`}
                          />
                          <span className={doctor.clocked_in ? 'text-green-600' : 'text-gray-500'}>
                            {doctor.clocked_in ? 'Available Today' : 'Not Available'}
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Buttons */}
                    <div className="flex gap-2">
                      <button
                        onClick={() => window.location.href = `/doctors/${doctor.id}`}
                        className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-sm font-semibold"
                      >
                        View Profile
                      </button>
                      <button
                        onClick={() => console.log('Book appointment with', doctor.name)}
                        className="flex-1 bg-white border border-blue-600 text-blue-600 py-2 px-4 rounded-lg hover:bg-blue-50 transition-colors text-sm font-semibold"
                      >
                        Book
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
