import ibis
import pandas as pd
from pathlib import Path

def test_duckdb_integration():
    base_dir = Path(__file__).parent
    parquet_path = str(base_dir / "data" / "processed" / "supply_chain_data.parquet")

    print("Testing DuckDB + Ibis integration...")
    print(f"Parquet file: {parquet_path}")

    con = ibis.duckdb.connect()
    table = con.read_parquet(parquet_path, table_name="supply_chain")

    print(f"\nTable schema:")
    print(table.schema())

    print(f"\nTotal rows: {table.count().execute()}")

    print("\nTest filter 1: Product type = 'skincare'")
    filtered = table.filter(table["Product type"] == "skincare")
    result = filtered.to_pandas()
    print(f"Filtered rows: {len(result)}")

    print("\nTest filter 2: Transportation modes in ['Air', 'Road']")
    filtered = table.filter(table["Transportation modes"].isin(["Air", "Road"]))
    result = filtered.to_pandas()
    print(f"Filtered rows: {len(result)}")

    print("\nTest combined filters")
    filtered = table.filter(
        (table["Product type"] == "skincare") &
        (table["Transportation modes"].isin(["Air", "Road"]))
    )
    result = filtered.to_pandas()
    print(f"Filtered rows: {len(result)}")
    print(f"Sample columns: {result.columns.tolist()[:5]}")

    print("\n✓ DuckDB integration test passed!")

if __name__ == "__main__":
    test_duckdb_integration()
