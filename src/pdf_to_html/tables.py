import fitz
import pandas as pd

class PDF():
    def __init__(self, file):
        self.pdf_doc = fitz.open(file)

    def find_table_start(self, pdf_page):
        """Find the position of the table start by detecting 'Header 1'."""
        text_blocks = pdf_page.get_text("blocks")
        for block in text_blocks:
            bbox = block[:4]
            text = block[4].strip()
            if "Header 1" in text:  # Look for a known table keyword
                return bbox[1]  # Return the Y-coordinate of the top of the block
        return None

    def extract_table(self, page_num):
        """Extract the table content starting from the 'Header 1' keyword."""
        pdf_page = self.pdf_doc.load_page(page_num)
        table_start_y = self.find_table_start(pdf_page)

        if table_start_y is None:
            print("Table not found")
            return None

        # Get all text blocks
        text_blocks = pdf_page.get_text("blocks")

        # Extract rows based on proximity
        table_rows = []
        for block in text_blocks:
            bbox = block[:4]
            text = block[4].strip()

            # Only capture text below the table start Y-coordinate and within reasonable vertical distance
            if bbox[1] >= table_start_y:
                table_rows.append(text.split())

        # Create a DataFrame from the extracted rows
        df = pd.DataFrame(table_rows)

        # Clean up DataFrame by setting the first row as header and dropping empty columns
        if not df.empty:
            df.columns = df.iloc[0]
            df = df.drop(0).reset_index(drop=True)
            df = df.dropna(how='all', axis=1)  # Drop empty columns

        return df