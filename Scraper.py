import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

headers = {
    "User-Agent": "Mozilla/5.0"
}
base_url = "https://sian.monshaat.gov.sa"

all_data = []

def extract_startup_details(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    member_details = soup.find('div', class_='member-details')
    if not member_details:
        return {}

    # Name and Logo
    name = member_details.find('h1').get_text(strip=True)
    logo_tag = member_details.find('div', class_='member--logo').find('img')
    logo_url = logo_tag['src'] if logo_tag else None

    # Tags (stage, sector, business model, team size)
    contact_info = member_details.select('div.contact-member p')
    tags = [p.get_text(strip=True) for p in contact_info]

    email = None
    phone = None
    for p in contact_info:
        link = p.find('a')
        if link:
            if 'mailto:' in link['href']:
                email = link.get_text(strip=True)
            elif 'tel:' in link['href']:
                phone = link.get_text(strip=True)

    # Description
    about = soup.select_one("#pills-tab1 p")
    description = about.get_text(strip=True) if about else ""

    # Services
    services = []
    service_items = soup.select("div.services_pkg div.item")
    for s in service_items:
        title = s.find('h3').get_text(strip=True)
        desc = s.find('p').get_text(strip=True)
        services.append({"title": title, "description": desc})

    return {
        "name": name,
        "logo_url": logo_url,
        "description": description,
        "stage": tags[2] if len(tags) > 2 else None,
        "sector": tags[0] if len(tags) > 0 else None,
        "business_model": tags[1] if len(tags) > 1 else None,
        "team_size": tags[3] if len(tags) > 3 else None,
        "email": email,
        "phone": phone,
        "services": services
    }

# Step 1: Loop through the list pages
for page in range(1, 202):  # 1 to 201
    print(f"Scraping list page {page}...")
    list_url = f"{base_url}/en/startups?page={page}"
    response = requests.get(list_url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Failed to load list page {page}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    member_list = soup.find("div", class_="member-list")

    if not member_list:
        print("  💤 No members found on this page; layout may have changed.")
        continue

    for member in member_list.find_all("div", class_="member-item"):
        a_tag = member.find("a", href=True)
        if not a_tag:
            continue

        profile_url = urljoin(base_url, a_tag["href"])  # full link
        data = extract_startup_details(profile_url)

        if data:                      # skip empty dicts
            all_data.append(data)
        time.sleep(0.5)               # gentle delay per profile

    time.sleep(1)
        
        
        # Visit the startup profile page
        # print(f"  ↳ Scraping profile: {name}")
        # profile_resp = requests.get(href, headers=headers)
        # if profile_resp.status_code != 200:
        #     print(f"    ❌ Failed to load profile for {name}")
        #     continue

        # profile_soup = BeautifulSoup(profile_resp.text, "html.parser")

        
        # # Extract attributes
        # labels = profile_soup.select("div.profile-left .info-item .text")  # Each label text
        # attributes = [lbl.get_text(strip=True) for lbl in labels]

        # stage = attributes[2] if len(attributes) > 2 else ""
        # sector = attributes[0] if len(attributes) > 0 else ""
        # model = attributes[1] if len(attributes) > 1 else ""
        # size = attributes[3] if len(attributes) > 3 else ""
        # email = attributes[4] if len(attributes) > 4 else ""
        # phone = attributes[5] if len(attributes) > 5 else ""

        # about_tag = profile_soup.find("div", class_="about-sec")
        # about = about_tag.get_text(strip=True) if about_tag else ""

        # # Optional: extract services
        # service_boxes = profile_soup.select(".services-box .white-card")
        # services = [s.get_text(strip=True, separator=" | ") for s in service_boxes]
        # services_combined = " || ".join(services)

        # all_data.append({
        #     "Name": name,
        #     "Stage": stage,
        #     "Sector": sector,
        #     "Model": model,
        #     "Size": size,
        #     "Email": email,
        #     "Phone": phone,
        #     "About": about,
        #     "Services": services_combined,
        #     "Profile Link": profile_link
        # })

        # time.sleep(0.5)  # Gentle delay between profiles

    # Delay between list pages

# Save to CSV
if not all_data:
    print("😕 Finished but scraped zero rows – please re‑check selectors.")
    import sys; sys.exit()

with open("sian_startups_detailed.csv", "w",
          newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
    writer.writeheader()
    writer.writerows(all_data)

print(f"✅ Done! Scraped {len(all_data)} startups into 'sian_startups_detailed.csv'")
