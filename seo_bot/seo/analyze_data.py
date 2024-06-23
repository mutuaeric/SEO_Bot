import re

def categorize_scraped_data(data):
    categories = {
        'URLs': [],
        'Emails': [],
        'Google Maps Links': [],
        'Phone Numbers': [],
        'LinkedIn Profiles': [],
        'Other Links': [],
        'Keywords': []
    }
    
    # Regex patterns for different categories
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    google_maps_pattern = r'^https:\/\/goo\.gl\/maps\/[a-zA-Z0-9]+$'
    phone_pattern = r'^tel:\+\d+$'
    linkedin_pattern = r'^https:\/\/www\.linkedin\.com\/company\/[\w-]+$'
    url_pattern = r'^https?:\/\/[\w\-\.]+\.\w{2,}\/?.*$'
    
    for item in data:
        if re.match(email_pattern, item):
            categories['Emails'].append(item)
        elif re.match(google_maps_pattern, item):
            categories['Google Maps Links'].append(item)
        elif re.match(phone_pattern, item):
            categories['Phone Numbers'].append(item)
        elif re.match(linkedin_pattern, item):
            categories['LinkedIn Profiles'].append(item)
        elif re.match(url_pattern, item):
            categories['URLs'].append(item)
        else:
            categories['Other Links'].append(item)
            
    
    return categories
