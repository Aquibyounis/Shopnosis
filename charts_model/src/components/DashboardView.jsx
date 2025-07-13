import React from "react";
import Plot from "react-plotly.js";
import KpiCard from "./KpiCard";

export default function DashboardView({ dashboard }) {
  return (
    <div>
      <h2>KPIs</h2>
      <div style={{ display: "flex", gap: 20, flexWrap: "wrap" }}>
        {dashboard.kpis.map(kpi => (
          <KpiCard key={kpi.id} kpi={kpi} />
        ))}
      </div>
      <h2>Charts</h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(350px, 1fr))",
          gap: 24,
        }}
      >
        {dashboard.charts.map((chart, i) => (
          <div
            key={i}
            style={{
              border: "1px solid #ddd",
              borderRadius: 8,
              padding: 16,
              background: "#fff",
              boxShadow: "0 2px 8px #0001",
            }}
          >
            <h4 style={{ marginTop: 0 }}>{chart.title}</h4>
            <Plot data={chart.data.data} layout={chart.data.layout} config={chart.config} />
          </div>
        ))}
      </div>
      <h2>Recommendations</h2>
      <ul>
        {dashboard.recommendations.map((rec, i) => (
          <li key={i}>
            <b>{rec.title}:</b> {rec.recommendation}
          </li>
        ))}
      </ul>
    </div>
  );
} 