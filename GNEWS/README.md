# GNEWS Data Pipeline Task
In this project, I have a complete data pipeline using Python to:
- fetch news data from an API
- Store it in a CSV file
- Clean and preprocess the data
- Perform analysis using Pandas
The key focus of my learning was on **data handling using Pandas, data cleaning, and efficient analysis from stored datasets instead of using API calls directly.**<br />
# Pandas
Used for data manipulation and analysis. It works by **transforming raw data from various formats into high-level, labeled data structures that are easy to manipulate and clean.**
# Series in Pandas
A Pandas Series is a one-dimensional labeled array.
```python
'''pd.Series(data, index=None, dtype=None)'''
import pandas as pd

s = pd.Series([10, 20, 30], index=["a", "b", "c"])
s.values #array([10,20,30])
s.index #['a','b','c']
s.dtype #int64
'''
a    10
b    20
c    30
dtype: int64
'''
```

---

# DataFrame
Collection of Series.<br />
In code, df["title"], df["country"], df["word_count"] are series objects.

# Series Operations
**Counting values (value_counts)**<br />
```python
Series.value_counts(normalize=False, sort=True, ascending=False, dropna=True)
```

---

- normalize = True : returns percentage instead of count
- sort = False : keeps original order
- ascending = True : lowest to highest
- dropna = False : includes NaN in count
**Apply Functions (Apply**)<br />
```python
Series.apply(func)
DataFrame.apply(func, axis=0 or 1)
```
---

- applies function to each series, and each df, axis=0 column wise and axis=1 row wise
**Grouping Data (groupby)**<br />
Splits data into groups, applies function aand combines result.
```python
DataFrame.groupby(by, as_index=True).agg(func)
```

---

**Aggregate function**<br />
```python
.mean() #finds mean
.sum() #finds sum
.count() 
.min() #returns minimum value
.max() #returns maxium value
.idmax() #returns index of highest value
.idmin() #returns index of lowest value
```

---

# Creating a DataFrame
```python
df = pd.DataFrame(structured_data_object)
```

---

structured_data_object refers to list, tuples, dictionary<br />
It Converts a list of dictionaries, tuples into a tabular format. Each dictionary is one row and keys are column names.
# Cleaning Column Names
```python
df.columns = df.columns.str().strip()
```

---

- .column access column labels
- .str.lower() converts all names to lowercase
- .str.strip() removes unwanted spaces
# Handling Missing Data
```python
df.fillna("N/A", implace = True)
```

---

- Replace all missing values with "N/A"
- implace = True modifies the original DataFrame
# Reading and Writing CSV
```python
filename = "filename.csv"
df.to_csv(filename, index=False) df = pd.read_csv(filename)
```

---

- index = False avoids adding extra index column
# Removing Duplicate Rows
```python
combined_df.drop_duplicates(subset=["url"], inplace=True)
```

---

- identifies duplicate rows based on the url column and keeps only unique entries
- implace = True modifies the original DataFrame
