import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Search, BrainCircuit, ShieldCheck, Globe2, FileText,
  ArrowRight, Loader2, Download
} from "lucide-react";
import "./styles.css";

const API = "http://localhost:8000";

function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function runResearch() {
    if (!query.trim()) return;

    setLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await fetch(`${API}/api/research`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          depth: "balanced",
          max_sources: 8
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Research failed");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function downloadPDF() {
    if (!result) return;
    const response = await fetch(`${API}/api/report/pdf`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(result)
    });
    if (!response.ok) { setError("PDF generation failed"); return; }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "AURA_Research_Report.pdf";
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    window.URL.revokeObjectURL(url);
  }

  async function downloadIEEE() {
  if (!result) return;

  try {
    const response = await fetch(
      `${API}/api/report/ieee-pdf`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(result)
      }
    );

    if (!response.ok) {
      throw new Error("IEEE PDF generation failed");
    }

    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;

    link.download =
      "AURA_IEEE_Research_Paper.pdf";

    document.body.appendChild(link);

    link.click();

    link.remove();

    window.URL.revokeObjectURL(url);

  } catch (error) {

    console.error(error);

    setError(
      "Unable to generate IEEE research paper."
    );
  }
}

  const agents = [
    "Planner Agent",
    "Research Agent",
    "Analysis Agent",
    "Verification Agent",
    "Synthesis Agent"
  ];

  return (
    <div className="app">
      <header>
        <div className="brand">
          <div className="logo"><BrainCircuit size={24} /></div>
          <div>
            <b>AURA</b>
            <span>Autonomous Research Intelligence</span>
          </div>
        </div>

        <div className="status">
          <span className="dot" /> Groq Agent Engine
        </div>
      </header>

      <main>
        <section className="hero">
          <div className="eyebrow">MULTI-AGENT RESEARCH SYSTEM</div>

          <h1>
            Turn a question into
            <br />
            <em>verified intelligence.</em>
          </h1>

          <p>
            Plan. Search. Analyze. Verify. Synthesize.
            AURA coordinates specialized AI agents to produce
            research-backed reports.
          </p>

          <div className="searchbox">
            <Search size={20} />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && runResearch()}
              placeholder="Ask a complex research question..."
            />

            <button onClick={runResearch} disabled={loading}>
              {loading ? <Loader2 className="spin" /> : <ArrowRight />}
            </button>
          </div>

          {error && <div className="error">{error}</div>}
        </section>

        {loading && (
          <section className="panel">
            <h2>Agent execution</h2>

            <div className="agents">
              {agents.map((agent, index) => (
                <div className="agent" key={agent}>
                  <div className="agenticon">
                    {index === 3 ? <ShieldCheck /> : <BrainCircuit />}
                  </div>

                  <div>
                    <b>{agent}</b>
                    <small>
                      {index === 0
                        ? "Decomposing research question"
                        : index === 1
                        ? "Collecting evidence"
                        : "Processing..."}
                    </small>
                  </div>

                  <Loader2 className="spin" />
                </div>
              ))}
            </div>
          </section>
        )}

        {result && (
          <section className="results">
            <div className="grid">
              <div className="panel">
                <div className="paneltitle">
                  <BrainCircuit /> Research plan
                </div>

                <ol>
                  {result.plan?.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ol>
              </div>

              <div className="panel">
                <div className="paneltitle">
                  <ShieldCheck /> Confidence
                </div>

                <div className="score">
                  {Math.round((result.confidence || 0) * 100)}
                  <span>%</span>
                </div>

                <small>
                  Based on the verification agent's audit
                </small>
              </div>
            </div>

            <div className="panel">
              <div className="paneltitle">
                <Globe2 /> Sources
                <span className="count">{result.sources?.length}</span>
              </div>

              <div className="sources">
                {result.sources?.map((source, index) => (
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noreferrer"
                    key={index}
                  >
                    <span>{index + 1}</span>
                    <div>
                      <b>{source.title}</b>
                      <small>{source.domain}</small>
                    </div>
                  </a>
                ))}
              </div>
            </div>

            <div className="panel report">
              <div className="reporthead">
                <div className="paneltitle">
                  <FileText /> Final intelligence report
                </div>
                <button className="download" onClick={downloadPDF}>
                <button className="download ieee" onClick={downloadIEEE}>
              IEEE Paper
              </button>
                  <Download size={16} /> Download PDF
                </button>
              </div>

              <pre>{result.final_answer}</pre>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
