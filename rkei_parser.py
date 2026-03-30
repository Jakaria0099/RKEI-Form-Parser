def process_files(file_paths):
    import pandas as pd
    import docx
    from io import BytesIO

    # Collect DataFrames extracted from all .docx files
    frames = []

    for path in file_paths:
        doc = docx.Document(path)
        for table in doc.tables:
            rows = [[cell.text for cell in row.cells] for row in table.rows]
            if len(rows) >= 1:
                df = pd.DataFrame(rows[1:], columns=rows[0])
                frames.append(df)

    # Combine all DataFrames
    all_data = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    # Convert DataFrame to Excel bytes
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        all_data.to_excel(writer, index=False)
    output.seek(0)

    return output.read()  # Return the Excel bytes