#!/usr/bin/env python

"""
Command-line interface for coral_data.
"""

import argparse
from coral_data.module import generate_coral_d18O, generate_sst_data

def parse_command_line():
    """
    Parses command-line arguments for generating both synthetic coral δ¹⁸O and SST datasets.
    """
    parser = argparse.ArgumentParser(description="Generate synthetic coral δ¹⁸O and SST datasets.")

    # Coral options
    parser.add_argument("--core_depth", type=int, default=100)
    parser.add_argument("--temp_trend", type=float, default=-0.02)
    parser.add_argument("--baseline_d18o", type=float, default=-5)
    parser.add_argument("--d18o_filename", type=str, default="simulated_d18o_dataset.csv")

    # SST options
    parser.add_argument("--years", type=int, default=20)
    parser.add_argument("--warming_trend", type=float, default=0.02)
    parser.add_argument("--start_temp", type=float, default=28)
    parser.add_argument("--sst_filename", type=str, default="simulated_sst_dataset.csv")

    # Shared argument between the two
    parser.add_argument("--location", type=str, default="Fake Coral Location")

    return parser.parse_args()

def main():
    args = parse_command_line()

    generate_coral_d18O(
        core_depth=args.core_depth,
        temp_trend=args.temp_trend,
        baseline_d18o=args.baseline_d18o,
        location=args.location,
        filename=args.d18o_filename
    )

    generate_sst_data(
        years=args.years,
        warming_trend=args.warming_trend,
        start_temp=args.start_temp,
        location=args.location,
        filename=args.sst_filename
    )

if __name__ == "__main__":
    main()
