import time
import pandas as pd
import datetime as dt
import pathlib

def main():
    while True:
        try:
            # pick the most-recent signal file
            sig_path = max(pathlib.Path("data").glob("*signals*.csv"))
        except ValueError:          # none found yet
            time.sleep(60)
            continue

        # TODO: read latest row, run Backtrader or broker orders here

        # append placeholder equity to monitor CSV
        pd.DataFrame(
            {"ts": [dt.datetime.utcnow()], "eq": [0]}
        ).to_csv("data/pnl.csv", mode="a", header=False, index=False)

        time.sleep(60)              # wait 1 min

if __name__ == "__main__":
    main()
