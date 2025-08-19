import argparse
import os
import pandas as pd
import geopandas as gpd

def load_counties(path):
    gdf = gpd.read_file(path)
    # Expect a county name field, e.g., 'NAME' for TIGER
    if 'NAME' not in gdf.columns:
        print("WARN: 'NAME' field not found. Columns:", gdf.columns)
    return gdf

def load_exports(exports_dir):
    # Merge multiple CSV exports from GEE (if you exported per year or batch)
    frames = []
    for fn in os.listdir(exports_dir):
        if fn.lower().endswith('.csv'):
            frames.append(pd.read_csv(os.path.join(exports_dir, fn)))
    if not frames:
        raise FileNotFoundError("No CSV files found in exports dir.")
    df = pd.concat(frames, ignore_index=True)
    return df

def clean_and_join(counties_gdf, exports_df):
    # Heuristic join on county name (adjust as needed)
    county_col_candidates = [c for c in exports_df.columns if c.lower() in ('name','county','county_nam','county_name')]
    if not county_col_candidates:
        raise ValueError("Could not find county name column in exports.")
    county_col = county_col_candidates[0]
    exports_df[county_col] = exports_df[county_col].astype(str).str.strip().str.upper()
    counties_gdf['NAME_UP'] = counties_gdf['NAME'].astype(str).str.strip().str.upper()

    merged = counties_gdf.merge(exports_df, left_on='NAME_UP', right_on=county_col, how='left')
    return merged

def compute_metrics(gdf):
    # Example metric: percent cropland change using histogram output if available
    # Assume frequency histogram stored in column like 'change_histogram'; if not present, skip.
    hist_col = next((c for c in gdf.columns if 'histogram' in c.lower()), None)
    if hist_col and gdf[hist_col].notna().any():
        def pct_gain_loss(h):
            try:
                d = eval(h) if isinstance(h, str) else h
                gain = d.get('1', 0)
                loss = d.get('-1', 0)
                total = sum(d.values()) or 1
                return pd.Series({
                    'pct_gain': 100.0 * gain / total,
                    'pct_loss': 100.0 * loss / total
                })
            except Exception:
                return pd.Series({'pct_gain': None, 'pct_loss': None})
        gdf[['pct_gain','pct_loss']] = gdf[hist_col].apply(pct_gain_loss)
    return gdf

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counties", required=True, help="Path to county shapefile/geojson (e.g., TIGER counties for Michigan).")
    ap.add_argument("--exports", required=True, help="Directory with CSV exports from GEE.")
    ap.add_argument("--out", required=True, help="Output CSV path.")
    args = ap.parse_args()

    counties = load_counties(args.counties)
    exports = load_exports(args.exports)
    merged = clean_and_join(counties, exports)
    metrics = compute_metrics(merged)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    metrics.drop(columns=['geometry']).to_csv(args.out, index=False)
    print(f"Wrote metrics to {args.out}")

if __name__ == "__main__":
    main()
