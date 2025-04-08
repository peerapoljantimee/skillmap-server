# app\utils\scraping\fetch_jobs_card.py

from utils.scraping.config import *
import requests
import json
from rich import print


def _make_request(method: str, url: str, **kwargs):
    try:
        response = requests.request(method, url, **kwargs)
        return response.json()
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return None


def fetch_jobs_card_utils(classification_id, subclassification_id):
    """Fetch job cards and extract job IDs."""
    try:
        job_ids = []
        job_cards = []
        page = 1

        while True:
            params = {
                **SEARCH_PARAMS,
                "page": page,
                "classification": classification_id,
                "subclassification": subclassification_id,
            }

            data = _make_request("GET", SEARCH_ENDPOINT, params=params)

            if not data or data.get("status") == 400:
                break

            jobs = data.get("data", [])
            if not jobs:
                # print(
                #     f"[yellow]⚠ No jobs found on page {page}. The search has ended[/yellow]"
                # )
                break

            new_job_ids = [
                job["solMetadata"]["jobId"]
                for job in jobs
                if job["solMetadata"].get("jobId")
            ]
            job_ids.extend(new_job_ids)
            job_cards.extend(jobs)

            # print(
            #     f"[cyan]📄 Page {page}:[/cyan] Found [green]{len(new_job_ids)}[/green] jobs"
            # )
            page += 1

        return {"jobId": job_ids}, {"data": job_cards}

    except Exception as e:
        return {"status": "error", "message": str(e)}


# if __name__ == "__main__":
#     job_ids, job_cards = fetch_jobs_card_utils(6281, 6288)

#     with open("job_cards.json", "w") as file:
#         json.dump(job_cards, file, indent=4)

#     with open("job_ids.json", "w") as file:
#         json.dump(job_ids, file, indent=4)
