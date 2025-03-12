#!/usr/bin/env python

"""
Command-line interface for coral_data.
"""

import argparse
from coral_data.module import generate_coral_d18O, generate_sst_data

def parse_command_line():
    """
    Parses command-line arguments for generating synthetic datasets.
    """
    parser = argparse.ArgumentParser(description="Generate synthetic coral δ¹⁸O or SST datasets.")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Choose which dataset to generate")

    # Coral δ¹⁸O dataset options
    coral_parser = subparsers.add_parser("oxygen_isotopes", help="Generate coral δ¹⁸O dataset")
    coral_parser.add_argument("--core_depth", type=int, default=100, help="Total depth of the coral core in mm (default: 100).")
    coral_parser.add_argument("--temp_trend", type=float, default=-0.02, help="Isotope warming trend per mm (default: -0.02).")
    coral_parser.add_argument("--baseline_d18o", type=float, default=-5, help="Baseline δ¹⁸O value (default: -5).")
    coral_parser.add_argument("--location", type=str, default="Fake Coral Location", help="Location name for labeling (default: 'Fake Coral Location').")
    coral_parser.add_argument("--filename", type=str, default="simulated_d18o_dataset.csv", help="Output CSV filename (default: 'simulated_d18o_dataset.csv').")

    # SST dataset options
    sst_parser = subparsers.add_parser("sst", help="Generate SST dataset")
    sst_parser.add_argument("--years", type=int, default=20, help="Number of years of SST data (default: 20).")
    sst_parser.add_argument("--warming_trend", type=float, default=0.02, help="Temperature increase per year in °C (default: 0.02).")
    sst_parser.add_argument("--start_temp", type=float, default=28, help="Starting average SST in °C (default: 28).")
    sst_parser.add_argument("--location", type=str, default="Fake Coral Location", help="Location name for labeling (default: 'Fake Coral Location').")
    sst_parser.add_argument("--filename", type=str, default="simulated_sst_dataset.csv", help="Output CSV filename (default: 'simulated_sst_dataset.csv').")

    return parser.parse_args()

def main():
    """
    Main function to process arguments and call the appropriate function.
    """
    args = parse_command_line()
    
    if args.command == "oxygen_isotopes":
        generate_coral_d18O(
            core_depth=args.core_depth,
            temp_trend=args.temp_trend,
            baseline_d18o=args.baseline_d18o,
            location=args.location,
            filename=args.filename
        )
    elif args.command == "sst":
        generate_sst_data(
            years=args.years,
            warming_trend=args.warming_trend,
            start_temp=args.start_temp,
            location=args.location,
            filename=args.filename
        )

if __name__ == "__main__":
    main()
