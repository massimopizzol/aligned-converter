import pandas as pd

def validate_df(df):
    # Field check.
    database = df["Activity database"].unique().tolist()
    if len(database) > 1:
        print("Reminder: 'Activity database' column should only include name of your database.")

    # Check exchanges are defined.
    exchange_db = df[df['Exchange database'] == database[0]].copy()
    undefined_inputs = exchange_db[~exchange_db["Exchange input"].isin(df["Activity code"])]
    if len(undefined_inputs["Exchange input"].unique()) > 0:
        print(f"Reminder: {undefined_inputs["Exchange input"].tolist()} are undefined in your csv file. \n", 
              "Please check:\n"
                 "1. Did you fill 'Exchange input' cell for each exchange? \n"
                 "2. Did you define the 'Activity code' before you use it as the exchange input? \n"
                 "3. Did you spell exactly as what you defined in 'Activity code' column.")

    # Check all defined activities is used.
    empty_exchanges = df[df["Exchange input"].isna()].copy()
    acts = empty_exchanges["Activity code"].unique()
    unused_acts = [act for act in acts if act not in df["Exchange input"].values]
    if len(unused_acts) > 0:
        print(f"Reminder: {unused_acts} is defined but not used in your foreground system.")


if __name__ == "__main__":
    # Enter your csv file name (should be in the same directory as the script)
    csv_file = "test_db_excel_w_ecoinvent.csv"
    df = pd.read_csv(csv_file)
    validate_df(df)