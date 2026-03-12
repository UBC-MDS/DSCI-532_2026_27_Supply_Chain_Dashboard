import pandas as pd
from pathlib import Path

def convert_csv_to_parquet():
    base_dir = Path(__file__).parent.parent
    csv_path = base_dir / "data" / "raw" / "supply_chain_data.csv"
    parquet_path = base_dir / "data" / "processed" / "supply_chain_data.parquet"

    parquet_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    df.to_parquet(parquet_path, index=False, engine='pyarrow')

    print(f"Converted {csv_path} to {parquet_path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

if __name__ == "__main__":
    convert_csv_to_parquet()
