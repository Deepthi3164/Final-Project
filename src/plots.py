# plots.py
import pandas as pd
import matplotlib.pyplot as plt

def display_statistics(data_file):
    df = pd.read_csv(data_file)
    df.columns = df.columns.str.strip()
    df['Visit_time'] = pd.to_datetime(df['Visit_time'], format="%m/%d/%Y", errors='coerce')

    # VISIT COUNT BY YEAR
    df['Year'] = df['Visit_time'].dt.year
    yearly_counts = df.groupby('Year').size()

    plt.figure(figsize=(8, 5))
    yearly_counts.plot(kind='bar', title="Yearly Visit Trends", xlabel="Year", ylabel="Number of Visits")
    plt.tight_layout()
    plt.savefig("yearly_visit_trend.png")
    plt.close()

    # INSURANCE
    insurance_counts = df['Insurance'].value_counts()
    print("\nVisit Counts by Insurance Type:")
    print("{:<15} | {:<17}".format("Insurance", "Number of Visits"))
    print("-" * 35)
    for ins, count in insurance_counts.items():
        print("{:<15} | {:<17}".format(ins, count))

    plt.figure(figsize=(8, 5))
    insurance_counts.plot(kind='bar', title="Insurance Distribution")
    plt.xlabel("Insurance Type")
    plt.ylabel("Number of Visits")
    plt.tight_layout()
    plt.savefig("insurance_distribution.png")
    plt.close()

    # GENDER
    gender_counts = df['Gender'].value_counts()
    print("\nDemographics by Gender:")
    for gender, count in gender_counts.items():
        print(f"{gender}: {count}")

    plt.figure()
    gender_counts.plot(kind='pie', autopct='%1.1f%%', title="Gender Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("gender_distribution.png")
    plt.close()

    # RACE
    race_counts = df['Race'].value_counts()
    print("\nDemographics by Race:")
    for race, count in race_counts.items():
        print(f"{race}: {count}")

    plt.figure()
    race_counts.plot(kind='bar', title="Race Distribution")
    plt.xlabel("Race")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("race_distribution.png")
    plt.close()

    # ETHNICITY
    ethnicity_counts = df['Ethnicity'].value_counts()
    print("\nDemographics by Ethnicity:")
    for eth, count in ethnicity_counts.items():
        print(f"{eth}: {count}")

    plt.figure()
    ethnicity_counts.plot(kind='bar', title="Ethnicity Distribution")
    plt.xlabel("Ethnicity")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("ethnicity_distribution.png")
    plt.close()
