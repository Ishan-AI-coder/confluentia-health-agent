# Confluentia Health Agent
This  AI system is designed as a multi-agent framework where different specialized agents collaborate to analyze health-related data and provide actionable insights. Instead of relying on a single AI, the system uses multiple agents (Rachel, Warren, Carla, Advik, Neel, and Ruby), each with a unique area of expertise, and an Orchestrator Agent that decides which expert should handle a given input.

The workflow looks like this:

User Input/Report Upload → A user provides text, CSV, Excel, PDF, or image data.

Orchestrator Routing → The orchestrator determines which specialist agent should process the input.

Agent Processing → The chosen agent analyzes the data based on its role (e.g., biomarker analysis, chart generation, logistics).

Integrated Report → The system combines outputs into a structured, readable report with text, tables, and charts.

This makes the system modular, extensible, and closer to how real-world healthcare involves multiple specialists working together.


## Role of the agents
RachelAgent → General medical insights (broad interpretation of conditions).

WarrenAgent → Lab and diagnostic report analysis (structured data like blood tests, urine tests).

CarlaAgent → Correlations between patient symptoms and biomarkers.

AdvikAgent → Predictive insights on potential health risks.

NeelAgent → Patient relationship management (engagement, satisfaction).

RubyAgent → Logistics handling (appointments, scheduling, follow-ups).

## Use Cases

Healthcare Report Analysis
Input: Upload a blood test report (CSV, PDF, image).
Output: WarrenAgent interprets key biomarkers, highlights abnormalities, and generates a structured table.

Symptom–Biomarker Correlation
Input: "The patient complains of fatigue and headache."
Output: CarlaAgent links symptoms to lab results, identifying possible causes like anemia or dehydration.

Predictive Health Risk Assessment
Input: Historical health data across multiple reports.
Output: AdvikAgent forecasts potential risks (e.g., diabetes, cardiovascular issues).

Patient Engagement Monitoring
Input: "Patient 002 feedback log."
Output: NeelAgent assesses relationship stability (e.g., “critical, client frustrated with lack of short-term results”).

Logistics & Follow-Up Coordination
Input: “What’s the appointment status of Patient 005?”
Output: RubyAgent identifies scheduling conflicts and suggests resolutions.

Integrated Dashboard
The system can display abnormalities, risk percentages, and probable diseases in tables and charts (pie charts, bar graphs, trend lines).




## Features

- Fast dependency installation with `uv`
- Modern Python project structure
- Easy setup and development

## Requirements

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) installed

## Installation

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Development

- Install new dependencies:

    ```bash
    uv pip install <package>
    ```

- Update requirements:

    ```bash
    uv pip freeze > requirements.txt
    ```

## License

MIT

## AI Agents used 
 GOOGLE Gemini model 