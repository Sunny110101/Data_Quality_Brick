# run_data_quality.ps1

$inputPath = "data/input/input.csv"
$outputPath = "data/output/cleaned_data.csv"
$reportPath = "data/reports/quality_report.txt"
$configPath = "config/default_config.yaml"

# PowerShell version of line continuation using backtick (`)
python -m src.data_quality_checker `
    --input-csv $inputPath `
    --output-csv $outputPath `
    --report-path $reportPath `
    --config-path $configPath

Write-Host "Data quality check completed!"
Write-Host "Output saved to: $outputPath"
Write-Host "Report saved to: $reportPath"