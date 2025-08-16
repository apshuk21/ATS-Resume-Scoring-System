# ATS Resume Scoring System

This project is a modular, agentic AI-powered resume analysis tool designed to evaluate candidate resumes against job descriptions. It scores resumes across multiple dimensions and visualizes the results using dynamic charts. Built for extensibility, clarity, and real-world usability.

## Features

- Multi-agent orchestration using AutoGen GraphFlow
- Resume scoring across skills, experience, education, and formatting
- Structured schema output using Pydantic for strict validation and frontend compatibility
- Dynamic chart rendering with Chart.js (bar, pie, radar)
- Clean, responsive frontend layout with improvement highlights and summary text
- Timestamped analysis for traceability and versioning
- Persistent session and agent output storage using PostgreSQL
- Dockerized development environment for consistent setup and deployment

## Technologies Used

- Python (FastAPI, AutoGen, Pydantic)
- HTML, CSS, and Vanilla JavaScript
- Chart.js for frontend visualization
- PostgreSQL for structured data storage
- Docker and Docker Compose for containerized orchestration

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
│   ├── resume_schema.py
│   └── db_models.py       # SQLAlchemy models for session and agent output
├── prompts/
│   └── prompts_library.py # System prompts for agents
├── db.py                  # Database engine and session management
├── docker-compose.yml     # Docker Compose configuration for PostgreSQL
└── README.md
```

## How It Works

1. User Uploads Resume: Via a form on the frontend.
2. Agentic Analysis: AutoGen GraphFlow orchestrates multiple agents:
   - Resume Processing Agent
   - Job Description Agent
   - Scoring Agent
   - Improvement Agent
   - Visualization Agent
3. Schema Validation: Output is validated against strict Pydantic models.
4. Frontend Rendering: Summary text and charts are rendered dynamically using Chart.js.
5. Improvement Highlights: Actionable suggestions are displayed for the user.
6. Data Persistence: Resume text, job description, agent outputs, and metadata are stored in PostgreSQL for caching and traceability.

## Chart Types Supported

- bar: Score breakdown across dimensions
- pie: Binary alignment (e.g., education)
- radar: Comparative skill match analysis

Note: gauge charts are simulated using doughnut charts if needed.

## Setup Instructions

### Local Development

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

4. Open http://localhost:8000 in your browser.

### Docker Setup with PostgreSQL

1. Ensure Docker and Docker Compose are installed.

2. Create a .env file with the following variables:

   ```
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=ats_db
   POSTGRES_PORT=5432
   POSTGRES_HOST=postgres
   ENV=development
   ```

3. Start the containers:

   ```
   docker-compose up --build
   ```

4. FastAPI will auto-create tables in development mode. Data will persist in the postgres_data volume.

5. Access the app at http://localhost:8000.

## Future Enhancements

- Agent trace visualizer for debugging and transparency
- Tabbed interface for multi-resume comparison
- Heatmap or gauge-style scoring visualization
- PDF export of analysis report
- Integration with job boards or LinkedIn profiles
- Admin dashboard for session tracking and analytics

## License

MIT License. See LICENSE file for details.
