import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import { projectsApi } from "../api";

export default function Dashboard() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const loadProjects = async () => {
    setLoading(true);
    try {
      const data = await projectsApi.list();
      setProjects(data);
    } catch (err) {
      setError("Could not load projects");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    setSubmitting(true);
    try {
      await projectsApi.create({ name, description });
      setName("");
      setDescription("");
      setShowForm(false);
      loadProjects();
    } catch (err) {
      setError(err.response?.data?.error || "Could not create project");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this project and all its tasks?")) return;
    await projectsApi.remove(id);
    loadProjects();
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-xl font-bold">Your Projects</h1>
          <button
            onClick={() => setShowForm((s) => !s)}
            className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium px-4 py-2 rounded-md transition"
          >
            {showForm ? "Cancel" : "+ New Project"}
          </button>
        </div>

        {error && (
          <div className="mb-4 text-sm text-red-700 bg-red-50 border border-red-200 rounded-md p-2">
            {error}
          </div>
        )}

        {showForm && (
          <form
            onSubmit={handleCreate}
            className="bg-white border border-slate-200 rounded-lg p-4 mb-6 space-y-3"
          >
            <input
              placeholder="Project name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <textarea
              placeholder="Description (optional)"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={2}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <button
              type="submit"
              disabled={submitting}
              className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium px-4 py-2 rounded-md transition disabled:opacity-50"
            >
              {submitting ? "Creating..." : "Create Project"}
            </button>
          </form>
        )}

        {loading ? (
          <p className="text-slate-500 text-sm">Loading...</p>
        ) : projects.length === 0 ? (
          <p className="text-slate-500 text-sm">No projects yet. Create your first one!</p>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2">
            {projects.map((p) => (
              <div
                key={p.id}
                className="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-sm transition"
              >
                <div className="flex items-start justify-between">
                  <Link to={`/project/${p.id}`} className="font-semibold text-indigo-600 hover:underline">
                    {p.name}
                  </Link>
                  <button
                    onClick={() => handleDelete(p.id)}
                    className="text-xs text-slate-400 hover:text-red-600"
                  >
                    Delete
                  </button>
                </div>
                {p.description && (
                  <p className="text-sm text-slate-500 mt-1 line-clamp-2">{p.description}</p>
                )}
                <div className="flex gap-3 mt-3 text-xs text-slate-500">
                  <span>To Do: {p.task_counts.todo}</span>
                  <span>In Progress: {p.task_counts.in_progress}</span>
                  <span>Done: {p.task_counts.done}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
