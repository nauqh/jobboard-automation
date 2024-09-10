import instructor
from pydantic import BaseModel, Field
from openai import OpenAI
from enum import Enum
import os
import json


class JobRelevance(str, Enum):
    """Enumeration of job relevance to the candidate."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    IRRELEVANT = "irrelevant"


class Reply(BaseModel):
    relevancy: JobRelevance = Field(
        description="The relevance of the job to the candidate, with levels of high, medium, low, and irrelevant")
    reason: str = Field(
        description="Why do you think this job is relevant/irrelevant to the candidate")


class JobEvaluator:
    def __init__(self):
        self.client = instructor.from_openai(OpenAI())

    def __get_content(self):
        return """
        You are a job matching assistant that evaluates job descriptions and requirements for their suitability to a given candidate. You will be provided with a job's {title}, {description}, and {requirement}, and you will determine if the job is relevant to the given {candidate}. 

        There are 4 levels of job relevancy to the candidate: high, medium, low, and irrelevant:
            - High: the job is highly relevant to the candidate. The candidate's skills, experience, and qualifications align closely with the job's requirements, making them a strong match for the position.
            - Medium: the job may be relevant to the candidate. There is some requirement that is not fully aligned with the candidate's profile, but the candidate can learn or adapt to it in a short period of time since it is related to the candidate's existing skill set.
            - Low: the job is only marginally relevant to the candidate. The position might require skills or experience that the candidate does not possess or is only vaguely related to their background. The candidate may need significant upskilling or retraining to be a good fit.
            - Irrelevant: the job is not suitable for the candidate. The skills, experience, or qualifications required for the job do not align with the candidate's profile, making them an unlikely match for the position.

        The criteria for determining relevance include the candidate's years of experience and toolset proficiency. If the job requires more than 2 years of experience, mark it as irrelevant.
        """

    def evaluate_job(self, job: dict, candidate: str) -> Reply:
        content = self.__get_content()

        title, description, requirement = job['title'], job['descriptions'], job['requirements']

        reply = self.client.chat.completions.create(
            model="gpt-4o-mini",
            response_model=Reply,
            messages=[
                {
                    "role": "system",
                    "content": content,
                },
                {
                    "role": "user",
                    "content": f"""Hi there, please validate this job for me.
                    "title": {title},
                    "description": {description},
                    "requirement": {requirement},
                    "candidate": "{candidate}""",
                },
            ],
        )
        return reply


def process_jobs(jobs_file, output_file, candidate):
    with open(jobs_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for job in data:
        resp = evaluator.evaluate_job(job, candidate)
        job['relevancy'] = resp.relevancy.value
        job['reason'] = resp.reason
        job['tag'] = 'data' if 'ds' in jobs_file else 'fsw'

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


if __name__ == '__main__':
    evaluator = JobEvaluator()

    # Use a dictionary to map filenames to their corresponding candidates
    files_to_process = {
        'ds_jobs': 'ds',
        'fsw_jobs': 'fsw'
    }

    with open('profile.json', 'r') as file:
        candidates = json.load(file)

    # Iterate over the files and process them
    for filename, candidate_key in files_to_process.items():
        input_file = os.path.join('data/raw', f"{filename}.json")
        output_file = os.path.join('data/processed', f"{filename}.json")
        candidate = candidates[candidate_key]

        process_jobs(input_file, output_file, candidate)

    # # NOTE: Filter relevant jobs
    # with open('data/processed/ds_jobs.json', 'r', encoding='utf-8') as file:
    #     jobs = json.load(file)
    #     relevant_jobs = [
    #         job for job in jobs if job['relevancy'] != "irrelevant"]

    # with open('data/filter/ds_jobs.json', 'w', encoding='utf-8') as file:
    #     json.dump(relevant_jobs, file, ensure_ascii=False)
