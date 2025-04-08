import requests
from bs4 import BeautifulSoup
import time

# Custom User-Agent header to reduce the risk of getting blocked
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

# Base URL with a placeholder for the page number
BASE_URL = "https://www.realtor.com/international/mx/tijuana-baja-california/p{}"

def parse_listing(listing):
    """
    Given a BeautifulSoup tag corresponding to one listing, extract the required fields.
    
    **Note:** Replace the class names below with the actual selectors from the Realtor.com page.
    """
    property_type = listing.find("div", class_="property-type-class")
    property_type = property_type.get_text(strip=True) if property_type else ""
    
    land_size = listing.find("div", class_="land-size-class")
    land_size = land_size.get_text(strip=True) if land_size else ""
    
    rooms = listing.find("div", class_="rooms-class")
    rooms = rooms.get_text(strip=True) if rooms else ""
    
    parking_spaces = listing.find("div", class_="parking-spaces-class")
    parking_spaces = parking_spaces.get_text(strip=True) if parking_spaces else ""
    
    building_size = listing.find("div", class_="building-size-class")
    building_size = building_size.get_text(strip=True) if building_size else ""
    
    address = listing.find("div", class_="address-class")
    address = address.get_text(strip=True) if address else ""
    
    price = listing.find("span", class_="price-class")
    price = price.get_text(strip=True) if price else ""
    
    return {
        "Property Type": property_type,
        "Land Size": land_size,
        "Rooms": rooms,
        "Parking Spaces": parking_spaces,
        "Building Size": building_size,
        "Address": address,
        "Price": price,
    }

def scrape_page(page_number):
    """
    Fetch a single page and return a list of dictionaries—one per listing.
    """
    url = BASE_URL.format(page_number)
    print(f"Scraping page {page_number}: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching page {page_number}: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all listing elements on the page.
    # Adjust the selector below after inspecting the actual page structure.
    listings = soup.find_all("div", class_="component_property-card")
    
    page_results = []
    for listing in listings:
        data = parse_listing(listing)
        page_results.append(data)
    
    return page_results

def main():
    all_listings = []
    
    # Loop through pages 1 to 160
    for page in range(1, 5):
        listings = scrape_page(page)
        all_listings.extend(listings)
        # Be polite: wait a second between requests
        time.sleep(1)
    
    # Write the scraped data to a Markdown file as a table
    md_filename = "real_estate_listings.md"
    with open(md_filename, "w", encoding="utf-8") as mdfile:
        # Write a header for the Markdown file
        mdfile.write("# Real Estate Listings\n\n")
        
        # Write the table header
        headers = ["Property Type", "Land Size", "Rooms", "Parking Spaces", "Building Size", "Address", "Price"]
        mdfile.write("| " + " | ".join(headers) + " |\n")
        mdfile.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        
        # Write a row for each listing
        for listing in all_listings:
            # Escape pipe characters in the data if necessary
            row = "| " + " | ".join(listing.get(header, "").replace("|", "\\|") for header in headers) + " |\n"
            mdfile.write(row)
    
    print(f"Data written to {md_filename}")

if __name__ == "__main__":
    main()
