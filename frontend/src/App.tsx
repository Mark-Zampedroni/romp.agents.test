import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import './index.css'

const API_BASE = 'http://localhost:3000/api/v1'

interface Project {
  id: number
  title: string
  description: string
  status: string
  budget: number
  original_scope: string
  current_scope: string
  scope_changes: string
  client_id: number
  created_at: string
}

interface Task {
  id: number
  title: string
  status: string
  project_id: number
}

interface Invoice {
  id: number
  invoice_number: string
  amount: number
  status: string
  client_id: number
}

interface ClientHealth {
  client_id: number
  client_name: string
  health_score: number
  engagement_level: string
  total_interactions: number
  pending_invoices: number
  active_projects: number
}

function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([])
  const [tasks, setTasks] = useState<Task[]>([])
  const [invoices, setInvoices] = useState<Invoice[]>([])
  const [clientHealth, setClientHealth] = useState<ClientHealth[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [projectsRes, tasksRes, invoicesRes] = await Promise.all([
        fetch(`${API_BASE}/projects`),
        fetch(`${API_BASE}/tasks`),
        fetch(`${API_BASE}/invoices`)
      ])
      const projectsData = await projectsRes.json()
      const tasksData = await tasksRes.json()
      const invoicesData = await invoicesRes.json()
      
      setProjects(projectsData)
      setTasks(tasksData)
      setInvoices(invoicesData)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching data:', error)
      setLoading(false)
    }
  }

  if (loading) return <div className="container"><p>Loading...</p></div>

  const totalRevenue = invoices.reduce((sum, inv) => sum + inv.amount, 0)
  const pendingInvoices = invoices.filter(inv => inv.status === 'pending').length
  const activeProjects = projects.filter(p => p.status === 'active').length

  return (
    <div className="container">
      <h1>Freelancer Dashboard</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px', marginBottom: '30px' }}>
        <div className="card">
          <h3>Active Projects</h3>
          <p style={{ fontSize: '32px', fontWeight: 'bold' }}>{activeProjects}</p>
        </div>
        <div className="card">
          <h3>Pending Invoices</h3>
          <p style={{ fontSize: '32px', fontWeight: 'bold' }}>{pendingInvoices}</p>
        </div>
        <div className="card">
          <h3>Total Revenue</h3>
          <p style={{ fontSize: '32px', fontWeight: 'bold' }}>€{totalRevenue.toFixed(2)}</p>
        </div>
      </div>

      <div className="card">
        <h2>Recent Projects</h2>
        {projects.length === 0 ? <p>No projects yet</p> : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ textAlign: 'left', borderBottom: '2px solid #e5e7eb' }}>
                <th style={{ padding: '10px' }}>Title</th>
                <th style={{ padding: '10px' }}>Status</th>
                <th style={{ padding: '10px' }}>Budget</th>
                <th style={{ padding: '10px' }}>Scope Changes</th>
              </tr>
            </thead>
            <tbody>
              {projects.map(project => (
                <tr key={project.id} style={{ borderBottom: '1px solid #e5e7eb' }}>
                  <td style={{ padding: '10px' }}>{project.title}</td>
                  <td style={{ padding: '10px' }}><span className={`badge badge-${project.status}`}>{project.status}</span></td>
                  <td style={{ padding: '10px' }}>€{project.budget?.toFixed(2) || 'N/A'}</td>
                  <td style={{ padding: '10px' }}>{project.scope_changes ? 'Yes' : 'No'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div style={{ marginTop: '20px' }}>
        <Link to="/projects" className="btn">Manage Projects</Link>
        <Link to="/invoices" className="btn btn-secondary" style={{ marginLeft: '10px' }}>Invoices</Link>
        <Link to="/clients" className="btn btn-secondary" style={{ marginLeft: '10px' }}>Clients</Link>
      </div>
    </div>
  )
}

function Projects() {
  const [projects, setProjects] = useState<Project[]>([])
  const [newProject, setNewProject] = useState({ title: '', description: '', budget: '', original_scope: '', client_id: '1' })
  const [showForm, setShowForm] = useState(false)

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    const res = await fetch(`${API_BASE}/projects`)
    const data = await res.json()
    setProjects(data)
  }

  const createProject = async (e: React.FormEvent) => {
    e.preventDefault()
    await fetch(`${API_BASE}/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...newProject,
        budget: parseFloat(newProject.budget) || 0,
        client_id: parseInt(newProject.client_id)
      })
    })
    fetchProjects()
    setShowForm(false)
    setNewProject({ title: '', description: '', budget: '', original_scope: '', client_id: '1' })
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Projects</h1>
        <button className="btn" onClick={() => setShowForm(!showForm)}>+ New Project</button>
      </div>

      {showForm && (
        <div className="card">
          <h3>Create Project</h3>
          <form onSubmit={createProject}>
            <label>Title</label>
            <input value={newProject.title} onChange={e => setNewProject({...newProject, title: e.target.value})} required />
            <label>Description</label>
            <textarea value={newProject.description} onChange={e => setNewProject({...newProject, description: e.target.value})} />
            <label>Budget (EUR)</label>
            <input type="number" value={newProject.budget} onChange={e => setNewProject({...newProject, budget: e.target.value})} />
            <label>Original Scope</label>
            <textarea value={newProject.original_scope} onChange={e => setNewProject({...newProject, original_scope: e.target.value})} required />
            <label>Client ID</label>
            <input type="number" value={newProject.client_id} onChange={e => setNewProject({...newProject, client_id: e.target.value})} />
            <button type="submit" className="btn">Create Project</button>
          </form>
        </div>
      )}

      {projects.map(project => (
        <div key={project.id} className="card">
          <h3>{project.title}</h3>
          <p>{project.description}</p>
          <p><strong>Budget:</strong> €{project.budget?.toFixed(2)}</p>
          <p><strong>Status:</strong> <span className={`badge badge-${project.status}`}>{project.status}</span></p>
          <p><strong>Original Scope:</strong> {project.original_scope}</p>
          <p><strong>Current Scope:</strong> {project.current_scope}</p>
          {project.scope_changes && (
            <div style={{ background: '#fef3c7', padding: '10px', borderRadius: '4px', marginTop: '10px' }}>
              <strong>Scope Changes:</strong>
              <pre style={{ whiteSpace: 'pre-wrap', marginTop: '5px' }}>{project.scope_changes}</pre>
            </div>
          )}
        </div>
      ))}

      <Link to="/" className="btn btn-secondary" style={{ marginTop: '20px', display: 'inline-block' }}>Back to Dashboard</Link>
    </div>
  )
}

function Invoices() {
  const [invoices, setInvoices] = useState<Invoice[]>([])
  const [newInvoice, setNewInvoice] = useState({ amount: '', items: '', project_id: '1', client_id: '1' })
  const [showForm, setShowForm] = useState(false)

  useEffect(() => {
    fetchInvoices()
  }, [])

  const fetchInvoices = async () => {
    const res = await fetch(`${API_BASE}/invoices`)
    const data = await res.json()
    setInvoices(data)
  }

  const createInvoice = async (e: React.FormEvent) => {
    e.preventDefault()
    await fetch(`${API_BASE}/invoices`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...newInvoice,
        amount: parseFloat(newInvoice.amount),
        project_id: parseInt(newInvoice.project_id),
        client_id: parseInt(newInvoice.client_id)
      })
    })
    fetchInvoices()
    setShowForm(false)
    setNewInvoice({ amount: '', items: '', project_id: '1', client_id: '1' })
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Invoices</h1>
        <button className="btn" onClick={() => setShowForm(!showForm)}>+ New Invoice</button>
      </div>

      {showForm && (
        <div className="card">
          <h3>Create Invoice</h3>
          <form onSubmit={createInvoice}>
            <label>Amount (EUR)</label>
            <input type="number" value={newInvoice.amount} onChange={e => setNewInvoice({...newInvoice, amount: e.target.value})} required />
            <label>Items Description</label>
            <textarea value={newInvoice.items} onChange={e => setNewInvoice({...newInvoice, items: e.target.value})} required />
            <label>Project ID</label>
            <input type="number" value={newInvoice.project_id} onChange={e => setNewInvoice({...newInvoice, project_id: e.target.value})} />
            <label>Client ID</label>
            <input type="number" value={newInvoice.client_id} onChange={e => setNewInvoice({...newInvoice, client_id: e.target.value})} />
            <button type="submit" className="btn">Create Invoice</button>
          </form>
        </div>
      )}

      {invoices.map(invoice => (
        <div key={invoice.id} className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <h3>{invoice.invoice_number}</h3>
            <span className={`badge badge-${invoice.status}`}>{invoice.status}</span>
          </div>
          <p><strong>Amount:</strong> €{invoice.amount.toFixed(2)}</p>
          <p><strong>Items:</strong> {invoice.items}</p>
        </div>
      ))}

      <Link to="/" className="btn btn-secondary" style={{ marginTop: '20px', display: 'inline-block' }}>Back to Dashboard</Link>
    </div>
  )
}

function Clients() {
  const [clients, setClients] = useState<ClientHealth[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchClientHealth()
  }, [])

  const fetchClientHealth = async () => {
    try {
      const healthData: ClientHealth[] = []
      for (let clientId = 1; clientId <= 5; clientId++) {
        try {
          const res = await fetch(`${API_BASE}/clients/${clientId}/health`)
          if (res.ok) {
            const data = await res.json()
            healthData.push(data)
          }
        } catch (e) {
          // Client doesn't exist
        }
      }
      setClients(healthData)
      setLoading(false)
    } catch (error) {
      console.error('Error:', error)
      setLoading(false)
    }
  }

  if (loading) return <div className="container"><p>Loading...</p></div>

  return (
    <div className="container">
      <h1>Client Health Scores</h1>
      
      {clients.length === 0 ? <p>No clients yet</p> : (
        clients.map(client => (
          <div key={client.client_id} className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3>{client.client_name}</h3>
              <span className={`health-${client.engagement_level}`} style={{ fontSize: '24px', fontWeight: 'bold' }}>
                {client.health_score}/100
              </span>
            </div>
            <p><strong>Engagement:</strong> {client.engagement_level}</p>
            <p><strong>Total Interactions:</strong> {client.total_interactions}</p>
            <p><strong>Active Projects:</strong> {client.active_projects}</p>
            <p><strong>Pending Invoices:</strong> {client.pending_invoices}</p>
          </div>
        ))
      )}

      <Link to="/" className="btn btn-secondary" style={{ marginTop: '20px', display: 'inline-block' }}>Back to Dashboard</Link>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/invoices" element={<Invoices />} />
        <Route path="/clients" element={<Clients />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
