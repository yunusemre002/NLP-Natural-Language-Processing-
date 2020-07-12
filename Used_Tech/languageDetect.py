import pandas as pd
from langdetect import detect

# print(detect('今一はお前さん'))

reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Final_Project/DataSets/London2.csv", encoding="ISO-8859-1")  # Read data !
reviews_df = reviews_df[reviews_df['Review Text'].str.contains("<U") == False]  # Remove some reviews created full of unknown characters.
reviews_df_com = reviews_df[['Review Text', 'Review Rating', 'Property Name']]
reviews_df_com = reviews_df_com.dropna().copy()  # Remove emty review.
# reviews_df_com = reviews_df_com.sample(frac = 0.01, replace = False, random_state=42) # Toplamda 15000 yarom var bunların %1 ini yani 1500 tanesini işleme koy.
print(reviews_df_com.describe())

j = 1
for t in range(len(reviews_df_com)):  # iterate for each object
    i = str(reviews_df_com['Review Text'].values[t])  # Take just reviews to String : i
    if detect(i) != "en":
        print(j, i)
        # reviews_df_com = reviews_df_com.drop(index=reviews_df_com['Review Text'].index[t])
        j += 1

print("toplam: {},  Others: {}, English: {}".format(len(reviews_df_com), j, len(reviews_df_com) - j))
