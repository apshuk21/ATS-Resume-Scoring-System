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
      //   const charts =
      //     data?.charts && typeof data.charts === "object" ? data.charts : {};
      //   chartsEl.innerHTML = ""; // ensure empty

      //   Object.entries(charts).forEach(([_, chartData]) => {
      //     const canvas = document.createElement("canvas");
      //     chartsEl.appendChild(canvas);

      //     const type = chartData?.type ?? "bar";
      //     const labels = Array.isArray(chartData?.labels) ? chartData.labels : [];
      //     const values = Array.isArray(chartData?.values) ? chartData.values : [];
      //     const colors =
      //       chartData?.metadata?.colors ??
      //       labels.map((_, i) => `hsl(${(i * 47) % 360} 70% 60%)`);
      //     const title = chartData?.title ?? "Chart";

      //     const cfg = {
      //       type,
      //       data: {
      //         labels,
      //         datasets: [
      //           {
      //             label: title,
      //             data: values,
      //             backgroundColor: colors,
      //           },
      //         ],
      //       },
      //       options: {
      //         responsive: true,
      //         plugins: {
      //           legend: { display: true },
      //           title: { display: true, text: title },
      //         },
      //       },
      //     };

      //     const chart = new Chart(canvas, cfg);
      //     chartInstances.push(chart);
      //   });
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
