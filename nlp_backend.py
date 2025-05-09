import spacy
import psycopg2
import math

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="NLP_Data",
    user="postgres",
    password="ahmad",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Haversine distance function
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# Load city names once
def get_all_city_names():
    cursor.execute("SELECT city_name FROM nrw_cities")
    return [row[0].lower() for row in cursor.fetchall()]

city_list = get_all_city_names()

# Get city info
def get_city_info(city):
    cursor.execute("SELECT latitude, longitude, elevation FROM nrw_cities WHERE LOWER(city_name) = LOWER(%s)", (city,))
    return cursor.fetchone()

# Extract cities from query
def extract_cities(query):
    words = query.lower().split()
    return [city for city in city_list if city in words]

# Main query handler
def handle_query(query):
    cities = extract_cities(query)
    query_lower = query.lower()

    if "distance" in query_lower and len(cities) == 2:
        info1 = get_city_info(cities[0])
        info2 = get_city_info(cities[1])
        if info1 and info2:
            dist = haversine(info1[0], info1[1], info2[0], info2[1])
            return f"Distance between {cities[0].title()} and {cities[1].title()} is approximately {dist:.2f} km."
    elif "elevation" in query_lower and len(cities) == 1:
        info = get_city_info(cities[0])
        if info:
            return f"Elevation of {cities[0].title()} is {info[2]} meters."
    else:
        return "Sorry, I couldn't understand your request."
