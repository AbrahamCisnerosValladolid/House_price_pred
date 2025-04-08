import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_estimated_price(bath, number_bedrooms, total_sqft_fix, location):
   
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0] = bath
    x[1] = number_bedrooms
    x[2] = total_sqft_fix
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0],2)

def load_saved_artifacts():
    print("loading saved artifacts ... start")
    global __data_columns
    global __locations
    global __model

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)["data_columns"]
        __locations = __data_columns[3:]
        
    
    with open("./artifacts/bangalore_home_prices_model.pickle", "rb") as f:
        __model = pickle.load(f)
        print("loading saved artifacts ... done")


def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

if __name__ == "__main__":
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price(2, 2, 1000, "1st phase jp nagar"))
    print(get_estimated_price(2, 2, 1000, "Indira Nagar"))
    # print(get_estimated_price(2, 2, 1000, "Kalhalli"))
    