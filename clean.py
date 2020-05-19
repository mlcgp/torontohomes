# Imports
import numpy as np
import pandas as pd
import os

# Setup
df = pd.read_csv('raw_data.csv')
cwd = os.getcwd()
filename = f"{cwd}/clean_data.csv"

# Remove unwanted columns
df.drop(['Unnamed: 0', 'Status', 'Water Supply', 'Tax Legal Description', 'age'], axis=1, inplace=True)

# Rename some columns
df = df.rename(columns={'Bedrooms': 'bedrooms', 'Bedrooms_Plus': 'bedrooms_plus', 'Bathrooms': 'bathrooms',
                        'Kitchens': 'kitchens', 'Den/Family Room': 'den', 'Air Conditioning': 'air_con',
                        'Fireplace': 'fireplace', 'Basement': 'basement_A', 'Heating': 'heating_source',
                        'Heating_': 'heating_type', 'Exterior': 'exterior_mat', 'Driveway': 'driveway',
                        'Garage': 'garage', 'Parking Places': 'parking_places',
                        'Covered Parking Places': 'covered_parking', 'Taxes': 'est_annual_tax',
                        'Tax Year': 'tax_year', 'Fronting On': 'fronting_on', 'Frontage': 'frontage',
                        'Lot Depth': 'lot_depth', 'Lot Size Units': 'lot_units', 'Pool': 'pool',
                        'Cross Street': 'cross_street', 'Municipality District': 'district',
                        'Basement_': 'basement_B'})

# Move Basement B column beside Basement A
cols = list(df.columns.values)
df = df[['address', 'city', 'community', 'price', 'walk_score', 'listed_by', 'days_on_site', 'mls_id', 'type', 'style', 'bedrooms', 'Bedrooms Plus', 'bathrooms', 'kitchens', 'den', 'air_con', 'fireplace', 'basement_A', 'basement_B',
         'heating_source', 'heating_type', 'exterior_mat', 'driveway', 'garage', 'parking_places', 'covered_parking', 'est_annual_tax', 'tax_year', 'fronting_on', 'frontage', 'lot_depth', 'lot_units', 'pool', 'cross_street', 'district']]

# Data cleaning

# Start with price
df['price'] = df['price'].str.replace('\n', '').str.replace(
    '$', '').str.replace(',', '').astype(np.int32)

# Walk Score
# If the walk score wasn't found, I change the value to 0
df.loc[df.walk_score.str.len() > 2, 'walk_score'] = np.nan
df['walk_score'] = df['walk_score'].astype(float)

# Days on site
df.loc[df.days_on_site.str.contains('minutes|hours|hour', regex=True), 'days_on_site'] = '1'
df['days_on_site'] = df['days_on_site'].str.replace('Added ', '').str.replace(
    ' days ago', '').str.replace(' day ago', '')
df['days_on_site'] = df['days_on_site'].astype(int)

# Type and Style
df['type'] = df['type'].str.lower()
df['style'] = df['style'].str.lower()

# den
df['den']
df.loc[df.den.str.contains('Yes', regex=False, na=False), 'den'] = True
df.loc[df.den.str.contains('No', regex=False, na=False), 'den'] = False
df['den'] = df['den'].astype(bool)

# Air conditioning
df.loc[df.air_con.str.contains('None|N', regex=True, na=False), 'air_con'] = False
df.loc[df.air_con.str.contains('Y|Central Air|Window Unit|Wall Unit|Other|Part',
                               regex=True, na=False), 'air_con'] = True
# Fireplace
df.loc[df.fireplace.str.contains('No', regex=False, na=False), 'fireplace'] = False
df.loc[df.fireplace.str.contains('Yes', regex=True, na=False), 'fireplace'] = True

