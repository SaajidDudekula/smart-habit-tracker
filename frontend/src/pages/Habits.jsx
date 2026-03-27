import { useEffect, useState } from "react";
import "./Habits.css";

const API_BASE = "http://localhost:8000";

export default function Habits() {
  const [habits, setHabits] = useState([]);
  const [name, setName] = useState("");

  const token = localStorage.getItem("token");

  useEffect(() => {
    fetchHabits();
  }, []);

  // ==============================
  // FETCH (FALLBACK ONLY)
  // ==============================
  const fetchHabits = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/habits`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      setHabits(Array.isArray(data.habits) ? data.habits : []);
    } catch {
      setHabits([]);
    }
  };

  // ==============================
  // ADD HABIT (OPTIMISTIC)
  // ==============================
  const addHabit = async () => {
    if (!name.trim()) return;

    const tempHabit = {
      id: Date.now(),
      name,
      completed_today: false
    };

    setHabits(prev => [tempHabit, ...prev]);
    setName("");
    window.dispatchEvent(new Event("habits-updated"));

    try {
      await fetch(`${API_BASE}/api/habits`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ name })
      });

      fetchHabits(); // sync real ID
    } catch {
      fetchHabits();
    }
  };

  // ==============================
  // COMPLETE / UNDO (OPTIMISTIC)
  // ==============================
  const toggleComplete = async (id) => {
    setHabits(prev =>
      prev.map(h =>
        h.id === id
          ? { ...h, completed_today: !h.completed_today }
          : h
      )
    );

    window.dispatchEvent(new Event("habits-updated"));

    try {
      await fetch(`${API_BASE}/api/habits/${id}/complete`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }
      });
    } catch {
      fetchHabits(); // rollback safety
    }
  };

  // ==============================
  // EDIT HABIT (OPTIMISTIC)
  // ==============================
  const editHabit = async (id, oldName) => {
    const newName = prompt("Edit habit name:", oldName);
    if (!newName || newName === oldName) return;

    setHabits(prev =>
      prev.map(h => (h.id === id ? { ...h, name: newName } : h))
    );

    try {
      await fetch(`${API_BASE}/api/habits/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ name: newName })
      });
    } catch {
      fetchHabits();
    }
  };

  // ==============================
  // DELETE HABIT (OPTIMISTIC)
  // ==============================
  const deleteHabit = async (id) => {
    if (!window.confirm("Delete this habit?")) return;

    setHabits(prev => prev.filter(h => h.id !== id));
    window.dispatchEvent(new Event("habits-updated"));

    try {
      await fetch(`${API_BASE}/api/habits/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` }
      });
    } catch {
      fetchHabits();
    }
  };

  return (
    <div className="habits-page">
      <h2>Your Habits</h2>

      <div className="add-habit">
        <input
          placeholder="New habit name"
          value={name}
          onChange={e => setName(e.target.value)}
          onKeyDown={e => e.key === "Enter" && addHabit()}
        />
        <button className="btn-add" onClick={addHabit}>
          Add Habit
        </button>
      </div>

      <div className="habit-list">
        {habits.length === 0 ? (
          <p className="no-habits">No habits yet</p>
        ) : (
          habits.map(h => (
            <div
              key={h.id}
              className={`habit-card ${h.completed_today ? "completed" : ""}`}
            >
              <div className="habit-info">
                <h3>{h.name}</h3>
                {h.completed_today && <span>Done for today</span>}
              </div>

              <div className="habit-actions">
                <button onClick={() => toggleComplete(h.id)}>
                  {h.completed_today ? "Undo" : "Complete"}
                </button>
                <button onClick={() => editHabit(h.id, h.name)}>
                  Edit
                </button>
                <button onClick={() => deleteHabit(h.id)}>
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
