// Land Cover Change & Drought Overlay (Starter) — Earth Engine (JS)
// Switch STATE_FIPS to target state (e.g., '26' for Michigan).
// NOTE: You may need to adjust collections if deprecated; these were common as of 2024.

var STATE_FIPS = '26'; // Michigan
var START_YEAR = 2016;
var END_YEAR = 2024;

var counties = ee.FeatureCollection('TIGER/2018/Counties')
  .filter(ee.Filter.eq('STATEFP', STATE_FIPS));

// USDA Cropland Data Layer (CDL): ee.ImageCollection('USDA/NASS/CDL')
// WorldCover alternative: ee.ImageCollection('ESA/WorldCover/v200')
var cdl = ee.ImageCollection('USDA/NASS/CDL');

function cropMask(img) {
  // CDL classes for cultivated crops are typically 1-176 range with many codes; 
  // A simple heuristic: cropland classes > 0 and != 190/195/255 (non-ag categories).
  // Refine per your needs.
  var nonCrop = [0, 111, 112, 121, 122, 123, 131, 141, 142, 143, 152, 190, 195, 204, 205, 206, 254, 255];
  var mask = img.neq(0);
  nonCrop.forEach(function(v) { mask = mask.and(img.neq(v)); });
  return img.updateMask(mask).gt(0).rename('crop');
}

var startImg = cropMask(cdl.filter(ee.Filter.eq('year', START_YEAR)).first());
var endImg = cropMask(cdl.filter(ee.Filter.eq('year', END_YEAR)).first());

// Change map: -1 = loss, 0 = stable, +1 = gain
var change = endImg.subtract(startImg).rename('change');

// CHIRPS precipitation anomaly proxy (annual total z-score-ish via baseline)
var chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY');
var startAnnual = chirps.filterDate(START_YEAR + '-01-01', START_YEAR + '-12-31').sum();
var endAnnual = chirps.filterDate(END_YEAR + '-01-01', END_YEAR + '-12-31').sum();
var precipChange = endAnnual.subtract(startAnnual).rename('precip_delta');

// Zonal stats per county
var scale = 30; // CDL native is 30m
var results = change.addBands(precipChange).reduceRegions({
  collection: counties,
  reducer: ee.Reducer.mean().combine({
    reducer2: ee.Reducer.frequencyHistogram(), geometries: false
  }),
  scale: scale
});

// Export table
Export.table.toDrive({
  collection: results,
  description: 'agri_resilience_change_' + STATE_FIPS + '_' + START_YEAR + '_' + END_YEAR,
  fileFormat: 'CSV'
});

// Map display
Map.centerObject(counties, 6);
Map.addLayer(change, {min: -1, max: 1, palette: ['#2166ac','#f7f7f7','#b2182b']}, 'Cropland Change');
Map.addLayer(precipChange, {min: -500, max: 500}, 'Precip Delta (mm?)');
Map.addLayer(counties.style({color: 'black', fillColor: '00000000', width: 1}), {}, 'Counties');
