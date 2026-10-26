# AI_Assisted_Data_Analyst

An AI-assisted data analysis application that lets users ask questions about a dataset in natural language and receive answers grounded in actual SQL query results.

## Project objectives

- Load and inspect CSV datasets using Pandas.
- Store analytical data in SQLite.
- Convert natural-language questions into SQL using an LLM.
- Validate generated SQL before execution.
- Execute safe, read-only queries.
- Display query results and explain findings in plain English.
- Build a simple interface using Streamlit.
- Test critical components using Pytest.

## Technology stack

- Python
- Pandas
- SQLite
- LLM API (provider to be selected)
- Streamlit
- Pytest
- Git and GitHub

## Project status

Currently in Day 1: environment setup and project structure.

## Planned workflow

CSV dataset → Data inspection → SQLite → Natural-language question → SQL generation → SQL validation → Query execution → Results and explanation.

## Security

API keys and other secrets must remain in local environment variables or `.env`. Never commit real credentials to GitHub.

## Development

The application is being built incrementally, with each component tested before the next milestone.