import sys
import os

# Ensure project root is in sys.path so "src" and "pipeline" can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from pipeline.pipeline import SemiconductorProductRecommendationPipeline

def main():
    # Initialize the pipeline (this will log each step via logger in pipeline.py)
    pipeline = SemiconductorProductRecommendationPipeline()

    # Test a sample query
    query = "low-power MCU with Bluetooth 5.0"
    result = pipeline.recommend(query)

    # Print results (logs will already show progress)
    print("\n--- Recommendation Result ---")
    print(result)

if __name__ == "__main__":
    main()
