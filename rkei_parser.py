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
            if len(rows) >= 2:
                headers = rows[0]
                num_cols = len(headers)
                normalized = []
                for row in rows[1:]:
                    if len(row) < num_cols:
                        row = row + [''] * (num_cols - len(row))
                    elif len(row) > num_cols:
                        row = row[:num_cols]
                    normalized.append(row)
                if normalized:
                    # Deduplicate column names to prevent concat reindex errors
                    seen = {}
                    unique_headers = []
                    for h in headers:
                        if h in seen:
                            seen[h] += 1
                            unique_headers.append(f"{h}_{seen[h]}")
                        else:
                            seen[h] = 0
                            unique_headers.append(h)
                    df = pd.DataFrame(normalized, columns=unique_headers)
                    frames.append(df)

    # Combine all DataFrames
    all_data = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    # Convert DataFrame to Excel bytes
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        all_data.to_excel(writer, index=False)
    output.seek(0)

    return output.read()  # Return the Excel bytes