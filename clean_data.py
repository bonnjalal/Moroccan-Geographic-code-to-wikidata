import pandas as pd


def process_excel(input_file, output_file):
    """Processes an Excel sheet to extract administrative divisions from names.

    Args:
        input_file: Path to the input Excel file.
        output_file: Path to save the processed Excel file.
    """
    try:
        df = pd.read_excel(input_file)  # Read the Excel file into a DataFrame

        # Create a new column 'Administrative Division' initialized with empty strings
        df["Administrative Division"] = ""
        df["Administrative Division fr"] = ""

        keywords = ["جماعة", "دائرة", "إقليم", "جهة", "عمالة", "مقاطعة"]
        keywords_fr = [
            "Région",
            "Commune",
            "Arrondissement",
            "Cercle",
            "Préfecture",
            "Province",
        ]

        for index, row in df.iterrows():
            name = row["name"]
            name_fr = row["name_fr"]
            for keyword in keywords:
                if keyword in name:
                    df.loc[index, "name"] = name.replace(
                        keyword, ""
                    ).strip()  # Remove Keyword and extra spaces
                    df.loc[index, "Administrative Division"] += (
                        keyword + " "
                    )  # Add keyword to the new column

            df.loc[index, "Administrative Division"] = df.loc[
                index, "Administrative Division"
            ].strip()  # Remove trailing space

            for keyword in keywords_fr:
                if keyword in name_fr:
                    df.loc[index, "name_fr"] = name_fr.replace(
                        keyword, ""
                    ).strip()  # Remove Keyword and extra spaces
                    df.loc[index, "Administrative Division fr"] += (
                        keyword + " "
                    )  # Add keyword to the new column

            df.loc[index, "Administrative Division fr"] = df.loc[
                index, "Administrative Division fr"
            ].strip()  # Remove trailing space

        df.to_excel(
            output_file, index=False
        )  # Save the updated DataFrame to a new Excel file
        print(f"Processed Excel file saved to: {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage (replace with your file paths)
input_file = "input_data.xlsx"
output_file = "output_data.xlsx"
process_excel(input_file, output_file)
