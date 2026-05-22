# Week 5 — Exploratory Data Analysis (EDA)

## Overview
This project focuses on performing **Exploratory Data Analysis (EDA)** using Python libraries such as Pandas, Matplotlib, and Seaborn.  
The goal was to understand datasets before modeling by analyzing statistics, distributions, correlations, missing values, and outliers.

---

# What I Learned

Through this project, I learned how to:

- Perform a complete EDA workflow on real-world datasets
- Load and analyze data using **Pandas**
- Connect Python with **MySQL**
- Understand dataset structure using:
  - `df.shape`
  - `df.info()`
  - `df.dtypes`
- Detect missing values using:
  - `df.isnull().sum()`
- Generate summary statistics using:
  - `df.describe()`
- Analyze categorical data using:
  - `value_counts()`
- Create visualizations using:
  - Histograms
  - Box plots
  - Bar charts
  - Scatter plots
  - Correlation heatmaps
  - KDE plots
  - Pair plots
- Detect outliers using the **IQR method**
- Understand relationships between variables using:
  - Correlation matrices
  - Heatmaps
  - Regression plots
- Interpret data patterns and write analytical observations
- Save charts as `.png` files for reporting
- Build structured and reusable data analysis workflows

---

# Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- MySQL
- SQLAlchemy
- Jupyter Notebook

---

# Tasks Completed

## Task 01 — EDA Checklist

Performed the complete EDA checklist on a dataset by:

- Loading the dataset into Pandas
- Checking dataset shape and data types
- Identifying missing values
- Running summary statistics
- Analyzing categorical columns
- Plotting histograms
- Plotting box plots
- Writing observations from the analysis

### Skills Practiced
- Basic EDA workflow
- Data inspection
- Visualization
- Outlier detection

---

## Task 02 — Distribution Deep Dive

Fetched weather data from an API and analyzed distributions deeply.

### Completed Steps
- Retrieved weather data for multiple cities
- Stored data in **MySQL**
- Combined and analyzed temperature distributions
- Created box plots comparing cities
- Detected outliers using the IQR method
- Generated KDE plots
- Calculated grouped summary statistics

### Skills Practiced
- API handling
- Database integration
- Statistical analysis
- Distribution comparison

---

## Task 03 — Correlation Analysis

Created a synthetic student dataset and performed correlation analysis.

### Completed Steps
- Generated realistic student data
- Calculated correlation matrix
- Created heatmaps
- Identified strongest and weakest correlations
- Built scatter plots with regression lines
- Analyzed relationships between variables

### Skills Practiced
- Correlation analysis
- Regression visualization
- Relationship interpretation
- Synthetic dataset creation

---

## Task 04 — Full EDA Report

Performed a complete EDA project using a real-world API dataset.

### Completed Steps
- Extracted data from a public API
- Cleaned and transformed the dataset
- Generated multiple visualizations
- Conducted full EDA analysis
- Wrote observations and insights
- Compared category distributions

### Skills Practiced
- End-to-end EDA process
- Real-world data analysis
- Reporting and storytelling with data
- Visualization best practices

---

# Key Concepts Covered

## Summary Statistics
- Mean
- Median
- Standard Deviation
- Min / Max
- Quartiles

## Data Visualization
- Histograms
- Box Plots
- KDE Plots
- Scatter Plots
- Heatmaps
- Pair Plots

## Correlation Analysis
- Positive correlation
- Negative correlation
- Correlation strength
- Correlation vs causation

## Outlier Detection
Used the IQR method:

```python
outlier = value > Q3 + 1.5 * IQR
outlier = value < Q1 - 1.5 * IQR