import pandas as pd
from termcolor import colored
import matplotlib.pyplot as plt
import seaborn as sn


"""
1. reviews_df = pd.read_csv("file.cvs", encoding = "ISO-8859-1" )  önemli
"""
reviews_df = pd.read_csv("C:/Users/Demir/Desktop/Bitirme_projesi/DataSets/London.csv", encoding = "ISO-8859-1")   # read data   !!!!!
reviews_df_com = reviews_df[['Review Text','Review Rating', 'Property Name']]
reviews_df_com = reviews_df_com.dropna().copy() # boş yorum varsa kaldırır.
#reviews_df_com = reviews_df_com.sample(frac = 0.1, replace = False, random_state=42) # Toplamda 15000 yarom var bunların %1 ini yani 1500 tanesini işleme koy.
print(reviews_df_com.count() , reviews_df_com.describe(), sep="\n")

#df_uni = reviews_df_com[['Property Name','Review Rating']].drop_duplicates()
plt.figure(figsize = (10,5))
sn.countplot(x = 'Review Rating',data = reviews_df_com,color = 'orange')
#plt.show()

plt.figure(figsize = (14,6))
plt.title('Hotel distribution in States')
df_new = reviews_df_com.rename(columns={'Property Name': 'Property_Name'})
df_new.Property_Name.value_counts().plot.barh(color= 'orange')
plt.show()
