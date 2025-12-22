import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import DoctorDashboard from "./pages/DoctorDashboard";
import PatientDashboard from "./pages/PatientDashboard";
import { getAccessToken } from "./utils/auth";

// Simple Protected Route Component
const PrivateRoute = ({ children }) => {
  const token = getAccessToken();
  return token ? children : <Navigate to="/login" replace />;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Protected Routes */}
        <Route
          path="/doctor-dashboard"
          element={
            <PrivateRoute>
              <DoctorDashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/patient-dashboard"
          element={
            <PrivateRoute>
              <PatientDashboard />
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
