import pandas as pd
import numpy as np

loc = pd.read_csv('user_loc.csv', names=['reviewer_id','location'])
reviews = pd.read_csv('reviews.csv')

combined = reviews.merge(loc, on='reviewer_id', how='left')
choice_list = loc.location.unique()
combined['location'] = combined['location'].apply(lambda l: l if not pd.isna(l) else np.random.choice(choice_list))
combined.to_csv('review_scrapped.csv', index=False)