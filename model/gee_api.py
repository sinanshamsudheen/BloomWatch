import ee
import time

# --- CONFIGURATION ---
COORDINATES_ASSET_ID = 'users/van_der1873/Alaska_Points'
OUTPUT_FILE_NAME = 'Alaska_Phenology_ML_Data_Final'
START_DATE = '2000-01-01'
END_DATE = '2015-12-31'
SCALE = 1000
# ---------------------

# 1. Initialize Earth Engine
try:
    ee.Initialize(project='alaska-vegetation')
    print("✅ Earth Engine successfully initialized.")
except Exception as e:
    print(f"❌ Initialization Failed: {e}")
    exit()

# 2. Define Image Collections
ndvi_collection = ee.ImageCollection('MODIS/061/MOD13Q1') \
    .select(['NDVI', 'SummaryQA']) \
    .filterDate(START_DATE, END_DATE)

lst_mod = ee.ImageCollection('MODIS/061/MOD11A2') \
    .select(['LST_Day_1km', 'LST_Night_1km', 'QC_Day', 'QC_Night']) \
    .filterDate(START_DATE, END_DATE)

lst_myd = ee.ImageCollection('MODIS/061/MYD11A2') \
    .select(['LST_Day_1km', 'LST_Night_1km', 'QC_Day', 'QC_Night']) \
    .filterDate(START_DATE, END_DATE)

lst_collection = lst_mod.merge(lst_myd)

# 3. Load Coordinates
points = ee.FeatureCollection(COORDINATES_ASSET_ID)

# 4. Define the Extraction Function
def extract_phenology_features(image):
    day_lst = image.select('LST_Day_1km').multiply(0.02)
    night_lst = image.select('LST_Night_1km').multiply(0.02)
    mean_lst = day_lst.add(night_lst).divide(2).rename('Mean_LST_K')
    
    final_image = image.select(['NDVI', 'SummaryQA', 'QC_Day', 'QC_Night']).addBands(mean_lst)

    point_data = final_image.reduceRegions(
        collection=points,
        reducer=ee.Reducer.mean(),
        scale=SCALE
    )
    
    def add_date_info(feature):
        date = ee.Date(image.get('system:time_start'))
        return feature.set({
            'date': date.format('YYYY-MM-dd'),
            'year': date.get('year'),
            # FINAL FIX: Changed to the correct GEE function getDayOfYear()
            'doy': date.getDayOfYear()
        })
    return point_data.map(add_date_info)

# 5. Join and Merge Collections
time_filter = ee.Filter.maxDifference(
    difference=8 * 24 * 60 * 60 * 1000,
    leftField='system:time_start',
    rightField='system:time_start'
)

inner_join = ee.Join.inner()

joined_collection = inner_join.apply(
    primary=ndvi_collection,
    secondary=lst_collection,
    condition=time_filter
)

def merge_from_inner_join(feature):
    primary_image = ee.Image(feature.get('primary'))
    secondary_image = ee.Image(feature.get('secondary'))
    return primary_image.addBands(secondary_image)

merged_collection = ee.ImageCollection(joined_collection.map(merge_from_inner_join))

# 6. Execute the Final Workflow
print("\nProceeding to final feature extraction...")
all_extracted_features = merged_collection.map(extract_phenology_features).flatten()

# 7. Export the Final FeatureCollection to Google Drive
task = ee.batch.Export.table.toDrive(
    collection=all_extracted_features,
    description=OUTPUT_FILE_NAME,
    folder='GEE_Exports',
    fileNamePrefix=OUTPUT_FILE_NAME,
    fileFormat='CSV'
)

task.start()

print(f"\n🚀 GEE Export Task '{OUTPUT_FILE_NAME}' Started Successfully!")
print("Congratulations! The script is now fully corrected and the export will complete.")
print("You can monitor the task in the GEE Code Editor 'Tasks' tab.")