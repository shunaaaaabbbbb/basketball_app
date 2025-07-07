# Basketball App

This repository contains a simple Streamlit application that visualizes NBA player shot locations using `nba_api`.

## Setup
Install [uv](https://github.com/astral-sh/uv) and create a virtual environment to install the dependencies:
```bash
pip install uv
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Running the app
Launch the Streamlit app:
```
streamlit run shot_chart_app.py
```

Then open the provided local URL in a browser.
