from cleanse_data.openai_api import cleanse_query
from prompt.few_shot_prompt_builder import generate_context_for_query

def remove_after_nth_keyword(text):
    keyword="Question:"
    parts = text.split(keyword)
    return keyword.join(parts[:4])

def remove_before_nth_keyword(text):
    keyword="Answer:"
    parts = text.split(keyword)
    return keyword.join(parts[3:])

def remove_after_hash(text):
    parts = text.split("#")
    if len(parts) > 1:
        return parts[0]
    else:
        return text

def answer_query(query, model, tokenizer):

    # Cleanse the query using openAI
    print("Cleansing query...")
    query = cleanse_query(query)

    print("Generating context for prompt...")
    prompt = generate_context_for_query(query).format(input=query)
    prompt = prompt + '\nAnswer:'
    print("Tokenizing prompt...")
    inputs = tokenizer.encode(prompt, return_tensors='pt').to('cuda:0') #prompt = question + "Answer:"
    print("Generating answer...")
    max_length = 1000
    output = model.generate(inputs, max_length=max_length, temperature=0.25, top_p=0.92, do_sample=True, max_new_tokens = 200)
    generated_answer = tokenizer.decode(output[0], skip_special_tokens=True)

    # Cleanse the generated answer hallucination
    print("Cleansing generated answer...")
    generated_answer= remove_before_nth_keyword(generated_answer)
    generated_answer= remove_after_nth_keyword(generated_answer)
    generated_answer= remove_after_hash(generated_answer)
    print(generated_answer)
    return generated_answer
