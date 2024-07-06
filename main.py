from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv
import json

load_dotenv()


class JobMatchingAssistant:
    def __init__(self, model="gpt-3.5-turbo-0125"):
        self.llm = ChatOpenAI(model=model)
        self.prompt = self.__create_prompt()
        self.chain = self.prompt | self.llm

    def __create_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a job matching assistant that evaluates job descriptions for their suitability to a given candidate. You will be provided with a job's {title}, {description}, and {requirement}, and you will determine if the job is relevant to the given {candidate}. The criteria for determining relevance include the candidate's years of experience and toolset proficiency. Remove any job that requires more than 2 years of experience.

                    Provide a single integer percentage indicating how relevant this job is to the candidate, with 100 being the most suitable and 0 being the least suitable. If the job requires more than 2 years of experience, mark it as irrelevant.

                    Output your response in JSON format with a sample response as follows:
                        "suitability": number
                    """,
                )
            ]
        )

    def __get_parser(self):
        schema = [
            ResponseSchema(
                name='suitability', description="How suitable this job is to the candidate."
            ),
        ]
        return StructuredOutputParser.from_response_schemas(schema)

    def evaluate_job_suitability(self, job, candidate):
        title = job['title']
        description = job['descriptions']
        requirement = job['requirements']

        relevancy = self.chain.invoke(
            {
                "title": title,
                "description": description,
                "requirement": requirement,
                "candidate": candidate['DS']
            }
        )

        # Parse the suitability score from the relevancy response
        suitability = self.__get_parser().parse(
            relevancy.content)['suitability']

        return suitability

    def process_jobs(self, jobs_file, candidate_file, output_file):
        with open(jobs_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        with open(candidate_file, 'r') as file:
            candidate = json.load(file)

        # Iterate over each job entry in the list
        for job in data:
            job['suitability'] = self.evaluate_job_suitability(job, candidate)

        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    assistant = JobMatchingAssistant()
    assistant.process_jobs('data/raw/linkedin_jobs.json',
                           'data/profile.json',
                           'data/processed/linkedin_jobs_with_relevancy2.json')
