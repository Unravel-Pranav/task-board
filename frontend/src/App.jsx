import { useState, useEffect, useCallback } from 'react'
import confetti from 'canvas-confetti'
import { motion, AnimatePresence } from 'framer-motion'

// API Base URL
const API_BASE = '/api'

// Priority colors and labels
const PRIORITIES = {
  high: { label: 'High', class: 'priority-high', emoji: '🔥' },
  medium: { label: 'Medium', class: 'priority-medium', emoji: '⚡' },
  low: { label: 'Low', class: 'priority-low', emoji: '🌱' },
}

// Confetti celebration
const triggerConfetti = () => {
  const defaults = {
    spread: 360,
    ticks: 100,
    gravity: 0.5,
    decay: 0.94,
    startVelocity: 30,
    colors: ['#22c55e', '#14b8a6', '#06b6d4', '#f59e0b', '#ec4899']
  }

  confetti({
    ...defaults,
    particleCount: 50,
    scalar: 1.2,
    shapes: ['star']
  })

  confetti({
    ...defaults,
    particleCount: 30,
    scalar: 0.75,
    shapes: ['circle']
  })
}

// Task Item Component
const TaskItem = ({ task, onToggle, onDelete }) => {
  const priority = PRIORITIES[task.priority] || PRIORITIES.medium

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, x: -100 }}
      transition={{ duration: 0.3 }}
      className={`task-card glass rounded-xl p-4 flex items-center gap-4 ${
        task.completed ? 'opacity-60' : ''
      }`}
    >
      {/* Checkbox */}
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => onToggle(task.id)}
        className="checkbox-custom flex-shrink-0"
      />

      {/* Task Content */}
      <div className="flex-1 min-w-0">
        <p className={`text-white font-medium ${task.completed ? 'line-through opacity-50' : ''}`}>
          {task.title}
        </p>
        <div className="flex items-center gap-2 mt-1">
          <span className={`${priority.class} px-2 py-0.5 rounded-full text-xs text-white font-medium`}>
            {priority.emoji} {priority.label}
          </span>
          <span className="text-gray-400 text-xs">
            {new Date(task.created_at).toLocaleDateString()}
          </span>
        </div>
      </div>

      {/* Delete Button */}
      <button
        onClick={() => onDelete(task.id)}
        className="delete-btn p-2 rounded-lg hover:bg-red-500/20 text-gray-400 hover:text-red-400 transition-all"
        aria-label="Delete task"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </motion.div>
  )
}

// Progress Ring Component
const ProgressRing = ({ progress }) => {
  const circumference = 2 * Math.PI * 45
  const strokeDashoffset = circumference - (progress / 100) * circumference

  return (
    <div className="relative w-32 h-32">
      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
        {/* Background ring */}
        <circle
          cx="50"
          cy="50"
          r="45"
          stroke="rgba(255,255,255,0.1)"
          strokeWidth="8"
          fill="none"
        />
        {/* Progress ring */}
        <circle
          cx="50"
          cy="50"
          r="45"
          stroke="url(#gradient)"
          strokeWidth="8"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          style={{ transition: 'stroke-dashoffset 0.5s ease-out' }}
        />
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#22c55e" />
            <stop offset="50%" stopColor="#14b8a6" />
            <stop offset="100%" stopColor="#06b6d4" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-bold text-white">{Math.round(progress)}%</span>
        <span className="text-xs text-gray-400">Complete</span>
      </div>
    </div>
  )
}

// Stats Card Component
const StatsCard = ({ icon, label, value, color }) => (
  <motion.div
    whileHover={{ scale: 1.05 }}
    className="glass rounded-xl p-4 flex items-center gap-3"
  >
    <div className={`w-10 h-10 rounded-lg ${color} flex items-center justify-center`}>
      {icon}
    </div>
    <div>
      <p className="text-2xl font-bold text-white">{value}</p>
      <p className="text-xs text-gray-400">{label}</p>
    </div>
  </motion.div>
)

