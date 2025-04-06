import os

# Set mode and call main
os.environ["PHILQUERY_MODE"] = "embed"

from src.main import main
main()