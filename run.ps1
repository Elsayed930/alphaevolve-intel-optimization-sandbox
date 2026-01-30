$env:PYTHONPATH = "$PSScriptRoot\src"

# Forward args to the runner
python -m ae_sandbox.run @args

# After run, generate a one-page summary markdown for the benchmark report
# Assumes naming convention: run_reports/<benchmark>_report.json
$benchmark = "toy_clustering"

for ($i = 0; $i -lt $args.Count; $i++) {
  if ($args[$i] -eq "--benchmark" -and ($i + 1) -lt $args.Count) {
    $benchmark = $args[$i + 1]
  }
}

$reportPath = "run_reports/$($benchmark)_report.json"
python scripts/summarize_report.py --report $reportPath --out "run_reports/latest_summary.md"
