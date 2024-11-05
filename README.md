# data_quality_project

## Directory Structure
- src/: Source code
- scripts/: PowerShell scripts
- config/: Configuration files
- data/: Data directories
  - input/: Input CSV files
  - output/: Cleaned data
  - eports/: Quality reports
- 	ests/: Test files
- docker/: Docker-related files

## Setup
1. Install dependencies:
`powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r docker/requirements.txt
`

2. Run the pipeline:
`powershell
cd scripts
.\data_quality_pipeline.ps1 -InputCsvPath "../data/input/your_data.csv"
`

3. Build and run with Docker:
`powershell
docker build -t data-quality-checker -f docker/Dockerfile .
docker run -v D:\VSCODE\Data_splitting_train_test/data:/app/data data-quality-checker -InputCsvPath "/app/data/input/your_data.csv"
`
