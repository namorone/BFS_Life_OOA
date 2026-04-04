import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import ProtectedRoute from "../components/ProtectedRoute";
import DashboardPage from "../pages/DashboardPage";
import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage";
import { useAuth } from "../hooks/useAuth";

function HomeRedirect() {
  const { isAuthenticated } = useAuth();
  return <Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />;
}

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomeRedirect />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
