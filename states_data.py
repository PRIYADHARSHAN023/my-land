"""
Indian states and crop data for the My Land application
Contains dropdown options and reference data
"""

# Indian states and union territories
INDIAN_STATES = {
    'Andhra Pradesh': 'AP',
    'Arunachal Pradesh': 'AR',
    'Assam': 'AS',
    'Bihar': 'BR',
    'Chhattisgarh': 'CG',
    'Goa': 'GA',
    'Gujarat': 'GJ',
    'Haryana': 'HR',
    'Himachal Pradesh': 'HP',
    'Jharkhand': 'JH',
    'Karnataka': 'KA',
    'Kerala': 'KL',
    'Madhya Pradesh': 'MP',
    'Maharashtra': 'MH',
    'Manipur': 'MN',
    'Meghalaya': 'ML',
    'Mizoram': 'MZ',
    'Nagaland': 'NL',
    'Odisha': 'OR',
    'Punjab': 'PB',
    'Rajasthan': 'RJ',
    'Sikkim': 'SK',
    'Tamil Nadu': 'TN',
    'Telangana': 'TG',
    'Tripura': 'TR',
    'Uttar Pradesh': 'UP',
    'Uttarakhand': 'UK',
    'West Bengal': 'WB',
    'Andaman and Nicobar Islands': 'AN',
    'Chandigarh': 'CH',
    'Dadra and Nagar Haveli and Daman and Diu': 'DN',
    'Delhi': 'DL',
    'Jammu and Kashmir': 'JK',
    'Ladakh': 'LA',
    'Lakshadweep': 'LD',
    'Puducherry': 'PY'
}

# Major crop types grown in India
CROP_TYPES = [
    'Rice',
    'Wheat', 
    'Maize',
    'Cotton',
    'Sugarcane',
    'Soybean',
    'Groundnut',
    'Pulses',
    'Mustard',
    'Sunflower',
    'Barley',
    'Jowar',
    'Bajra',
    'Ragi',
    'Turmeric',
    'Chili',
    'Onion',
    'Potato',
    'Tomato',
    'Banana'
]

# State-wise major crops (for recommendations)
STATE_MAJOR_CROPS = {
    'Punjab': ['Wheat', 'Rice', 'Maize', 'Cotton'],
    'Haryana': ['Wheat', 'Rice', 'Sugarcane', 'Cotton'],
    'Uttar Pradesh': ['Wheat', 'Rice', 'Sugarcane', 'Potato'],
    'Madhya Pradesh': ['Wheat', 'Soybean', 'Rice', 'Cotton'],
    'Maharashtra': ['Cotton', 'Sugarcane', 'Soybean', 'Rice'],
    'Karnataka': ['Rice', 'Cotton', 'Sugarcane', 'Maize'],
    'Andhra Pradesh': ['Rice', 'Cotton', 'Groundnut', 'Sugarcane'],
    'Tamil Nadu': ['Rice', 'Cotton', 'Sugarcane', 'Groundnut'],
    'Gujarat': ['Cotton', 'Groundnut', 'Wheat', 'Rice'],
    'Rajasthan': ['Wheat', 'Mustard', 'Barley', 'Cotton'],
    'West Bengal': ['Rice', 'Wheat', 'Potato', 'Jute'],
    'Bihar': ['Rice', 'Wheat', 'Maize', 'Sugarcane'],
    'Odisha': ['Rice', 'Wheat', 'Sugarcane', 'Cotton'],
    'Telangana': ['Rice', 'Cotton', 'Maize', 'Sugarcane'],
    'Kerala': ['Rice', 'Coconut', 'Spices', 'Rubber'],
    'Assam': ['Rice', 'Tea', 'Jute', 'Cotton']
}

# Crop seasons
CROP_SEASONS = {
    'Kharif': ['Rice', 'Cotton', 'Sugarcane', 'Maize', 'Soybean', 'Groundnut', 'Jowar', 'Bajra'],
    'Rabi': ['Wheat', 'Barley', 'Mustard', 'Chickpea', 'Peas', 'Linseed'],
    'Zaid': ['Maize', 'Fodder', 'Watermelon', 'Cucumber', 'Sunflower']
}

# Soil type preferences for crops
CROP_SOIL_PREFERENCES = {
    'Rice': {
        'soil_types': ['Clay', 'Clay Loam'],
        'ph_range': (5.5, 6.5),
        'drainage': 'Poor to moderate'
    },
    'Wheat': {
        'soil_types': ['Loam', 'Clay Loam', 'Sandy Loam'],
        'ph_range': (6.0, 7.5),
        'drainage': 'Well drained'
    },
    'Cotton': {
        'soil_types': ['Black Cotton Soil', 'Clay Loam'],
        'ph_range': (5.8, 8.0),
        'drainage': 'Well drained'
    },
    'Maize': {
        'soil_types': ['Loam', 'Sandy Loam', 'Clay Loam'],
        'ph_range': (6.0, 7.5),
        'drainage': 'Well drained'
    },
    'Sugarcane': {
        'soil_types': ['Clay Loam', 'Loam'],
        'ph_range': (6.5, 7.5),
        'drainage': 'Moderate'
    },
    'Soybean': {
        'soil_types': ['Clay Loam', 'Sandy Loam'],
        'ph_range': (6.0, 7.0),
        'drainage': 'Well drained'
    }
}

# Climate requirements for major crops
CROP_CLIMATE_REQUIREMENTS = {
    'Rice': {
        'temperature_range': (20, 35),
        'rainfall_range': (1000, 2000),
        'humidity': 'High',
        'season': 'Kharif'
    },
    'Wheat': {
        'temperature_range': (12, 25),
        'rainfall_range': (450, 650),
        'humidity': 'Low to moderate',
        'season': 'Rabi'
    },
    'Cotton': {
        'temperature_range': (21, 35),
        'rainfall_range': (500, 1000),
        'humidity': 'Moderate',
        'season': 'Kharif'
    },
    'Maize': {
        'temperature_range': (18, 32),
        'rainfall_range': (500, 800),
        'humidity': 'Moderate',
        'season': 'Kharif/Rabi'
    },
    'Sugarcane': {
        'temperature_range': (20, 35),
        'rainfall_range': (1500, 2500),
        'humidity': 'High',
        'season': 'Year round'
    },
    'Soybean': {
        'temperature_range': (15, 30),
        'rainfall_range': (450, 700),
        'humidity': 'Moderate',
        'season': 'Kharif'
    }
}
