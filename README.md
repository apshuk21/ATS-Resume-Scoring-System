# ATS Resume Scoring System

This project is a modular, agentic AI-powered resume analysis tool designed to evaluate candidate resumes against job descriptions. It scores resumes across multiple dimensions and visualizes the results using dynamic charts. Built for extensibility, clarity, and real-world usability.

## Features

- Multi-agent orchestration using AutoGen GraphFlow
- Resume scoring across skills, experience, education, and formatting
- Structured schema output using Pydantic for strict validation and frontend compatibility
- Dynamic chart rendering with Chart.js (bar, pie, radar)
- Clean, responsive frontend layout with improvement highlights and summary text
- Timestamped analysis for traceability and versioning

## Technologies Used

- Python (FastAPI, AutoGen, Pydantic)
- HTML, CSS, and Vanilla JavaScript
- Chart.js for frontend visualization

## Project Structure

```
├── static/
│   ├── index.html         # Main frontend template
│   ├── style.css          # Responsive chart layout and styling
│   └── script.js          # Chart rendering and form submission logic
├── api/
│   └── main.py            # FastAPI entry point
├── agents/
│   ├── ats_agents.py      # Multi-agent orchestration using AutoGen GraphFlow
│   └── agent_definitions.py  # Individual agent configurations
├── models/
│   ├── visualization_payload_schema.py
│   ├── score_report_schema.py
│   ├── improvement_report_schema.py
│   └── resume_schema.py
├── prompts/
│   └── prompts_library.py # System prompts for agents
└── README.md
```

## How It Works

1. **User Uploads Resume**: Via a form on the frontend.
2. **Agentic Analysis**: AutoGen GraphFlow orchestrates multiple agents:
   - Resume Processing Agent
   - Job Description Agent
   - Scoring Agent
   - Improvement Agent
   - Visualization Agent
3. **Schema Validation**: Output is validated against strict Pydantic models.
4. **Frontend Rendering**: Summary text and charts are rendered dynamically using Chart.js.
5. **Improvement Highlights**: Actionable suggestions are displayed for the user.

## Chart Types Supported

- `bar`: Score breakdown across dimensions
- `pie`: Binary alignment (e.g., education)
- `radar`: Comparative skill match analysis

Note: `gauge` charts are simulated using doughnut charts if needed.

## Setup Instructions

1. Clone the repository:

   ```
   git clone https://github.com/apshuk21/ATS-Resume-Scoring-System.git
   cd ATS-Resume-Scoring-System
   ```

2. Create a virtual environment and install dependencies:

   ```
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:

   ```
   uvicorn api.main:app --reload
   ```

4. Open `http://localhost:8000` in your browser.

## Future Enhancements

- Agent trace visualizer for debugging and transparency
- Tabbed interface for multi-resume comparison
- Heatmap or gauge-style scoring visualization
- PDF export of analysis report
- Integration with job boards or LinkedIn profiles

## License

MIT License. See `LICENSE` file for details.
