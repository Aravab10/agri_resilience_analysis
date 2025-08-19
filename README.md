# Agri-Resilience: Land Use Change & Drought Risk (Starter Kit)

This starter project helps you showcase **geospatial analysis** for agricultural resilience, using **Google Earth Engine (GEE)**, **Python (GeoPandas)**, **QGIS**, and a lightweight **Streamlit** dashboard.

## What it does (MVP)
1. **Land cover change** (cropland vs non-cropland) between two years using USDA Cropland Data Layer (CDL) or ESA WorldCover.
2. **Drought exposure** overlay using CHIRPS precipitation anomaly or SPEI proxy (via ERA5-Land).
3. **County-level statistics** (acres changed, % change) with export to CSV.
4. **Streamlit dashboard** to filter by county and year, and visualize metrics.

> ⚠️ You can switch from Michigan to any US state by changing the boundary asset.

## Quick Start
### 1) GEE (JavaScript)
- Open **`gee/land_cover_change.js`** in the Earth Engine Code Editor.
- Set `STATE_FIPS` and `START_YEAR`/`END_YEAR`.
- Run and export the county stats table to Google Drive as CSV.

### 2) Python (Processing & Joins)
- Install requirements:
  ```bash
  cd python
  pip install -r requirements.txt
  ```
- Place exported CSV(s) into `../data/exports/` (create folder).
- Run:
  ```bash
  python pipeline.py --counties shapefiles/mi_counties.shp --exports ../data/exports --out ../data/processed/metrics.csv
  ```

### 3) Streamlit App
- From project root:
  ```bash
  cd streamlit
  pip install -r ../python/requirements.txt
  streamlit run app.py
  ```

## Suggested Storyline (for Dr. Lark)
- **Question:** Where is cropland expanding/shrinking and how is it correlating with drought exposure?
- **Method:** CDL-based change detection, county-level zonal stats, overlay precipitation anomaly (CHIRPS) / PET (ERA5-Land), export clean metrics.
- **Output:** A CSV + simple dashboard highlighting hotspots and a reproducible GEE script.

## Folders
- `gee/` — Earth Engine JS analysis
- `python/` — processing pipeline
- `streamlit/` — dashboard app
- `data/` — place exports/processed files here
- `notebooks/` — optional exploration

— Generated 2025-08-08
