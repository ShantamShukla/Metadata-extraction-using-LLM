
import sys
import os
import json
import argparse
import logging

from pipeline import process_file

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description="Data Abstraction from Different File Types using LLMs."
    )
    parser.add_argument(
        "--input-file", 
        required=True, 
        help="Path to the input file (text, excel, csv)."
    )

    args = parser.parse_args()
    file_path = args.input_file

    if not os.path.isfile(file_path):
        logger.error(f"File does not exist: {file_path}")
        sys.exit(1)

    # Run the pipeline
    results = process_file(file_path)

    # Print JSON output
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    # Configure logging for the entire application
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    main()