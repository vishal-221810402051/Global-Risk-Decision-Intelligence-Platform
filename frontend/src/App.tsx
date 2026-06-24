import { useEffect, useState } from "react";

import { fetchHealth } from "./api/health";
import type { HealthResponse } from "./types/health";

const fallbackCountries = ["India", "France", "Kenya"];
const fallbackSectors = ["Agriculture", "Energy"];

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHealth()
      .then((data) => {
        setHealth(data);
        setError(null);
      })
      .catch(() => {
        setHealth(null);
        setError("Backend is offline or unreachable.");
      });
  }, []);

  const countries = health?.mvp_countries ?? fallbackCountries;
  const sectors = health?.mvp_sectors ?? fallbackSectors;

  return (
    <main className="app-shell">
      <section className="intro">
        <p className="eyebrow">Phase 1 Foundation</p>
        <h1>Global Risk Decision Intelligence Platform</h1>
        <p className="summary">
          A base application shell for turning climate, agriculture, and energy
          signals into decision-ready operational alerts.
        </p>
      </section>

      <section className="status-grid" aria-label="Project status">
        <article className="panel">
          <span className="label">Current phase</span>
          <strong>{health?.phase ?? "Phase 1 - Base App Setup"}</strong>
        </article>

        <article className="panel">
          <span className="label">Backend health</span>
          <strong className={health?.status === "ok" ? "healthy" : "offline"}>
            {health?.status ?? "offline"}
          </strong>
          {error ? <p className="hint">{error}</p> : null}
        </article>
      </section>

      <section className="scope-grid" aria-label="MVP scope">
        <article>
          <span className="label">MVP countries</span>
          <ul>
            {countries.map((country) => (
              <li key={country}>{country}</li>
            ))}
          </ul>
        </article>

        <article>
          <span className="label">MVP sectors</span>
          <ul>
            {sectors.map((sector) => (
              <li key={sector}>{sector}</li>
            ))}
          </ul>
        </article>
      </section>
    </main>
  );
}

export default App;
