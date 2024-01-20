from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import Chroma

def get_results(query):
    print("Loading documents into Chroma...")
    embedding_function = HuggingFaceInstructEmbeddings(model_name="all-MiniLM-L6-v2")
    chroma_db = Chroma(persist_directory="./", embedding_function=embedding_function)

    # query it
    print("Performing similarity search...")
    matching_results = chroma_db.similarity_search(query, k=5)
    
    sorted_results=[]
    for result in matching_results:
        sorted_results.append(result.page_content)
    
    sorted_results = sorted(sorted_results, key=len)

    # Store the top 3 strings (shortest) in a new list
    reduced_results = sorted_results[3:]
    # format the results
    formatted_results = []

    for result in reduced_results:
        prompt, completion = result.split("\n", 1)
        prompt = prompt.replace("query: ", "")
        completion = completion.replace("answer: ", "").strip()

        formatted_results.append({
            "question": prompt,
            "answer": completion,
        })

    print("Done performing similarity search.")
    return formatted_results
