def process_files(file_paths):
    import pandas as pd
    from io import BytesIO

    # Create an empty DataFrame to aggregate all Excel data
    all_data = pd.DataFrame()

    for path in file_paths:
        # Read the Excel file
        excel_data = pd.read_excel(path)
        # Append the data to the all_data DataFrame
        all_data = all_data.append(excel_data, ignore_index=True)

    # Convert DataFrame to Excel bytes
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        all_data.to_excel(writer, index=False)
    output.seek(0)

    return output.read()  # Return the Excel bytes