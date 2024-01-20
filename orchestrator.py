from adapters.input_adapter import get_questions
from adapters.mpt7b_instruct_adapter import mpt7b_configuraton
from inference.smart_doctor import answer_query
from adapters.output_adapter import persist_generated_responses 
import datetime

current_datetime = datetime.datetime.now()
# Format the date and time as a string
current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
print(f"Orchestration of smart doctor inference starts : {current_datetime_str}")

print("Fetching questions from past day...")
questions_from_past_day = get_questions()
print("Question from past day fetched successfully. Total questions fetched: ", len(questions_from_past_day))

# Create the model and tokenizer for inference
model, tokenizer =  mpt7b_configuraton()

smart_doctor_responses = {}
for question_id, question in questions_from_past_day:
    try:
        print("processing question: ", question_id)
        generated_answer = answer_query(question, model, tokenizer)
        smart_doctor_responses[question_id] = generated_answer
        print("Persisting smart doctor response to database...")
        persist_generated_responses(smart_doctor_responses)
        del smart_doctor_responses[question_id]
    except Exception as answer_generation_exception:
        print("Exception occurred while processing question: ", question_id)
        print("Exception: ", answer_generation_exception)
print("Smart doctor responses generated successfully. Total responses generated: ", len(smart_doctor_responses))

# print("Persisting smart doctor responses to database...")
# persist_generated_responses(smart_doctor_responses)
