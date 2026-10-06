import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  ArrowRight,
  BookOpen,
  Brain,
  Building2,
  ChevronRight,
  CircleHelp,
  Database,
  GraduationCap,
  LoaderCircle,
  MessageSquare,
  Network,
  RefreshCw,
  Search,
  Send,
  Sparkles,
  Users,
  X,
  Zap,
} from "lucide-react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const suggestions = [
  "Which branches does the college offer?",
  "What subjects does Rajendra teach?",
  "Who teaches Artificial Intelligence?",
  "What is the prerequisite for Machine Learning?",
  "Tell me about Artificial Intelligence",
  "Which subjects are in B.Tech Information Technology?",
  "Tell me about student 53",
];

function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! I am the College Ontology AI Assistant. Ask me about departments, subjects, faculty, students, courses, prerequisites, or subject details.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [backendOnline, setBackendOnline] = useState(false);

  const [dashboardOpen, setDashboardOpen] = useState(false);

  const [stats, setStats] = useState(null);
  const [statsLoading, setStatsLoading] = useState(false);
  const [statsError, setStatsError] = useState("");

  const [graph, setGraph] = useState(null);
  const [graphLoading, setGraphLoading] = useState(false);
  const [graphError, setGraphError] = useState("");

  const [reasoning, setReasoning] = useState(null);
  const [reasoningLoading, setReasoningLoading] = useState(false);
  const [reasoningError, setReasoningError] = useState("");

  const [graphSearch, setGraphSearch] = useState("");
  const [selectedNode, setSelectedNode] = useState(null);

  useEffect(() => {
    checkBackend();
  }, []);

  async function checkBackend() {
    try {
      const response = await fetch(`${API_URL}/health`);
      setBackendOnline(response.ok);
    } catch {
      setBackendOnline(false);
    }
  }

  async function loadStats() {
    setStatsLoading(true);
    setStatsError("");

    try {
      const response = await fetch(`${API_URL}/stats`);

      if (!response.ok) {
        throw new Error("Unable to load ontology statistics.");
      }

      const data = await response.json();
      setStats(data);
    } catch (error) {
      setStatsError(error.message);
    } finally {
      setStatsLoading(false);
    }
  }

  async function loadGraph() {
    setGraphLoading(true);
    setGraphError("");

    try {
      const response = await fetch(`${API_URL}/graph`);

      if (!response.ok) {
        throw new Error("Unable to load knowledge graph.");
      }

      const data = await response.json();
      setGraph(data);
    } catch (error) {
      setGraphError(error.message);
    } finally {
      setGraphLoading(false);
    }
  }

  async function loadReasoning() {
    setReasoningLoading(true);
    setReasoningError("");

    try {
      const response = await fetch(`${API_URL}/reasoning`);

      if (!response.ok) {
        throw new Error("Unable to load OWL-RL reasoning information.");
      }

      const data = await response.json();
      setReasoning(data);
    } catch (error) {
      setReasoningError(error.message);
    } finally {
      setReasoningLoading(false);
    }
  }

  async function openDashboard() {
    setDashboardOpen(true);

    await Promise.all([
      loadStats(),
      loadGraph(),
      loadReasoning(),
    ]);
  }

  async function askQuestion(questionOverride = null) {
    const question = (questionOverride ?? input).trim();

    if (!question || loading) {
      return;
    }

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: question,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
        }),
      });

      if (!response.ok) {
        throw new Error("The backend could not process the question.");
      }

      const data = await response.json();

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: data.answer,
          type: data.type,
          data: data.data,
        },
      ]);

      setBackendOnline(true);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            "I could not connect to the backend. Please make sure FastAPI is running on port 8000.",
          type: "error",
        },
      ]);

      setBackendOnline(false);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    askQuestion();
  }

  function clearChat() {
    setMessages([
      {
        role: "assistant",
        content:
          "Chat cleared. Ask me another question about the college knowledge graph.",
      },
    ]);
  }

  const filteredNodes = useMemo(() => {
    if (!graph?.nodes) {
      return [];
    }

    const query = graphSearch.trim().toLowerCase();

    if (!query) {
      return graph.nodes;
    }

    return graph.nodes.filter((node) =>
      node.label.toLowerCase().includes(query)
    );
  }, [graph, graphSearch]);

  const selectedEdges = useMemo(() => {
    if (!selectedNode || !graph?.edges) {
      return [];
    }

    return graph.edges.filter(
      (edge) =>
        edge.source === selectedNode.id ||
        edge.target === selectedNode.id
    );
  }, [graph, selectedNode]);

  const reasoningStats = reasoning
    ? {
        before: reasoning.before_reasoning ?? 0,
        after: reasoning.after_reasoning ?? 0,
        inferred: reasoning.inferred_triples ?? 0,
      }
    : null;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Brain size={22} />
          </div>

          <div>
            <h1>College AI</h1>
            <span>Ontology Assistant</span>
          </div>
        </div>

        <div className="sidebar-status">
          <span
            className={`status-dot ${
              backendOnline ? "online" : "offline"
            }`}
          />

          {backendOnline ? "Backend connected" : "Backend offline"}
        </div>

        <nav className="sidebar-nav">
          <button className="nav-item active">
            <MessageSquare size={18} />
            <span>AI Assistant</span>
          </button>

          <button className="nav-item" onClick={openDashboard}>
            <Network size={18} />
            <span>Knowledge Graph</span>
          </button>

          <button className="nav-item" onClick={openDashboard}>
            <Zap size={18} />
            <span>OWL-RL Reasoning</span>
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-project">
            <Sparkles size={17} />
            <div>
              <strong>Ontology Project</strong>
              <span>RDF + SPARQL + OWL-RL</span>
            </div>
          </div>

          <button className="clear-button" onClick={clearChat}>
            <RefreshCw size={16} />
            Clear conversation
          </button>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">COLLEGE KNOWLEDGE SYSTEM</p>
            <h2>College Ontology AI Assistant</h2>
          </div>

          <div className="topbar-actions">
            <div className="connection-badge">
              <span
                className={`status-dot ${
                  backendOnline ? "online" : "offline"
                }`}
              />
              {backendOnline ? "Online" : "Offline"}
            </div>

            <button className="dashboard-button" onClick={openDashboard}>
              <Network size={17} />
              Explore Knowledge Graph
            </button>
          </div>
        </header>

        <section className="chat-section">
          <div className="chat-header">
            <div className="chat-title">
              <div className="assistant-avatar">
                <Brain size={22} />
              </div>

              <div>
                <h3>Ontology Assistant</h3>
                <p>Ask questions using natural language</p>
              </div>
            </div>

            <div className="technology-pills">
              <span>RDF</span>
              <span>SPARQL</span>
              <span>OWL-RL</span>
            </div>
          </div>

          <div className="messages-area">
            {messages.map((message, index) => (
              <div
                key={`${message.role}-${index}`}
                className={`message-row ${message.role}`}
              >
                {message.role === "assistant" && (
                  <div className="message-avatar">
                    <Brain size={17} />
                  </div>
                )}

                <div
                  className={`message-bubble ${
                    message.role === "assistant"
                      ? "assistant-bubble"
                      : "user-bubble"
                  }`}
                >
                  <p>{message.content}</p>

                </div>
              </div>
            ))}

            {loading && (
              <div className="message-row assistant">
                <div className="message-avatar">
                  <Brain size={17} />
                </div>

                <div className="message-bubble assistant-bubble loading-bubble">
                  <LoaderCircle className="spin" size={18} />
                  <span>Querying ontology...</span>
                </div>
              </div>
            )}
          </div>

          <div className="suggestions-section">
            <div className="suggestions-heading">
              <CircleHelp size={15} />
              Try asking
            </div>

            <div className="suggestions-list">
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  className="suggestion-chip"
                  onClick={() => askQuestion(suggestion)}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>

          <form className="chat-input-area" onSubmit={handleSubmit}>
            <div className="input-wrapper">
              <MessageSquare size={19} />

              <input
                type="text"
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder="Ask something about the college..."
                disabled={loading}
              />

              <button
                type="submit"
                className="send-button"
                disabled={loading || !input.trim()}
                aria-label="Send question"
              >
                <Send size={18} />
              </button>
            </div>
          </form>
        </section>
      </main>

      {dashboardOpen && (
        <div
          className="dashboard-overlay"
          onClick={() => setDashboardOpen(false)}
        >
          <div
            className="dashboard-modal"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="dashboard-header">
              <div>
                <p className="eyebrow">SEMANTIC KNOWLEDGE SYSTEM</p>
                <h2>Knowledge Graph Dashboard</h2>
                <p>
                  Explore RDF entities, relationships and OWL-RL reasoning.
                </p>
              </div>

              <button
                className="close-dashboard"
                onClick={() => setDashboardOpen(false)}
              >
                <X size={20} />
              </button>
            </div>

            <div className="dashboard-content">
              <section className="dashboard-section">
                <div className="section-heading">
                  <div>
                    <h3>Ontology Statistics</h3>
                    <p>Live information from the FastAPI backend.</p>
                  </div>

                  <button
                    className="refresh-button"
                    onClick={() => {
                      loadStats();
                      loadReasoning();
                    }}
                  >
                    <RefreshCw
                      size={15}
                      className={
                        statsLoading || reasoningLoading
                          ? "spin"
                          : ""
                      }
                    />
                    Refresh
                  </button>
                </div>

                {statsError && (
                  <div className="error-card">{statsError}</div>
                )}

                <div className="stats-grid">
                  <div className="stat-card">
                    <div className="stat-icon">
                      <Database size={20} />
                    </div>

                    <div>
                      <span>RDF Triples</span>
                      <strong>
                        {statsLoading ? "..." : stats?.knowledge_graph?.triples ?? "—"}
                      </strong>
                    </div>
                  </div>

                  <div className="stat-card">
                    <div className="stat-icon">
                      <Network size={20} />
                    </div>

                    <div>
                      <span>Reasoned Triples</span>
                      <strong>
                        {statsLoading
                          ? "..."
                          : stats?.knowledge_graph?.reasoned_triples ?? "—"}
                      </strong>
                    </div>
                  </div>

                  <div className="stat-card highlight">
                    <div className="stat-icon">
                      <Zap size={20} />
                    </div>

                    <div>
                      <span>Inferred Triples</span>
                      <strong>
                        {statsLoading
                          ? "..."
                          : stats?.knowledge_graph?.inferred_triples ?? "—"}
                      </strong>
                    </div>
                  </div>
                </div>
              </section>

              <section className="dashboard-section">
                <div className="section-heading">
                  <div>
                    <h3>Knowledge Base Entities</h3>
                    <p>
                      Main entities currently represented in the ontology.
                    </p>
                  </div>
                </div>

                <div className="entity-grid">
                  <div className="entity-card">
                    <Building2 size={20} />
                    <div>
                      <span>Departments</span>
                      <strong>
                        {stats?.entities?.departments ?? "—"}
                      </strong>
                    </div>
                  </div>

                  <div className="entity-card">
                    <BookOpen size={20} />
                    <div>
                      <span>Subjects</span>
                      <strong>
                        {stats?.entities?.subjects ?? "—"}
                      </strong>
                    </div>
                  </div>

                  <div className="entity-card">
                    <Users size={20} />
                    <div>
                      <span>Faculty</span>
                      <strong>
                        {stats?.entities?.faculty ?? "—"}
                      </strong>
                    </div>
                  </div>

                  <div className="entity-card">
                    <GraduationCap size={20} />
                    <div>
                      <span>Students</span>
                      <strong>
                        {stats?.entities?.students ?? "—"}
                      </strong>
                    </div>
                  </div>

                  <div className="entity-card">
                    <BookOpen size={20} />
                    <div>
                      <span>Courses</span>
                      <strong>
                        {stats?.entities?.courses ?? "—"}
                      </strong>
                    </div>
                  </div>
                </div>
              </section>

              <section className="dashboard-section reasoning-lab">
                <div className="section-heading">
                  <div>
                    <div className="section-title-with-icon">
                      <Zap size={20} />
                      <h3>OWL-RL Reasoning Lab</h3>
                    </div>

                    <p>
                      Visualize how semantic reasoning expands the knowledge
                      graph.
                    </p>
                  </div>

                  <span className="engine-badge">
                    {reasoning?.reasoning_engine || "OWL-RL"}
                  </span>
                </div>

                {reasoningError && (
                  <div className="error-card">{reasoningError}</div>
                )}

                {reasoningLoading && !reasoning ? (
                  <div className="reasoning-loading">
                    <LoaderCircle className="spin" size={22} />
                    Loading reasoning results...
                  </div>
                ) : (
                  <>
                    <div className="reasoning-flow">
                      <div className="reasoning-box">
                        <span>Original RDF</span>
                        <strong>
                          {reasoningStats?.before ?? "—"}
                        </strong>
                        <small>triples</small>
                      </div>

                      <div className="reasoning-arrow">
                        <ArrowRight size={25} />
                        <span>OWL-RL</span>
                      </div>

                      <div className="reasoning-box">
                        <span>Reasoned Graph</span>
                        <strong>
                          {reasoningStats?.after ?? "—"}
                        </strong>
                        <small>triples</small>
                      </div>

                      <div className="reasoning-arrow plus-arrow">
                        <span>+</span>
                      </div>

                      <div className="reasoning-box inferred">
                        <span>Additional Triples</span>
                        <strong>
                          +{reasoningStats?.inferred ?? "—"}
                        </strong>
                        <small>inferred</small>
                      </div>
                    </div>

                    <div className="reasoning-explanation">
                      <div className="explanation-icon">
                        <Brain size={21} />
                      </div>

                      <div>
                        <h4>What is happening here?</h4>

                        <p>
                          The original ontology and college data contain{" "}
                          <strong>
                            {reasoningStats?.before ?? 268}
                          </strong>{" "}
                          RDF triples. OWL-RL reasoning applies semantic
                          rules to that graph and expands it to{" "}
                          <strong>
                            {reasoningStats?.after ?? 731}
                          </strong>{" "}
                          triples.
                        </p>

                        <p>
                          That means the reasoner produced{" "}
                          <strong>
                            {reasoningStats?.inferred ?? 463}
                          </strong>{" "}
                          additional semantic facts. These inferred facts
                          allow the system to understand relationships and
                          types that are logically derivable from the ontology.
                        </p>
                      </div>
                    </div>

                    <div className="reasoning-note">
                      <strong>Important for your viva:</strong>
                      <span>
                        The +463 figure is the difference between the graph
                        size before and after OWL-RL expansion. It should not
                        automatically be described as 463 new college
                        relationships.
                      </span>
                    </div>
                  </>
                )}
              </section>

              <section className="dashboard-section">
                <div className="section-heading">
                  <div>
                    <h3>RDF Relationship Explorer</h3>
                    <p>
                      Select an entity to inspect its graph relationships.
                    </p>
                  </div>

                  <button
                    className="refresh-button"
                    onClick={loadGraph}
                  >
                    <RefreshCw
                      size={15}
                      className={graphLoading ? "spin" : ""}
                    />
                    Reload graph
                  </button>
                </div>

                {graphError && (
                  <div className="error-card">{graphError}</div>
                )}

                <div className="graph-toolbar">
                  <div className="graph-search">
                    <Search size={17} />

                    <input
                      type="text"
                      value={graphSearch}
                      onChange={(event) =>
                        setGraphSearch(event.target.value)
                      }
                      placeholder="Search entities..."
                    />
                  </div>

                  <span className="graph-count">
                    {filteredNodes.length} entities
                  </span>
                </div>

                <div className="graph-explorer">
                  <div className="graph-node-list">
                    {graphLoading ? (
                      <div className="graph-loading">
                        <LoaderCircle className="spin" size={22} />
                        Loading graph...
                      </div>
                    ) : filteredNodes.length === 0 ? (
                      <div className="graph-empty">
                        No matching entities.
                      </div>
                    ) : (
                      filteredNodes.map((node) => (
                        <button
                          key={node.id}
                          className={`graph-node ${
                            selectedNode?.id === node.id
                              ? "selected"
                              : ""
                          }`}
                          onClick={() => setSelectedNode(node)}
                        >
                          <div className="graph-node-icon">
                            <Network size={16} />
                          </div>

                          <div>
                            <strong>{node.label}</strong>
                            <span>{node.type || "Entity"}</span>
                          </div>

                          <ChevronRight size={16} />
                        </button>
                      ))
                    )}
                  </div>

                  <div className="graph-details">
                    {selectedNode ? (
                      <>
                        <div className="selected-node-header">
                          <div className="selected-node-icon">
                            <Network size={22} />
                          </div>

                          <div>
                            <span>Selected entity</span>
                            <h4>{selectedNode.label}</h4>
                          </div>
                        </div>

                        <div className="selected-node-meta">
                          <div>
                            <span>Type</span>
                            <strong>
                              {selectedNode.type || "Entity"}
                            </strong>
                          </div>

                          <div>
                            <span>Relationships</span>
                            <strong>{selectedEdges.length}</strong>
                          </div>
                        </div>

                        <div className="relationship-list">
                          <h4>RDF Relationships</h4>

                          {selectedEdges.length === 0 ? (
                            <p className="muted-text">
                              No relationships found.
                            </p>
                          ) : (
                            selectedEdges.map((edge, index) => {
                              const isSource =
                                edge.source === selectedNode.id;

                              return (
                                <div
                                  className="relationship-item"
                                  key={`${edge.source}-${edge.target}-${index}`}
                                >
                                  <span>
                                    {isSource
                                      ? selectedNode.label
                                      : edge.source_label}
                                  </span>

                                  <div className="relationship-predicate">
                                    <ArrowRight size={14} />
                                    <strong>
                                      {edge.predicate_label}
                                    </strong>
                                  </div>

                                  <span>
                                    {isSource
                                      ? edge.target_label
                                      : selectedNode.label}
                                  </span>
                                </div>
                              );
                            })
                          )}
                        </div>
                      </>
                    ) : (
                      <div className="graph-placeholder">
                        <Network size={42} />
                        <h4>Select an entity</h4>
                        <p>
                          Choose an entity from the list to explore its RDF
                          relationships.
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </section>

              <section className="dashboard-section semantic-section">
                <div className="section-heading">
                  <div>
                    <h3>Semantic Relationship Map</h3>
                    <p>
                      High-level view of how ontology entities connect.
                    </p>
                  </div>
                </div>

                <div className="semantic-map">
                  <div className="semantic-center">
                    <Brain size={25} />
                    <span>College Ontology</span>
                  </div>

                  <div className="semantic-node node-department">
                    <Building2 size={18} />
                    <span>Departments</span>
                  </div>

                  <div className="semantic-node node-faculty">
                    <Users size={18} />
                    <span>Faculty</span>
                  </div>

                  <div className="semantic-node node-student">
                    <GraduationCap size={18} />
                    <span>Students</span>
                  </div>

                  <div className="semantic-node node-subject">
                    <BookOpen size={18} />
                    <span>Subjects</span>
                  </div>

                  <div className="semantic-node node-course">
                    <Database size={18} />
                    <span>Courses</span>
                  </div>
                </div>
              </section>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;