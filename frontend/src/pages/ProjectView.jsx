import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import { projectsApi, tasksApi } from "../api";

const STATUS_LABELS = {
  todo: "To Do",
  in_progress: "In Progress",
  done: "Done",
};

export default function ProjectView() {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [projectData, taskData] = await Promise.all([
        projectsApi.get(id),
        tasksApi.list(id, filter || undefined),
      ]);
      setProject(projectData);
      setTasks(taskData);
    } catch (err) {
      setError("Could not load project");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id, filter]);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    setSubmitting(true);
    try {
      await tasksApi.create(id, {
        title,
        description,
        due_date: dueDate || undefined,
      });
      setTitle("");
      setDescription("");
      setDueDate("");
      setShowForm(false);
      loadData();
    } catch (err) {
      setError(err.response?.data?.error || "Could not create task");
    } finally {
      setSubmitting(false);
    }
  };

  const handleStatusChange = async (taskId, status) => {
    await tasksApi.update(taskId, { status });
    loadData();
  };

  const handleDelete = async (taskId) => {
    if (!confirm("Delete this task?")) return;
    await tasksApi.remove(taskId);
    loadData();
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-6 py-8">
        <Link to="/dashboard" className="text-sm text-indigo-600 hover:underline">
          ← Back to Dashboard
        </Link>

        {loading ? (
          <p className="text-slate-500 text-sm mt-4">Loading...</p>
        ) : (
          <>
            <div className="flex items-center justify-between mt-2 mb-4">
              <div>
                <h1 className="text-xl font-bold">{project?.name}</h1>
                {project?.description && (
                  <p className="text-sm text-slate-500">{project.description}</p>
                )}
              </div>
              <button
                onClick={() => setShowForm((s) => !s)}
                className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium px-4 py-2 rounded-md transition"
              >
                {showForm ? "Cancel" : "+ New Task"}
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
                  placeholder="Task title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
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
                <input
                  type="date"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                  className="rounded-md border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <button
                  type="submit"
                  disabled={submitting}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium px-4 py-2 rounded-md transition disabled:opacity-50"
                >
                  {submitting ? "Creating..." : "Create Task"}
                </button>
              </form>
            )}

            <div className="flex gap-2 mb-4">
              {["", "todo", "in_progress", "done"].map((s) => (
                <button
                  key={s || "all"}
                  onClick={() => setFilter(s)}
                  className={`text-xs px-3 py-1.5 rounded-full border transition ${
                    filter === s
                      ? "bg-indigo-600 text-white border-indigo-600"
                      : "bg-white text-slate-600 border-slate-300 hover:bg-slate-100"
                  }`}
                >
                  {s ? STATUS_LABELS[s] : "All"}
                </button>
              ))}
            </div>

            {tasks.length === 0 ? (
              <p className="text-slate-500 text-sm">No tasks match this filter.</p>
            ) : (
              <div className="space-y-2">
                {tasks.map((t) => (
                  <div
                    key={t.id}
                    className="bg-white border border-slate-200 rounded-lg p-4 flex items-start justify-between"
                  >
                    <div className="flex-1">
                      <p className="font-medium">{t.title}</p>
                      {t.description && (
                        <p className="text-sm text-slate-500 mt-0.5">{t.description}</p>
                      )}
                      {t.due_date && (
                        <p className="text-xs text-slate-400 mt-1">Due {t.due_date}</p>
                      )}
                    </div>
                    <div className="flex items-center gap-2 ml-4">
                      <select
                        value={t.status}
                        onChange={(e) => handleStatusChange(t.id, e.target.value)}
                        className="text-xs rounded-md border border-slate-300 px-2 py-1"
                      >
                        {Object.entries(STATUS_LABELS).map(([value, label]) => (
                          <option key={value} value={value}>
                            {label}
                          </option>
                        ))}
                      </select>
                      <button
                        onClick={() => handleDelete(t.id)}
                        className="text-xs text-slate-400 hover:text-red-600"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
