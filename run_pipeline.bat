@echo off
cd /d "D:\VS CODE\ETL-Analytics-Pipeline"
call venv\Scripts\activate

python -m ingest.run

for /f "usebackq tokens=1,* delims==" %%a in (".env") do set "%%a=%%b"

cd crypto_dbt
dbt run --profiles-dir .
dbt test --profiles-dir .
cd ..