// Main App Component
function App() {
  const [tasks, setTasks] = useState([])
  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0, progress_percentage: 0 })
  const [newTaskTitle, setNewTaskTitle] = useState('')
  const [newTaskPriority, setNewTaskPriority] = useState('medium')
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all') // all, pending, completed

  // Fetch tasks
  const fetchTasks = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE}/tasks`)
      if (response.ok) {
        const data = await response.json()
        setTasks(data.tasks)
        setStats({
          total: data.total,
          completed: data.completed,
          pending: data.pending,
          progress_percentage: data.progress_percentage
        })
      }
    } catch (error) {
      console.error('Error fetching tasks:', error)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchTasks()
  }, [fetchTasks])

  // Add task
  const handleAddTask = async (e) => {
    e.preventDefault()
    if (!newTaskTitle.trim()) return

    try {
      const response = await fetch(`${API_BASE}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTaskTitle, priority: newTaskPriority })
      })
      
      if (response.ok) {
        setNewTaskTitle('')
        fetchTasks()
      }
    } catch (error) {
      console.error('Error adding task:', error)
    }
  }

  // Toggle task completion
  const handleToggleTask = async (taskId) => {
    try {
      const response = await fetch(`${API_BASE}/tasks/${taskId}/toggle`, {
        method: 'PATCH'
      })
      
      if (response.ok) {
        const updatedTask = await response.json()
        
        // Check if all tasks are now completed for confetti
        const currentTasks = tasks.map(t => t.id === taskId ? updatedTask : t)
        const allCompleted = currentTasks.length > 0 && currentTasks.every(t => t.completed)
        
        if (allCompleted) {
          triggerConfetti()
        } else if (updatedTask.completed) {
          // Single task completion mini celebration
          confetti({
            particleCount: 20,
            spread: 45,
            origin: { y: 0.7 },
            colors: ['#22c55e', '#14b8a6']
          })
        }
        
        fetchTasks()
      }
    } catch (error) {
      console.error('Error toggling task:', error)
    }
  }

  // Delete task
  const handleDeleteTask = async (taskId) => {
    try {
      const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
        method: 'DELETE'
      })
      
      if (response.ok) {
        fetchTasks()
      }
    } catch (error) {
      console.error('Error deleting task:', error)
    }
  }

  // Filter tasks
  const filteredTasks = tasks.filter(task => {
    if (filter === 'pending') return !task.completed
    if (filter === 'completed') return task.completed
    return true
  })

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-green-500"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background Orbs */}
      <div className="floating-orb w-96 h-96 bg-green-500/30 -top-48 -left-48" />
      <div className="floating-orb w-80 h-80 bg-cyan-500/20 top-1/2 -right-40" style={{ animationDelay: '-5s' }} />
      <div className="floating-orb w-64 h-64 bg-purple-500/20 bottom-20 left-1/4" style={{ animationDelay: '-10s' }} />

      <div className="relative z-10 max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <motion.header 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-10"
        >
          <h1 className="font-display text-5xl font-extrabold gradient-text mb-2">
            TaskFlow
          </h1>
          <p className="text-gray-400 font-body">
            Stay organized, stay productive ✨
          </p>
        </motion.header>

        {/* Stats Section */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-dark rounded-2xl p-6 mb-8"
        >
          <div className="flex flex-col md:flex-row items-center gap-6">
            {/* Progress Ring */}
            <ProgressRing progress={stats.progress_percentage} />

            {/* Stats Cards */}
            <div className="flex-1 grid grid-cols-3 gap-4">
              <StatsCard
                icon={<span className="text-lg">📋</span>}
                label="Total Tasks"
                value={stats.total}
                color="bg-blue-500/20"
              />
              <StatsCard
                icon={<span className="text-lg">✅</span>}
                label="Completed"
                value={stats.completed}
                color="bg-green-500/20"
              />
              <StatsCard
                icon={<span className="text-lg">⏳</span>}
                label="Pending"
                value={stats.pending}
                color="bg-amber-500/20"
              />
            </div>
          </div>

          {/* Motivational message */}
          {stats.total > 0 && stats.progress_percentage === 100 && (
            <motion.div 
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="mt-4 text-center"
            >
              <span className="text-2xl">🎉</span>
              <p className="text-green-400 font-medium">All tasks completed! You're amazing!</p>
            </motion.div>
          )}
        </motion.div>

        {/* Add Task Form */}
        <motion.form 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          onSubmit={handleAddTask}
          className="glass-dark rounded-2xl p-6 mb-8"
        >
          <div className="flex flex-col md:flex-row gap-4">
            {/* Task Input */}
            <input
              type="text"
              value={newTaskTitle}
              onChange={(e) => setNewTaskTitle(e.target.value)}
              placeholder="What needs to be done?"
              className="flex-1 bg-white/5 border border-white/10 rounded-xl px-5 py-4 text-white placeholder-gray-500 focus:outline-none input-glow font-body"
            />
            
            {/* Priority Select */}
            <div className="relative">
              <select
                value={newTaskPriority}
                onChange={(e) => setNewTaskPriority(e.target.value)}
                className="appearance-none bg-white/5 border border-white/10 rounded-xl pl-4 pr-10 py-4 text-white focus:outline-none input-glow font-body cursor-pointer min-w-[140px]"
              >
                <option value="high" className="bg-gray-900">🔥 High</option>
                <option value="medium" className="bg-gray-900">⚡ Medium</option>
                <option value="low" className="bg-gray-900">🌱 Low</option>
              </select>
              <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                <svg className="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clipRule="evenodd" />
                </svg>
              </div>
            </div>

            {/* Add Button */}
            <button
              type="submit"
              className="btn-gradient px-8 py-4 rounded-xl text-white font-semibold flex items-center gap-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Add Task
            </button>
          </div>
        </motion.form>

        {/* Filter Tabs */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="flex gap-2 mb-6"
        >
          {['all', 'pending', 'completed'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg font-medium capitalize transition-all ${
                filter === f
                  ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`}
            >
              {f}
            </button>
          ))}
        </motion.div>

        {/* Task List */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="space-y-3"
        >
          <AnimatePresence mode="popLayout">
            {filteredTasks.length > 0 ? (
              filteredTasks.map((task) => (
                <TaskItem
                  key={task.id}
                  task={task}
                  onToggle={handleToggleTask}
                  onDelete={handleDeleteTask}
                />
              ))
            ) : (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="glass-dark rounded-2xl p-12 text-center"
              >
                <span className="text-6xl mb-4 block">
                  {filter === 'completed' ? '🎯' : filter === 'pending' ? '✨' : '📝'}
                </span>
                <p className="text-gray-400 text-lg">
                  {filter === 'completed' 
                    ? 'No completed tasks yet. Keep going!'
                    : filter === 'pending'
                    ? 'No pending tasks. All done!'
                    : 'No tasks yet. Add your first task above!'}
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* Footer */}
        <motion.footer 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 text-center text-gray-500 text-sm"
        >
          <p>Built with 💚 using FastAPI & React</p>
        </motion.footer>
      </div>
    </div>
  )
}

export default App

