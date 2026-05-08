# import pandas as pd
#
#
# def load_and_clean_data(filepath):
#     try:
#         # Load the CSV
#         df = pd.read_csv(filepath, low_memory=False)
#         print("✅ CSV loaded successfully!")
#
#         # 1. Expanded City List
#         major_cities = ['Berlin', 'München', 'Hamburg', 'Köln', 'Frankfurt am Main', 'Stuttgart']
#         df = df[df['regio2'].isin(major_cities)].copy()
#
#         # 2. Updated Column Mapping (Added features)
#         cols_to_keep = {
#             'regio2': 'city',
#             'regio3': 'district',
#             'baseRent': 'baseRent',
#             'totalRent': 'totalRent',
#             'livingSpace': 'livingSpace',
#             'noRooms': 'noRooms',
#             'hasKitchen': 'hasKitchen',
#             'balcony': 'balcony'
#         }
#
#         df = df[list(cols_to_keep.keys())]
#         df = df.rename(columns=cols_to_keep)
#
#         # 3. Data Cleaning
#         df = df.dropna(subset=['baseRent', 'livingSpace', 'noRooms'])
#
#         # Clean district names (Remove underscores)
#         df['district'] = df['district'].str.replace('_', ' ')
#
#         # Filter out outliers
#         df = df[(df['baseRent'] > 200) & (df['baseRent'] < 10000)]
#         df = df[(df['livingSpace'] > 10) & (df['livingSpace'] < 500)]
#
#         # 4. Math
#         df['price_per_m2'] = df['baseRent'] / df['livingSpace']
#
#         print(f"✅ Cleaned data has {len(df)} listings across {df['city'].nunique()} cities.")
#         return df
#
#     except Exception as e:
#         print(f"❌ Error in processor: {e}")
#         return None
import pandas as pd


def load_and_clean_data(filepath):
    try:
        # Load the CSV
        df = pd.read_csv(filepath, low_memory=False)

        # Mapping Kaggle columns to clean names
        cols = {
            'regio2': 'city', 'regio3': 'district', 'baseRent': 'baseRent',
            'totalRent': 'totalRent', 'livingSpace': 'livingSpace',
            'noRooms': 'noRooms', 'hasKitchen': 'hasKitchen', 'balcony': 'balcony',
            'petsAllowed': 'petsAllowed', 'garden': 'garden', 'lift': 'lift'
        }

        # Filter existing columns and rename
        df = df[list(cols.keys())].rename(columns=cols)
        df = df.dropna(subset=['baseRent', 'livingSpace', 'city'])

        # Formatting
        df['city'] = df['city'].str.title().str.replace('_', ' ')
        df['district'] = df['district'].str.replace('_', ' ')

        # Outlier filtering
        df = df[(df['baseRent'] > 150) & (df['baseRent'] < 8000)]
        df['price_per_m2'] = (df['baseRent'] / df['livingSpace']).round(2)

        return df
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def get_market_stats(df):
    return {
        'total_listings': f"{len(df):,}",
        'avg_rent': f"€{round(df['totalRent'].mean(), 2)}",
        'city_count': df['city'].nunique(),
        'top_city': df.groupby('city')['price_per_m2'].mean().idxmax()
    }