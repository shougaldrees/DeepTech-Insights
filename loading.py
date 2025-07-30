import csv, json, ast

CSV_FILE  = "sian_startups_detailed.csv"
JSON_FILE = "loaded_data.json"

def convert_csv_to_json_sian(csv_path: str, json_path: str) -> None:

    all_startups = []

    #clean "name" 
    with open(csv_path, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            raw_services = row.get("services", "").strip()

            try:                          
                services = ast.literal_eval(raw_services)
                assert isinstance(services, list)
            except Exception:               
                services = [
                    {
                        "title": part.split(":")[0].strip(),
                        "description": part.split(":")[1].strip()
                                      if ":" in part else ""
                    }
                    for part in raw_services.split(";") if part.strip()
                ]

            startup = {
                "company_name":          row.get("name", "").strip(),
                "Description":           row.get("description", "").strip(),
                "team_size":             row.get("team_size", "").strip(),
                "services":              services,

                
                "website_url": "",
                "cr_number": "",
                "date_established": "",
                "hq_country": "SA",
                "hq_operating_city": "",
                "company_origin": "Saudi Entity",
                "founder_names": [],
                "contact_email":        row.get("email", "").strip(),
                "contact_number":       row.get("phone", "").strip(),
                "cto_name": "",
                "is_DeepTech": False,
                "is_AdvancedTech": False,
                "r_and_d_dependency": "",
                "annual_r_and_d_spend_pct": "",
                "r_and_d_funding_pct": "",
                "revenue_from_r_and_d_pct": "",
                "main_innovation_challenges": [],
                "r_and_d_specific_challenges": [],
                "innovation_products": [],
                "funding_stage":         row.get("stage", "").strip(),
                "total_funding_raised_sar": 0,
                "number_of_rounds": 0,
                "rounds_breakdown": 0, #refine
                "currently_raising": False,
                "funding_sources": [],
                "last_funding_date": "",
                "ip_status": "",
                "ip_type": "",
                "ip_count": 0,
                "ip_support_needed": "",
                "rdia_relationship": [], #refine
                "external_relationships": False,
                "relationship_type": [],
                "relationship_names": "",
                "national_priority_focus": [],
                "sector":               row.get("sector", "").strip(),
                "sub-sector": "",
                "sector_label": {
                    "MAGNiiT": "",
                    "Monshaat": row.get("sector", "").strip()
                },
                "core_technology": "",
                "sustainability_contribution": "",
                "social_impact": "",
                "operating_status": "",
                "last_verified_date": "",
                "data_source": "Monshaat (SIAN)",
                "engagements_received": 0,
                "quality_index": 0,
                "engagement_score": None,
                "engagement_feedback": ""
            }

            all_startups.append(startup)

    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_startups, f, indent=2, ensure_ascii=False)

    print(f"Converted {len(all_startups)} startups → {json_path}")

if __name__ == "__main__":
    convert_csv_to_json(CSV_FILE, JSON_FILE)
