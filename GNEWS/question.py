import pandas as pd
from datetime import datetime, timezone, timedelta

df = pd.read_csv("news_data.csv")

#verifying csv is loaded correctly
'''
print("\nCSV loaded successfully for analysis")
print("Total rows in CSV:", len(df))

print("\nPreview fo data:")
print(df.head())
'''
#question 1
print("Which country out of Neapl, India, USA, UK and Australia published the most headlines today?")

country_counts = df["country"].value_counts()

print("\nHeadlines count per country:")
print(country_counts)

#count maxium headlines count
most_headlines_count = country_counts.max()

#get all ountries with max counts
most_headlines_country = country_counts[country_counts == most_headlines_count]

print("\nCountry with the most headlines today: ")
for country, count in most_headlines_country.items():
    print(f'{count} headlines in {country}')


#question 2
print("\nWhat is the Average number of words in a headline title per country?")
#count number of words i each title
df["title_word_count"] = df["title"].apply( #create  new column in pandas dataframe by counting the word in exisiting column title
    lambda x: len(str(x).split())
)

avg_words_per_country = df.groupby("country")["title_word_count"].mean().round(2)

print("\nAverage number of words in headline title per country:")
print(f"{avg_words_per_country} words in {country}")

#question 3
print("\nAre there any headlines that appeared in more than one country? If yes, which one?")
df["duplicate_title"] = df["title"].str.lower().str.strip()

# Find duplicates across countries
duplicates = df[df.duplicated(subset=["duplicate_title"], keep=False)]
if len(duplicates)>0:
    print("\nYes there are headlines that appeared in more than one country.")
    print(duplicates.sort_values("duplicate_title"))
else:
    print("\nNo duplicates Found")


#question 4
print("\nWhich news source published the most headlines across all 5 countries?")
source_counts = df["source_name"].value_counts()
print(source_counts)

top_source = source_counts.idxmax()
max_source_count = source_counts.max()

print(f"{top_source} published most headlines ({max_source_count}) across all 5 countries.")

#question 5
print("\nWhat percentage of all headlines were published in the last 6 hours vs older than 6 hours")
#current time
current_time = datetime.now(timezone.utc)

#convert published_at column to datetime
df["published_at"] = pd.to_datetime(df["published_at"], errors = "coerce")

#time difference
df["time_difference"] = current_time - df["published_at"]

#headlines published within last 6 hours
recent_headlines = df[df["time_difference"] <= timedelta(hours=6)]
#headlines published older than 6 hours
older_headlines = df[df["time_difference"] > timedelta(hours=6)]

num_recent = len(recent_headlines)
num_older = len(older_headlines)

total_headlines = len(df)

recent_percentage = ((num_recent/total_headlines)*100)
older_percentage = ((num_older/total_headlines)*100)

print(f"{recent_percentage:.2f} % headlines were published in last 6 hours")
print(f"{older_percentage:.2f} % headlines were published older than 6 hours")

#question 7
print("\nSave only headlines with a title longer than 6 words to a CSV. How many passed that filter?")

#question 8
print("\nWhich country had the longest headline on average and which had the shortest?")