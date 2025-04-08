import html2text
from utils.simplified.extract import extract_salary_range

def transform_job_data_utils(data):
    transformed_data = []

    for job in data:
        job_id = job["jobDetails"]["job"]["id"] if job["jobDetails"]["job"]["id"] else None
        # print(job_id)
        title = job["jobDetails"]["job"]["title"] if job["jobDetails"]["job"]["title"] else None
        job_type = job["jobDetails"]["job"]["workTypes"]["label"] if job["jobDetails"]["job"]["workTypes"] else None
        status = job["jobDetails"]["job"]["status"] if job["jobDetails"]["job"]["status"] else None
        posted_date = job["jobDetails"]["job"]["listedAt"]["dateTimeUtc"] if job["jobDetails"]["job"]["listedAt"] else None
        expiry_date = job["jobDetails"]["job"]["expiresAt"]["dateTimeUtc"] if job["jobDetails"]["job"]["expiresAt"] else None

        # Salary extraction
        salary_range = extract_salary_range(
                job["jobDetails"]["job"]["salary"]["label"] if job["jobDetails"]["job"]["salary"] else None
        ),


        # Classification extraction
        main_category_id = job["jobDetails"]["job"]["tracking"]["classificationInfo"]["classificationId"] if job["jobDetails"]["job"]["tracking"]["classificationInfo"] else None
        main_category_name = job["jobDetails"]["job"]["tracking"]["classificationInfo"]["classification"] if job["jobDetails"]["job"]["tracking"]["classificationInfo"] else None
        sub_category_id = job["jobDetails"]["job"]["tracking"]["classificationInfo"]["subClassificationId"] if job["jobDetails"]["job"]["tracking"]["classificationInfo"] else None
        sub_category_name = job["jobDetails"]["job"]["tracking"]["classificationInfo"]["subClassification"] if job["jobDetails"]["job"]["tracking"]["classificationInfo"] else None      

        # Location extraction
        area = job["jobDetails"]["job"]["tracking"]["locationInfo"]["area"] if job["jobDetails"]["job"]["tracking"]["locationInfo"] else None
        city = job["jobDetails"]["gfjInfo"]["location"]["state"] if job["jobDetails"]["gfjInfo"]["location"] else None
        country = job["jobDetails"]["gfjInfo"]["location"]["country"] if job["jobDetails"]["gfjInfo"]["location"] else None

        # Company Info
        company_name = job["jobDetails"]["job"]["advertiser"]["name"] if job["jobDetails"]["job"]["advertiser"] else None
        company_id = job["jobDetails"]["job"]["advertiser"]["id"] if job["jobDetails"]["job"]["advertiser"] else None
        shortName = job["jobDetails"]["companyProfile"]["name"] if job["jobDetails"]["companyProfile"] else None
        industry = job["jobDetails"]["companyProfile"]["overview"]["industry"] if job["jobDetails"]["companyProfile"]else None
        max_size_label = job["jobDetails"]["companyProfile"]["overview"]["size"]["description"] if job["jobDetails"]["companyProfile"] else None
        registrationDate = job["jobDetails"]["job"]["advertiser"]["registrationDate"]["dateTimeUtc"] if job["jobDetails"]["job"]["advertiser"] else None
        isVerified = job["jobDetails"]["job"]["advertiser"]["isVerified"] if job["jobDetails"]["job"]["advertiser"] else None
   
        # Content Extraction
        content = html2text.html2text(job["jobDetails"]["job"]["content"])
        
        # Link
        shareLink = job["jobDetails"]["job"]["shareLink"] if job["jobDetails"]["job"]["shareLink"] else None
        companySearchUrl = job["jobDetails"]["companySearchUrl"] if job["jobDetails"]["companySearchUrl"] else None

        # Prepare transformed data
        transformed_data.append({
            "jobId": job_id,
            "basicInfo": {
                "title": title,
                "type": job_type,
                "status": status,
                "postedDate": posted_date,
                "expiryDate": expiry_date
            },
            "salary": salary_range[0],
            "classification": {
                "mainCategory": {
                    "id": main_category_id, 
                    "name": main_category_name
                },
                "subCategory": {
                    "id": sub_category_id, 
                    "name": sub_category_name
                }
            },
            "location": {
                "area": area,
                "city": city,
                "country": country
            },
            "company": {
                "id": company_id,
                "name": company_name,
                "shortName": shortName,
                "industry": industry,
                "max_size": max_size_label,
                "registrationDate": registrationDate,
                "isVerified": isVerified
            },
            "content": content,
            "shareLink": shareLink,
            "companySearchUrl": companySearchUrl
        })

    return transformed_data