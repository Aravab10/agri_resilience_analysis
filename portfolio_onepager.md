# Portfolio One-Pager (Draft)
**Project:** Agri-Resilience: Land Use Change & Drought Risk (Michigan)

**Objective:** Identify counties with significant cropland change and overlay drought exposure to prioritize resilience strategies.

**Data & Methods:**
- Land cover change: USDA NASS Cropland Data Layer (CDL) in **GEE**; change map (-1 loss, +1 gain).
- Drought proxy: **CHIRPS** precipitation change between start/end years.
- Zonal statistics: County-level aggregation; export CSV.
- Processing & Dashboard: **Python (GeoPandas)** + **Streamlit**.

**Deliverables:**
- GEE script (exportable table + map).
- Processed metrics CSV.
- Simple dashboard app for filtering & ranking counties.
