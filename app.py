
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- Set Streamlit Page Config ---
st.set_page_config(
    page_title="Web Scraper Demo App 📚",
    page_icon="📚",
    layout="centered",
)

# --- App Header ---
st.title("📚 Book Scraper Demo")
st.write("Paste a BooksToScrape URL or use the pre-filled one to scrape book titles and prices.")

# --- Pre-filled URL Input ---
default_url = "http://books.toscrape.com/catalogue/category/books_1/page-1.html"
url = st.text_input("Paste the URL of the page you want to scrape:", value=default_url)

# --- Scrape button ---
if st.button("Scrape"):
    if url:
        with st.spinner('Scraping in progress...'):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                books = soup.find_all("article", class_="product_pod")

                data = []
                for book in books:
                    title = book.h3.a["title"]
                    price = book.find("p", class_="price_color").text
                    availability = book.find("p", class_="instock availability").text.strip()
                    data.append({"Title": title, "Price": price, "Availability": availability})

                if data:
                    df = pd.DataFrame(data)
                    st.success(f"Scraped {len(df)} books!")
                    st.dataframe(df)

                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name='scraped_books.csv',
                        mime='text/csv',
                    )
                else:
                    st.warning("No books found on the page. Please check the URL.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please paste a valid URL!")

# --- About This App ---
st.markdown("---")
st.subheader("About this app")
st.write(
    "This demo app showcases live web scraping using Python, BeautifulSoup, "
    "and Streamlit. It extracts book titles and prices from an open site. "
    "Built for educational and portfolio purposes."
)
st.write("Made with ❤️ by Nitin Dhir")
