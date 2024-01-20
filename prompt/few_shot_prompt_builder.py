from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from semantic_search.similarity_search import get_results

def generate_context_for_query(query):
    top_matches = get_results(query) #refers to semantic_search

    prompt = PromptTemplate(input_variables=["question", "answer"], template="Question: {question}\nAnswer: {answer}")

    prompt = FewShotPromptTemplate(
    examples=top_matches, 
    example_prompt=prompt, 
    suffix="Question: {input}", 
    input_variables=["input"]
    )

    return prompt
