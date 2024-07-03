from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema


from dotenv import load_dotenv
import json

load_dotenv()


llm = ChatOpenAI(model="gpt-3.5-turbo-0125")


def __get_parser():
    schema = [
        ResponseSchema(
            name='suitability', description="How suitable this job is to the candidate."),
    ]
    return StructuredOutputParser.from_response_schemas(schema)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a job matching assistant that evaluates job descriptions for their suitability to a given candidate. You will be provided with a job's {title}, {description}, and {requirement}, and you will determine if the job is relevant to the given {candidate}. The criteria for determining relevance include the candidate's years of experience and toolset proficiency. Remove any job that requires more than 1 year of experience.

            Provide a single integer percentage indicating how relevant this job is to the candidate, with 100 being the most suitable and 0 being the least suitable. If the job requires more than 1 year of experience, mark it as irrelevant.

            Output your response in JSON format with a sample response as follows:
                "suitability": number
            """,
        )
    ]
)

chain = prompt | llm


with open('data/raw/itviec_jobs.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Iterate over each job entry in the list
for job in data:
    title = job['title']
    description = job['descriptions']
    requirement = job['requirements']

    # Call the `chain.invoke` function with the relevant data
    relevancy = chain.invoke(
        {
            "title": title,
            "description": description,
            "requirement": requirement,
            "candidate": 'Junior data analyst who has less than 1 year experience with Python, SQL, Tableau and Power BI'
        }
    )

    # Parse the suitability score from the relevancy response
    suitability = __get_parser().parse(relevancy.content)['suitability']

    # Add the relevancy score to the job entry
    job['suitability'] = suitability

with open('data/processed/itviec_jobs_with_relevancy2.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
