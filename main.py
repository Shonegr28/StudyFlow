import pandas as pd
from datetime import datetime
from data_entry import get_date, get_hours, get_category, get_description
import csv
import matplotlib.pyplot as plt 


class CSV:
    CSV_FILE = "Student_life_tracker.csv"
    COLUMNS = ["date", "category", "description", "hours"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        """Initializes the CSV file if it doesn't exist."""
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date: str, category: str, description: str, hours: float) -> None:
        """Adds a new entry to the CSV file."""
        new_entry = {
            "date": date,
            "category": category,
            "description": description,
            "hours": hours
        }
        try:
            with open(cls.CSV_FILE, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
                writer.writerow(new_entry)
            print("Entry added successfully")
        except Exception as e:
            print(f"An error occurred while adding the entry: {e}")

    @classmethod
    def get_data(cls, start_date: str, end_date: str):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format= CSV.FORMAT)
        start_date =datetime.strptime(start_date, CSV.FORMAT )
        end_date =datetime.strptime(end_date, CSV.FORMAT )
        mask = (df["date"]>= start_date) & (df["date"] <= end_date)
        filtered_df=df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range")
        else:
            print(f"Student time tracked from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)}))

            total_study_hours = filtered_df[filtered_df["category"] == "Study"]["hours"].sum()
            total_relaxation_hours = filtered_df[filtered_df["category"] == "Relaxation"]["hours"].sum()

            # Convert total hours to hours and minutes format
            def format_hours(total_hours: float) -> str:
                hours = int(total_hours)
                minutes = int((total_hours - hours) * 60)
                return f"{hours} hrs {minutes} mins"

            print("\nSummary: ")
            print(f"Total Study: {format_hours(total_study_hours)}")
            print(f"Total Relaxation: {format_hours(total_relaxation_hours)}")

        return filtered_df

    
def add():
    CSV.initialize_csv()
    date= get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    category = get_category()
    description = get_description()
    hours = get_hours()
    CSV.add_entry(date, category, description, hours)

# CSV.get_data("01-01-2024", "25-09-2024")

def plot_transactions(df):
    df.set_index('date', inplace=True)
    income_df = (df[df["category"] == "Study"].resample("D").sum().reindex(df.index, fill_value=0))
    expense_df = (df[df["category"] == "Relaxation"].resample("D").sum().reindex(df.index, fill_value=0))

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["hours"], label="Study", color="g")
    plt.plot(expense_df.index, expense_df["hours"], label="Relaxation", color="r")
    plt.xlabel("Date")
    plt.ylabel("Hours")
    plt.title("StudyFlow Chart")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add a new Entry")
        print("2. View Study and Relaxation Entry and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_data(start_date, end_date)
            if input("Do you want to see a plot? (y/n)").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
