# -*- coding: utf-8 -*-
"""
Streamlit app for RKEI Parser - Upload DOCX files and download processed Excel
"""

import streamlit as st
import tempfile
from pathlib import Path
from typing import List

# Import the parser function
from rkei_parser import process_files

# Configure page
st.set_page_config(
    page_title="RKEI Parser",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Title and instructions
st.title("📄 RKEI Form Parser")
st.markdown("""
Upload your RKEI .docx forms, click **Process**, and download the Excel summary.

**How to use:**
1. Click "Upload files" below
2. Select one or more .docx files
3. Click the **Process Files** button
4. Download your Excel file when ready
""")

st.divider()

# File uploader
uploaded_files = st.file_uploader(
    "Upload RKEI .docx files",
    type=["docx"],
    accept_multiple_files=True,
    help="Select one or more Word documents (.docx format)"
)

# Process button and logic
if st.button("🔄 Process Files", type="primary", use_container_width=True):
    if not uploaded_files:
        st.error("❌ Please upload at least one .docx file first.")
    else:
        try:
            # Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Write uploaded files to temp directory
                file_paths = []
                for uploaded_file in uploaded_files:
                    file_location = temp_path / uploaded_file.name
                    with open(file_location, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    file_paths.append(str(file_location))
                
                st.info(f"📦 Processing {len(file_paths)} file(s)...")
                
                # Process files with spinner
                with st.spinner("Processing... Please wait."):
                    excel_bytes = process_files(file_paths)
                
                # Verify we got output
                if excel_bytes and len(excel_bytes) > 0:
                    st.success("✅ Files processed successfully!")
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Excel File",
                        data=excel_bytes,
                        file_name="final_output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                else:
                    st.error("❌ Processing returned no output. Please check your files.")
        
        except FileNotFoundError as e:
            st.error(f"❌ File error: {str(e)}")
        except ValueError as e:
            st.error(f"❌ Invalid file format: {str(e)}")
        except Exception as e:
            st.error(f"❌ Processing failed: {str(e)}")
            st.info("💡 Please verify your files are valid RKEI forms and try again.")

st.divider()
st.markdown("*RKEI Parser • Streamlit App*", help="Built with Streamlit")
