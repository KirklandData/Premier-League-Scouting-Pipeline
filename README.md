# Premier League Match Finder Pipeline

This is an automated data pipeline built to help football scouts, club managers, and match analysts look at clean team statistics easily. The system downloads messy match logs from the web, runs them through cleaning steps inside a local database filing cabinet, and displays the outcomes clearly on a web dashboard screen.

## What I built and who it is for
I built this project for football scouts who need reliable match numbers without dealing with chaotic, broken data sheets. 

The software goes out to the web, fetches raw match logs, checks for missing data points, and fixes them automatically. It then loads the clean results into an interactive web screen with simple dropdown filters so users can check scoring statistics, track crowd sizes, or spot high-scoring matches instantly.

## How the data moves (Step-by-Step)
Instead of putting all my code into one massive file, I built this pipeline like a clean professional kitchen with separate work areas:

1. **The Ingestion Station** (*extract/fetch_fixtures.py*): This is written in Python. Its only job is to drive out to the internet API, copy the raw match details exactly as they are written, and save a backup copy in our raw storage folder as a JSON file.
2. **The Cleaning Engine** (*sql/ folder*): Once the raw file is downloaded, a database tool called **DuckDB** reads the data and runs three separate SQL filters in order:
   - **Table Set up** (*01_raw.sql*): Reads the raw text layout and formats it into a neat table grid with rows and columns.
   - **The Quality Filter** (*02_staging.sql*): This is our main cleanup gate. If a match is completely missing its score lines, it throws the whole row away because an incomplete report is useless. If a box like stadium attendance is left blank, it automatically drops a backup '0' in the box so it does not break our math equations later on.
   - **The Scout Summary Mart** (*03_marts.sql*): This checks the table for duplicate entries, matches up columns, and engineers useful check-boxes, like highlighting matches that had 4 or more goals.
3. **The Quality Inspector** (*tests/test_pipeline.py*): Before the data is allowed out, this script checks our tables to ensure no blank numbers or negative fields accidentally leaked through our system.
4. **The Display Counter** (*app/scouting_app.py*): This uses a tool called **Streamlit** to read the clean database tables and draw the bar charts and grids directly on a web page screen.

**Safe Re-runs (Idempotency):** Every time you run the master pipeline script (`python run_models.py`), the database completely wipes the old tables and builds them brand new from the original raw download file. This means you can run the pipeline a hundred times in a row and it will always give you the exact same clean results without cluttering or doubling the rows.

## How to run the system
```bash
# 1. Download this project folder from GitHub
git clone https://github.com && cd premier-league-scouting-pipeline

# 2. Install the necessary packages
pip install -r requirements.txt

# 3. Ingest the data and run the database cleaning models
python run_models.py

# 4. Run the automated data quality checks
python -m pytest tests/

# 5. Launch the web dashboard screen on your browser
streamlit run app/scouting_app.py
```

## Future Upgrades
- **Automatic Cloud Timers:** Schedule the pipeline to wake up and run by itself every Sunday at midnight so the data stays fresh without human intervention.
- **Leagues Dropdown:** Add a menu to allow scouts to switch between English Premier League, Spanish La Liga, or World Cup match sets without editing the underlying code templates.

## Where AI helped
In compliance with the Data School guidelines, I used an AI assistant as a pair-programmer to write this code. Specifically, the AI helped me draft the precise file-path text syntax needed for DuckDB to locate and parse raw JSON text strings, and helped generate the template structures for our testing files (`pytest`). All core architectural logic paths—such as choosing football data, setting up the three cleaning layers, choosing to drop null scores, and designing the total goals metric—were completely directed, validated, and finalized by myself.
