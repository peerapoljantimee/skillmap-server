import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request
from utils.skill_extractors.prompt import PROMPT_ENGINEERING

# สร้าง Request สำหรับส่งไปยัง API
def create_requests(jobs_data : list, model_config="claude-3-5-haiku-20241022", max_tokens_config = 1024, temperature_config = 0):

   request = []
   for job in jobs_data:
      job_id=str(job.get("job_id"))
      content = job.get("content")
      fomatted_prompt = PROMPT_ENGINEERING.format(job_posting=content)
        
      request.append(Request(
         custom_id=job_id,
         params=MessageCreateParamsNonStreaming(
         model=model_config,
         temperature=temperature_config,
         max_tokens=max_tokens_config,
         messages=[{
            "role": "user",
            "content": fomatted_prompt,
            }]
         )
      ))
      
   return request


