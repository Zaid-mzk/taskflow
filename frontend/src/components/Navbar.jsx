import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="bg-white border-b border-slate-200 px-6 py-3 flex items-center justify-between">
      <Link to="/dashboard" className="text-lg font-bold text-indigo-600">
        TaskFlow
      </Link>
      {isAuthenticated && (
        <div className="flex items-center gap-4 text-sm">
          <span className="text-slate-600">Hi, {user.username}</span>
          <button
            onClick={handleLogout}
            className="px-3 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 transition"
          >
            Log out
          </button>
        </div>
      )}
    </nav>
  );
}
