import os
import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path="bookings.csv"):
    if not os.path.exists(file_path):
        # Also check current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        alt_path = os.path.join(script_dir, file_path)
        if os.path.exists(alt_path):
            file_path = alt_path
        else:
            print(f"Error: File '{file_path}' not found.")
            return None

    try:
        raw_df = pd.read_csv(file_path, dtype=str)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    valid_rows = []
    for _, row in raw_df.iterrows():
        pnr = str(row["PNR"]).strip()
        train = str(row["Train"]).strip()
        t_class = str(row["Class"]).strip()
        fare_raw = str(row["Fare"]).strip()
        status = str(row["Status"]).strip()

        try:
            fare = float(fare_raw)
            if fare < 0:
                print(f"Warning: Row with PNR {pnr} skipped - invalid fare.")
                continue
        except ValueError:
            print(f"Warning: Row with PNR {pnr} skipped - invalid fare.")
            continue

        valid_rows.append([pnr, train, t_class, fare, status])

    df = pd.DataFrame(valid_rows, columns=["PNR", "Train", "Class", "Fare", "Status"])
    return df

def show_revenue_per_train(df):
    confirmed_df = df[df["Status"].str.lower() == "confirmed"]
    grouped = confirmed_df.groupby("Train")["Fare"].sum().reset_index()
    grouped.columns = ["Train", "Revenue"]
    grouped = grouped.sort_values(by=["Revenue", "Train"], ascending=[False, True])

    for _, row in grouped.iterrows():
        print(f"{row['Train']} : Rs. {int(row['Revenue'])}")
    total_rev = int(grouped["Revenue"].sum())
    print(f"Total confirmed revenue: Rs. {total_rev}")

    # Display Matplotlib Bar Chart
    plt.figure(figsize=(5, 4))
    plt.bar(grouped["Train"], grouped["Revenue"], color="forestgreen", width=0.4)
    plt.title("Revenue per Train (Confirmed Only)")
    plt.xlabel("Train")
    plt.ylabel("Revenue (Rs.)")
    plt.tight_layout()
    plt.show()

def show_bookings_per_train(df):
    grouped = df.groupby("Train")["PNR"].count().reset_index()
    grouped.columns = ["Train", "Count"]
    grouped = grouped.sort_values(by=["Count", "Train"], ascending=[False, True])

    for _, row in grouped.iterrows():
        print(f"{row['Train']} : {row['Count']}")
    print(f"Total bookings: {len(df)}")

    plt.figure(figsize=(5, 4))
    plt.bar(grouped["Train"], grouped["Count"], color="steelblue", width=0.4)
    plt.title("Bookings per Train")
    plt.xlabel("Train")
    plt.ylabel("Number of Bookings")
    plt.tight_layout()
    plt.show()

def main():
    df = load_data("bookings.csv")
    if df is None or df.empty:
        return

    while True:
        print("\n--- Railway Reservation Analyzer ---")
        print("1. Bookings per train")
        print("2. Revenue per train (Confirmed only)")
        print("3. Exit")

        choice = input("Select an option: ").strip()

        if choice == "2":
            show_revenue_per_train(df)
        elif choice == "1":
            show_bookings_per_train(df)
        elif choice == "3":
            print("Exiting.")
            break
        else:
            print("Invalid choice, please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
