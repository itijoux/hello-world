import { useState } from "react";
import { profiles, getExplorationDirections } from "./directions.js";

export default function App() {
  const [profileId, setProfileId] = useState(profiles[0].id);
  const profile = profiles.find((p) => p.id === profileId);
  const directions = getExplorationDirections(profile);

  return (
    <main className="page">
      <header className="header">
        <h1>Future Explorer</h1>
        <p className="subtitle">
          A look at where your current classes might lead — including places you
          haven't thought to look.
        </p>
      </header>

      <section className="selector" aria-label="Choose a student">
        {profiles.map((p) => (
          <button
            key={p.id}
            className={`chip ${p.id === profileId ? "chip--active" : ""}`}
            onClick={() => setProfileId(p.id)}
          >
            {p.name}
          </button>
        ))}
      </section>

      <section className="profile">
        <h2>
          {profile.name}
          <span className="profile-grade">, {profile.grade}</span>
        </h2>
        <p className="profile-note">{profile.note}</p>
        <ul className="classes">
          {profile.classes.map((c) => (
            <li key={c}>{c}</li>
          ))}
        </ul>
      </section>

      <section className="directions">
        <h3 className="directions-title">Directions to explore</h3>
        <div className="cards">
          {directions.map((d) => (
            <article key={d.title} className="card">
              <h4 className="card-title">{d.title}</h4>
              <p className="card-body">{d.connection}</p>
              <p className="card-next">
                <span className="card-next-label">Next step</span>
                {d.nextStep}
              </p>
            </article>
          ))}
        </div>
      </section>

      {/* TODO: let a student star or save directions */}
      {/* TODO: ask a follow-up question on any direction */}
      {/* TODO: let students enter their own classes */}
    </main>
  );
}
