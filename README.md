# Premier League Match Finder Pipeline

This is an automated data pipeline built to help football scouts, club managers, and match analysts look at clean team statistics easily. The system downloads messy match logs from the web, runs them through cleaning steps inside a local database filing cabinet, and displays the outcomes clearly on a web dashboard screen.

## What I built and who it is for
I built this project for football scouts who need reliable match numbers without dealing with chaotic, broken data sheets. 

The software goes out to the web, fetches raw match logs, checks for missing data points, and fixes them automatically. It then loads the clean results into an interactive web screen with simple dropdown filters so users can check scoring statistics, track crowd sizes, or spot high-scoring matches instantly.

## The data
The project uses the free, open-source football data from the StatsBomb API. It does not require any passwords or API keys to use.

The data starts as a large, messy text file tracking match events. The extraction script goes out to the web, fetches this text file, and saves it safely in our raw folder as a backup file. All the cleaning and sorting is done inside our database tables, not on the website itself.

## How it works
The pipeline uses a lightweight database engine called **DuckDB** to run three separate SQL cleaning layers one after the other. This process is triggered by running `python run_models.py`.

1. **raw_matches** (*sql/01_raw.sql*): This reads the raw text file we downloaded and splits it into a simple grid layout with rows and columns.
2. **staging_matches** (*sql/02_staging.sql*): This acts as our main filter. If a match is completely missing its final scores, the system throws that row away because an incomplete report is useless. If a non-critical box like stadium attendance is left blank, it automatically puts a '0' in the box so it does not break our math calculations later.
3. **mart_scouting_fixtures** (*sql/03_marts.sql*): This is our final, neat summary table. It checks for duplicate records using a counting layout to ensure every match only appears once. It also creates simple tick-boxes, like highlighting matches that had 4 or more goals.

Finally, the **Streamlit app** (*app/scouting_app.py*) reads this clean summary table and draws the bar charts and grids directly on a web page screen.

**Safe Re-runs (Idempotency):** Every time you run the script, it deletes the old tables and builds them brand new from the original raw download file. This means you can run the pipeline a hundred times in a row and it will always give you the exact same clean results without cluttering or doubling the rows.

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

## What I would do next
- **Automatic Cloud Timers:** Schedule the pipeline to wake up and run by itself every Sunday at midnight so the data stays fresh without human intervention.
- **Leagues Dropdown:** Add a menu to allow scouts to switch between English Premier League, Spanish La Liga, or World Cup match sets without editing the underlying code templates.

## Where AI helped
In compliance with the Data School guidelines, I used an AI assistant as a pair-programmer to write this code. Specifically, the AI helped me draft the precise file-path text syntax needed for DuckDB to locate and parse raw JSON text strings, and helped generate the template structures for our testing files (`pytest`). All core architectural decisions—such as choosing football data, setting up the three cleaning layers, choosing to drop null scores, and designing the total goals metric—were completely directed, validated, and finalized by myself.
