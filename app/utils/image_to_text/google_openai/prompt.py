# utils\image_to_text\google_openai\prompt.py
PROMPT_ENGINEERING = """
You are an advanced parser for job postings. Given the OCR result from a job advertisement image:

\"\"\"
{ocr_text}
\"\"\"

Extract and format the data strictly as the JSON structure provided below.

Requirements:
- Respond with JSON only, no extra explanation or markdown.
- If information is missing or unclear, set its value as null.
- Do not infer or hallucinate values.

JSON format:

{{
  "basicInfo": {{
    "title": null
  }},
  "salary": {{
    "min_salary": null,
    "max_salary": null
  }},
  "location": {{
    "area": null,
    "city": null,
    "country": null
  }},
  "content": null
}}
"""
# .format(google_vision_ocr_text)