# Basement_A (weird duplicated strings separated with commas)
df['basement_A'] = df['basement_A'].str.replace('Sep Entrance, Sep Entrance', 'Sep Entrance')
df['basement_A'] = df['basement_A'].str.replace('Full, Full', 'Full')
df['basement_A'] = df['basement_A'].str.replace('Walk-Up, Walk-Up', 'Walk-Up')
df['basement_A'] = df['basement_A'].str.replace('Finished, Finished', 'Finished')
df['basement_A'] = df['basement_A'].str.replace('Fin W/O, Fin W/O', 'Fin W/O')
df['basement_A'] = df['basement_A'].str.replace('W/O, W/O', 'W/O')
df['basement_A'] = df['basement_A'].str.replace('Part Fin, Part Fin', 'Unfinished')
df['basement_A'] = df['basement_A'].str.replace('Y', 'Unfinished')
df['basement_A'] = df['basement_A'].str.replace('N', '{x}'.format(x=np.nan))
df['basement_A'] = df['basement_A'].str.replace('None', '{x}'.format(x=np.nan))
df['basement_A'] = df['basement_A'].str.replace('Unfinished, Unfinished', 'Unfinished')
df['basement_A'] = df['basement_A'].str.replace('Other, Other', 'Unfinished')

# Basement_B
df['basement_B'] = df['basement_B'].str.replace(r'^\s*$', '{x}'.format(x=np.nan), regex=True)
df['basement_B'] = df['basement_B'].str.replace('None', '{x}'.format(x=np.nan))
# print(df[['basement_A', 'basement_B']].to_string())

# Heating Source and Heating Type
df['heating_source'].str.replace('', '{x}'.format(x=np.nan))
df['heating_type'].str.replace('', '{x}'.format(x=np.nan))

# Exterior Materials
df['exterior_mat'] = df['exterior_mat'].str.replace("None", '{x}'.format(x=np.nan), regex=False)
df['exterior_mat'] = df['exterior_mat'].str.replace(r'^\s*$', '{x}'.format(x=np.nan), regex=True)

# Driveway
df['driveway'] = df['driveway'].str.replace(r'^\s*$', '{x}'.format(x=np.nan), regex=True)

# Garage
df['garage'] = df['garage'].str.replace(r'^\s*$', '{x}'.format(x=np.nan), regex=True)

# Parking
df['parking_places'] = df['parking_places'].astype(np.float16)
df['covered_parking'] = df['covered_parking'].astype(np.float16)
# Add a total column
df['total_parking'] = df.parking_places.add(df.covered_parking, fill_value=0)
# Rearrange again...
df = df[['address', 'city', 'community', 'price', 'walk_score', 'listed_by', 'days_on_site', 'mls_id', 'type', 'style', 'bedrooms', 'Bedrooms Plus', 'bathrooms', 'kitchens', 'den', 'air_con', 'fireplace', 'basement_A', 'basement_B',
         'heating_source', 'heating_type', 'exterior_mat', 'driveway', 'garage', 'parking_places', 'covered_parking', 'total_parking', 'est_annual_tax', 'tax_year', 'fronting_on', 'frontage', 'lot_depth', 'lot_units', 'pool', 'cross_street', 'district']]

# Taxes per year
df['est_annual_tax'] = df['est_annual_tax'].astype(np.float32)
df['tax_year'] = df['tax_year'].astype('Int16')

# Fronting on
df['fronting_on'] = df['fronting_on'].str.replace(r'^\s*$', '{x}'.format(x=np.nan), regex=True)

# Lot Depth
df['lot_depth'] = df['lot_depth'].astype(np.float32)
df['lot_units'] = df['lot_units'].str.replace(r'^\s*$', '{x}'.format(x=np.nan), regex=True)

# Pool
df.loc[df.pool.str.contains("None", regex=False, na=True), 'pool'] = False
df.loc[df.pool.str.contains(r'^\s*$', regex=True, na=True), 'pool'] = False
df.loc[df.pool.str.contains("Inground|Indoor|Abv Ground", regex=True, na=False), 'pool'] = True
df['pool'] = df['pool'].astype(bool)

# Cross Street
df['cross_street'] = df['cross_street'].str.replace(r'^\s*$', '{x}'.format(x=np.nan), regex=True)

# Municipality
df['district'] = df['district'].str.replace(r'^\s*$', '{x}'.format(x=np.nan), regex=True)

# Drop listings that have at least 80% of the dataframe's variables missing
df = df.dropna(axis=0, thresh=len(df.T)*0.80)

# Export csv
df.to_csv(filename)
