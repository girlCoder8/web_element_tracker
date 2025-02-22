import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from utils import extract_locators, save_to_json, save_to_csv
from styles import apply_styles
import time

def main():
    # Apply custom styles
    apply_styles()

    st.title("Web Element Locator Extractor")
    st.markdown("""
    Extract web element locators from any webpage. Enter a URL below to get:
    - IDs
    - Names
    - Data-testids
    - Links & URLs
    - Buttons
    - Class Names
    - Accessibility Attributes
    - CSS Selectors
    - XPath Locators
    """)

    # URL input
    url = st.text_input("Enter Website URL", placeholder="https://example.com")

    if url:
        try:
            with st.spinner("Fetching webpage content..."):
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

            # Extract locators with progress bar
            progress_bar = st.progress(0)
            locators = extract_locators(soup, progress_bar)

            if not any(len(v) > 0 for v in locators.values()):
                st.warning("No locators found on the specified webpage.")
                return

            # Convert to DataFrame for display
            df = pd.DataFrame({
                'Type': [],
                'Locator': [],
                'Element': []
            })

            for locator_type, elements in locators.items():
                for element in elements:
                    df = pd.concat([df, pd.DataFrame({
                        'Type': [locator_type],
                        'Locator': [element['locator']],
                        'Element': [element['element']]
                    })], ignore_index=True)

            # Display results
            st.subheader("Found Locators")
            st.dataframe(df, use_container_width=True)

            # Export options
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Export to JSON"):
                    json_string = save_to_json(locators)
                    st.download_button(
                        label="Download JSON",
                        file_name="locators.json",
                        mime="application/json",
                        data=json_string
                    )

            with col2:
                if st.button("Export to CSV"):
                    csv_string = save_to_csv(df)
                    st.download_button(
                        label="Download CSV",
                        file_name="locators.csv",
                        mime="text/csv",
                        data=csv_string
                    )

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching the webpage: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()