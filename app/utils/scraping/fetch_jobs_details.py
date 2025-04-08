# app\utils\scraping\fetch_jobs_details.py

from utils.scraping.config import *
import requests
import json
# from rich import print


def _make_request(method: str, url: str, **kwargs):
    try:
        response = requests.request(method, url, **kwargs)
        return response.json()
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return None


def fetch_job_details_utils(jobId: int):
    """Fetch details information for job"""
    
    try:
        # print(f"[cyan]Fetching details[/cyan] jobId: [green]{jobId}[/green]")
        variables = {
            "jobId": jobId,
            "jobDetailsViewedCorrelationId": "828ad57a-f0dd-4efc-a9f8-b250d4aedb1d",
            "sessionId": "6e19340b-19ca-4494-b3fb-f2becdc11085",
            "zone": "asia-3",
            "locale": "en-TH",
            "languageCode": "en",
            "countryCode": "TH",
            "timezone": "Asia/Bangkok",
        }

        body = {
            "operationName": "jobDetails",
            "variables": variables,
            "query": JOB_DETAIL_QUERY,
        }

        jobDetails = _make_request("POST", DETAIL_ENDPOINT, json=body)
        # print("[green]Completed[/green]")
        return jobDetails
     
    except Exception as e:
        return {"status": "error", "message": str(e)}


# if __name__ == "__main__":

#     jobIds = {
#         "jobId": [
#             "82298206",
#             "82045263",
#             # "82306582",
#             # "81960869",
#             # "82204680",
#             # "82171475",
#         ]
#     }

#     jobsDetails = []
#     for jobId in jobIds["jobId"]:
#         jobDetails = fetch_job_details(jobId)
#         if jobDetails:
#             jobsDetails.append(jobDetails["data"])

#     print(len({"data": jobsDetails}))
#     with open("jobDetails_data.json", "w") as file:
#         json.dump({"data": jobsDetails}, file, indent=4)

   # python -m app.utils.scraping.fetch_jobs_details
