# MLOps Lab 2 – Airflow Pipeline

Lab Assignment 2 for MLOps (IE-7374), Northeastern University.

Based on Airflow_Labs/Lab_1 from the course repo: https://github.com/raminmohammadi/MLOps

## What this project does

This project runs Apache Airflow in Docker and uses it to run a pipeline that finds
the most common keywords in a set of news headlines. The pipeline has four steps that
run in order: load the headlines, clean them, count the keywords, and save the top 10
to an Excel file. The original K-Means clustering pipeline from the course lab is also
included and runs on the same setup.

## Customizations I Made

- Built a new pipeline, `News_Keywords_Pipeline`, in `dags/news_keywords_dag.py`, with
  its functions in `dags/src/news_keywords.py` and its data in `dags/data/headlines.csv`.
- The cleaning step lowercases the headlines, removes punctuation and numbers, and drops
  common filler words like "the" and "of", so only meaningful keywords are counted.
- The final step saves the top 10 keywords and their counts to
  `working_data/top_keywords.xlsx`.
- Upgraded the setup to Airflow 3.3.2. The README in the course repo still uses
  Airflow 2.5.1, but the lab code uses the new Airflow 3 style, so I matched the version
  to the code.
- Added the `working_data` folder to the Docker setup so the Excel output appears on my
  computer, and added `openpyxl` to the packages so Python can write Excel files.
- Turned off Airflow's built-in example pipelines so only the lab pipelines show up.
- Added input checks that stop the pipeline with a clear error if the headlines file is
  missing its column or is empty, and set the pipeline to retry once if a step fails.

## How To Run

1. Install Docker Desktop and make sure it says "Engine running".
2. Clone this repo and open a terminal inside the folder.
3. Create the folders Airflow needs and the user file:
```
   mkdir -p ./logs ./plugins ./config ./working_data
   echo -e "AIRFLOW_UID=$(id -u)" > .env
```
4. Set up the database (this takes a few minutes the first time):
```
   docker compose up airflow-init
```
5. Start Airflow:
```
   docker compose up -d
```
6. Open http://localhost:8080 and log in with username `airflow` and password `airflow`.
7. Turn on `News_Keywords_Pipeline` and click the play button to trigger it.
8. When all four steps are green, open `working_data/top_keywords.xlsx` to see the results.
9. To stop Airflow, run:
```
   docker compose down
```

## What I Learned

I learned that Airflow works like a manager for a pipeline. Each step is a task, and
Airflow runs them in the right order, passes results from one step to the next, and
shows which steps passed or failed. I also learned that version numbers matter a lot.
The same lab can break if the Airflow version does not match the way the code is
written, so checking the code before choosing a version saved me from errors.