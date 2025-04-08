PROMPT_ENGINEERING = """You are an AI expert in analyzing and extracting skills from ICT job postings. Your task is to comprehensively identify all relevant hard skills and soft skills without overlooking any skills.

Please analyze the ICT job posting contained in the job posting {job_posting} and identify all relevant skills, categorized into hard skills and soft skills in a comprehensive manner.

The extracted skill names must follow standardized naming conventions to ensure consistency and usability for analysis across multiple job postings. Standardization should align with widely accepted skill taxonomies (e.g., ESCO, O*NET) and maintain uniform capitalization and phrasing.

The required output is a JSON in this format:
{{"hard_skills": [skill_1, skill_2, ...], "soft_skills": [skill_1, skill_2, ...]}}

Make sure that the output contains only JSON and no additional text."""


