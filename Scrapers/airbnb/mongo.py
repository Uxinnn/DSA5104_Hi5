from pymongo import MongoClient
import pandas as pd
import numpy as np
from datetime import datetime
import time
import uuid

cities = ["Asheville", "Austin", "Boston", "Bozeman", "Broward County", "Cambridge", "Chicago", "Clark County", "Columbus", "Dallas"]
for city in cities:
    UID = str(uuid.uuid4())
    print(f"Mongo {city}")
    csv = pd.read_csv(f'{city}/review_scrapped.csv')
    review_df = csv[["listing_id", "id", "date","reviewer_id","comments"]]

    user_df = csv[["reviewer_id","reviewer_name","location"]]
    user_df.columns = ["_id", "name", "location"]
    review_extra_csv = user_df.apply(lambda x: [f"Review by {x['name']}"] + np.minimum(np.random.normal(4.4, 0.5, 8), 5-np.random.normal(0.01, 0.001)).tolist(), axis=1, result_type="expand")
    review_df.reset_index(drop=True, inplace=True)
    review_extra_csv.reset_index(drop=True, inplace=True)
    review_df = pd.concat([review_df, review_extra_csv], axis=1)
    review_df.columns = ["listing_id", "_id", "date","reviewer_id","text", "title","overall_score","cleanliness_score","service_score","value_score","location_score","sleepquality_score","checkin_score","communication_score"]
    assert review_df.shape[0] == review_extra_csv.shape[0]


    listing_csv = pd.read_csv(f'{city}/listings.csv')
    doc_csv = listing_csv[["id", "listing_url", "name", "neighbourhood"]]
    rating_csv = []
    host_csv = listing_csv[["host_since", "host_location", "host_about", "host_response_time", "host_neighbourhood", "host_verifications", "host_name"]]
    loc_csv = listing_csv[["latitude", "longitude"]]
    loc_csv = loc_csv.apply(lambda x: f"{x['latitude']}, {x['longitude']}", axis=1).to_frame("address_detailed")
    host_csv = host_csv.apply(lambda x: {"name": x["host_name"], "host_since" : x['host_since'],"host_description":x['host_about'], "host_address": x["host_location"], "host_responsetime": x["host_response_time"],"host_neighbourhood": x["host_neighbourhood"],"host_verification": x["host_verifications"]}, axis=1).to_frame("host")
    listing_review = doc_csv.apply(lambda x: (review_df[review_df["listing_id"] ==  x['id']])["_id"].tolist() ,axis=1).to_frame("reviews")

    doc_csv.reset_index(drop=True, inplace=True)
    loc_csv.reset_index(drop=True, inplace=True)
    host_csv.reset_index(drop=True, inplace=True)
    listing_review.reset_index(drop=True, inplace=True)
    listing_df = pd.concat([doc_csv, loc_csv, host_csv, listing_review],  axis=1)
    listing_df.columns = ["_id", "url", "name", "address", 'address_detailed', 'host', 'reviews']
    listing_df["type"] = "airbnb"
    listing_df["neighbourhood_city"] = UID
    assert doc_csv.shape[0] == listing_df.shape[0]

    attr_csv = pd.read_csv(f'{city}/attractions.csv')["0"].tolist()

    neighbourhood = {"_id": UID, "city": city, "country": "United States", "attractions": attr_csv}

    user_csv_listing = listing_csv[["host_id","host_since", "host_location", "host_about", "host_response_time", "host_neighbourhood", "host_verifications", "host_name"]]
    user_csv_listing = user_csv_listing.apply(lambda x: [x["host_id"], x["host_name"],x["host_neighbourhood"], {"host_since" : x['host_since'],"host_description":x['host_about'], "host_address": x["host_location"], "host_responsetime": x["host_response_time"],"host_neighbourhood": x["host_neighbourhood"],"host_verification": x["host_verifications"]}], axis=1, result_type="expand")
    user_csv_listing.columns = ["_id", "name", "location", "host"]
    user_df_combined = pd.concat([user_csv_listing, user_df], axis=0)
    user_df_combined.drop_duplicates(subset=['_id'], ignore_index=True, inplace=True)
    user_review = user_df_combined.apply(lambda x: (review_df[review_df["reviewer_id"] ==  x['_id']])["_id"].tolist() ,axis=1).to_frame("reviews")
    user_df_combined.reset_index(drop=True, inplace=True)
    user_review.reset_index(drop=True, inplace=True)
    user_df_final =  pd.concat([user_df_combined, user_review], axis=1)
    assert user_df_final.shape[0] == user_df_combined.shape[0]
    print("Done data processing")


    transactions = list()
    for ind, accom in listing_df.iterrows():
        aid = accom["_id"]
        if not isinstance(accom["reviews"], list):
            continue
        for rid in accom["reviews"]:

            start_epoch = np.random.randint(1100000000, 1700000000)
            duration = np.random.randint(1, 14)
            end_epoch = start_epoch + 86400 * duration
            t = {
                "date_start": time.strftime('%B %d, %Y', time.localtime(start_epoch)), 
                "date_end": time.strftime('%B %d, %Y', time.localtime(end_epoch)), 
                "price": np.random.randint(100, 1000) * duration, 
                "review_id": rid, 
                "accomodation_id": aid, 
            }
            transactions.append(t)
            
        
    client = MongoClient('localhost', 27017) 
    db = client["project"]
    listing_df.drop_duplicates(subset=['_id'], ignore_index=True, inplace=True)
    review_df.drop_duplicates(subset=['_id'], ignore_index=True, inplace=True)
    user_df_final.drop_duplicates(subset=['_id'], ignore_index=True, inplace=True)

    db["accommodation"].insert_many(listing_df.to_dict('records'))
    db["reviews"].insert_many(review_df.to_dict('records'))

    for user_dict in user_df_final.to_dict('records'):
        ret = db["user"].find_one({"_id": user_dict["_id"]})
        if not ret:
            db["user"].insert_one(user_dict)
        else:
            ret["reviews"] = ret["reviews"] + user_dict["reviews"]
            if isinstance(user_dict["host"], dict):
                ret["host"] = user_dict["host"]
            db["user"].replace_one({"_id": ret["_id"]}, ret)

    db["neighbourhood"].insert_one(neighbourhood)
    db["transactions"].insert_many(transactions)
