const data = {
  charts: {
    skills_match: {
      type: "radar",
      title: "Skills Match Analysis",
      labels: ["Matched Skills", "Missing Skills"],
      values: [5, 9],
      metadata: null,
    },
    education_alignment: {
      type: "pie",
      title: "Education Alignment",
      labels: ["Aligned", "Not Aligned"],
      values: [1, 0],
      metadata: null,
    },
    score_breakdown: {
      type: "bar",
      title: "Score Breakdown",
      labels: [
        "Skills Match",
        "Experience Relevance",
        "Education Alignment",
        "Format & Structure",
        "Keyword Optimization",
      ],
      values: [16, 19, 4, 9, 9],
      metadata: null,
    },
  },
  summary_text:
    "Apoorva Shukla's resume scores 78 out of 100 against the Senior Frontend Engineer role. Skills in JavaScript and React are strong, but important technologies like TypeScript and GraphQL are missing. The candidate's experience exceeds the requirement with over 8 years in relevant roles. Education is aligned, though lacks field specification.",
  improvement_highlights: [
    "Add TypeScript, Next.js, Tailwind CSS or Styled Components, Redux, and other missing skills to the skills section.",
    "Highlight specific projects involving TypeScript and testing frameworks like Jest and Cypress.",
    "Specify field of study in the education section for better clarity.",
    "Add a resume summary to highlight key strengths and career objectives.",
    "Include detailed achievements related to frontend technologies.",
  ],
  timestamp: "2023-10-27T18:35:00Z",
};

// /static/script.js
(() => {
  const form = document.getElementById("analyze-form");
  const btn = document.getElementById("analyze-btn");
  const summaryEl = document.getElementById("summary");
  const chartsEl = document.getElementById("charts-container");

  /** Optional: track charts to destroy them explicitly */
  let chartInstances = [];

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    btn.disabled = true;
    btn.textContent = "Analyzing...";
    summaryEl.textContent = "Processing...";
    chartsEl.innerHTML = "";
    chartInstances.forEach((c) => c?.destroy());
    chartInstances = [];

    try {
      const formData = new FormData(form);

      const res = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Request failed: ${res.status}`);
      }

      const data = await res.json();

      // Safe text rendering
      const summaryText = data?.summary_text ?? "No summary available.";
      const improvements = Array.isArray(data?.improvement_highlights)
        ? data.improvement_highlights
        : [];

      // Build summary safely
      summaryEl.innerHTML = ""; // clear
      const h2 = document.createElement("h2");
      h2.textContent = "Summary";
      const p = document.createElement("p");
      p.textContent = summaryText;
      const h3 = document.createElement("h3");
      h3.textContent = "Improvement Suggestions";
      const ul = document.createElement("ul");
      improvements.forEach((s) => {
        const li = document.createElement("li");
        li.textContent = s;
        ul.appendChild(li);
      });
      const ts = document.createElement("p");
      const tsVal = data?.timestamp ? new Date(data.timestamp) : new Date();
      ts.innerHTML = `<em>Generated at: ${tsVal.toLocaleString()}</em>`;

      summaryEl.append(h2, p, h3, ul, ts);

      // Charts
      const charts =
        data?.charts && typeof data.charts === "object" ? data.charts : {};
      chartsEl.innerHTML = ""; // ensure empty

      Object.entries(charts).forEach(([_, chartData]) => {
        const canvas = document.createElement("canvas");
        chartsEl.appendChild(canvas);

        const type = chartData?.type ?? "bar";
        const labels = Array.isArray(chartData?.labels) ? chartData.labels : [];
        const values = Array.isArray(chartData?.values) ? chartData.values : [];
        const colors =
          chartData?.metadata?.colors ??
          labels.map((_, i) => `hsl(${(i * 47) % 360} 70% 60%)`);
        const title = chartData?.title ?? "Chart";

        const cfg = {
          type,
          data: {
            labels,
            datasets: [
              {
                label: title,
                data: values,
                backgroundColor: colors,
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: { display: true },
              title: { display: true, text: title },
            },
          },
        };

        const chart = new Chart(canvas, cfg);
        chartInstances.push(chart);
      });
    } catch (err) {
      summaryEl.innerHTML =
        "<p style='color:red'>Error processing request.</p>";
      console.error(err);
    } finally {
      btn.disabled = false;
      btn.textContent = "Analyze";
    }
  });
})();
