const data = {
  charts: {
    skills_match: {
      type: "radar",
      title: "Skills Match Analysis",
      labels: ["Matched Skills", "Missing Skills"],
      values: [5, 9],
      metadata: null,
    },
    experience_relevance: {
      type: "gauge",
      title: "Experience Relevance",
      labels: ["Experience Years"],
      values: [8.42],
      metadata: {
        min: ",",
      },
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
