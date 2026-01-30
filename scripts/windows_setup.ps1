# Windows quick setup (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
python -m ae_sandbox.run --benchmark toy_clustering --steps 25
