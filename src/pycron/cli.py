# This file is used to run the CLI for the pycron package
import argparse

def run():
    parser = argparse.ArgumentParser(description="A simple cron job scheduler")
    parser.add_argument("-c", "--cmd", help="Command to run")
    parser.add_argument("-t", "--time", help="Cron time")
    args = parser.parse_args()

    cmd = args.cmd
    time = args.time

    # Add to the crontab
    # Once trigger, collect the data and update the data


    