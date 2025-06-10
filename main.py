import random
import json
import os
import sys

KEY_FILE_PATH = "key.txt"
MODEL_NAME = "gemini-1.5-flash"

CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
RESET = "\033[0m"


def get_llm_model():
    module_found = False
    try:
        import google.generativeai as genai

        module_found = True
    except:
        pass

    if os.path.exists(KEY_FILE_PATH) and module_found:
        with open(KEY_FILE_PATH, "r") as api_key_file:
            key = api_key_file.read()
        genai.configure(api_key=key)
        return genai.GenerativeModel(MODEL_NAME)
    else:
        return None


def get_questions_file_path(questions_id: str):
    return f"{questions_id}.json"


def get_state_file_path(questions_id: str):
    return f"{questions_id}_state.json"


def get_answers_file_path(questions_id: str):
    return f"{questions_id}_answers.json"


def load_state(questions_id: str):
    state_file_path = get_state_file_path(questions_id)
    with open(state_file_path, "r") as state_file:
        return json.load(state_file)


def load_own_answers(questions_id: str) -> None | dict:
    answers_file_path = get_answers_file_path(questions_id)
    if not os.path.exists(answers_file_path):
        return None
    with open(answers_file_path, "r") as answers_file:
        return json.load(answers_file)


def load_questions(questions_id: str):
    questions_file_path = get_questions_file_path(questions_id)
    with open(questions_file_path, "r", encoding="utf-8") as questions_file:
        return json.load(questions_file)


def dump_state(state: dict, questions_id: str):
    state_file_path = get_state_file_path(questions_id)
    with open(state_file_path, "w") as state_file:
        json.dump(state, state_file, indent=4)


def initialize_state_file(questions_id):
    questions = load_questions(questions_id)
    state = {}
    for topic_id in questions:
        question_count = len(questions[topic_id]["questions"])
        state[topic_id] = [False for _ in range(question_count)]
    dump_state(state, questions_id)


def does_state_file_exist(questions_id: str):
    state_file_path = get_state_file_path(questions_id)
    return os.path.exists(state_file_path)


def mark_question_as_complete(topic_id: str, question_idx: int, questions_id: str):
    state = load_state(questions_id)
    state[topic_id][question_idx] = True
    dump_state(state, questions_id)


def get_own_answer(topic_id: str, question_idx: int, questions_id: str):
    own_answers = load_own_answers(questions_id)
    if own_answers is None:
        return None
    return own_answers[topic_id][question_idx]


def get_random_question_and_mark_as_complete(questions_id: str):
    state = load_state(questions_id)
    unseen_question_tuples = []
    for topic, question_states in state.items():
        for question_state_idx, question_state in enumerate(question_states):
            if not question_state:
                unseen_question_tuples.append((topic, question_state_idx))

    if len(unseen_question_tuples) == 0:
        print(RED + "No questions remaining" + RESET)
        return

    topic_id, question_idx = random.choice(unseen_question_tuples)
    mark_question_as_complete(topic_id, question_idx, questions_id)

    questions = load_questions(questions_id)
    topic_name = questions[topic_id]["topic_name"]
    question_content = questions[topic_id]["questions"][question_idx]

    return topic_id, topic_name, question_content, question_idx


def get_completion_rate(questions_id: str):
    completed_questions = 0
    question_count_total = 0
    state = load_state(questions_id)
    for _, question_states in state.items():
        for question_state in question_states:
            question_count_total += 1
            if question_state:
                completed_questions += 1
    return completed_questions, question_count_total


def prompt_llm(prompt: str, llm_model) -> str:
    try:
        grounded_prompt = (
            "You are going to give a response that will be read in a terminal, so there is no Markdown support. "
            "Your response needs to be easily understandable when read as plain text. "
            f"The question you will reply to is: {prompt}"
        )
        response = llm_model.generate_content(grounded_prompt)
        return response.text
    except Exception as e:
        print(RED + f"Error occurred when prompting LLM:\n{e}" + RESET)


def does_questions_id_exist(questions_id: str):
    questions_file_path = get_questions_file_path(questions_id)
    return os.path.exists(questions_file_path)


if len(sys.argv) == 1:
    print("Please enter an ID for the questions you wish to practice.")
    sys.exit(0)

questions_id = sys.argv[1]
if not (does_questions_id_exist(questions_id)):
    print(f"Questions with ID '{questions_id}' not found.")
    sys.exit(0)

if not does_state_file_exist(questions_id):
    initialize_state_file(questions_id)

llm_model = get_llm_model()

print(f"LLM available? {GREEN + 'Yes' + RESET if llm_model is not None else RED + 'No' + RESET}")
print(f"Questions ID: " + GREEN + questions_id + RESET)

while True:
    try:
        print()
        print(CYAN + "1 - Get question" + RESET)
        print(CYAN + "2 - Get completion rate" + RESET)
        print(CYAN + "3 - Reset state" + RESET)
        print(CYAN + "4 - Exit" + RESET)

        choice = input("")
        if choice == "1":
            result = get_random_question_and_mark_as_complete(questions_id)
            if not result:
                continue
            topic_id, topic_name, question_content, question_idx = result
            print()
            print(f"{YELLOW}Topic #{topic_id}: {topic_name}{RESET}")
            print(YELLOW + question_content + RESET)
            while True:
                print()
                print(CYAN + "1 - Finish question" + RESET)
                print(CYAN + "2 - Get own answer" + RESET)
                print(CYAN + "3 - Get LLM answer" + RESET)
                inner_choice = input("")
                if inner_choice == "1":
                    break
                if inner_choice == "2":
                    own_answer = get_own_answer(topic_id, question_idx, questions_id)
                    if own_answer is not None:
                        print()
                        print(GREEN + own_answer + RESET)
                    else:
                        print(RED + "Own answer not available." + RESET)
                elif inner_choice == "3":
                    if llm_model is not None:
                        chat_gpt_answer = prompt_llm(question_content, llm_model)
                        print()
                        print(GREEN + chat_gpt_answer + RESET)
                    else:
                        print(RED + "LLM not available." + RESET)
                else:
                    print(RED + "Incorrect input detected." + RESET)
        elif choice == "2":
            completed_questions, question_count_total = get_completion_rate(questions_id)
            completion_percent = (completed_questions / float(question_count_total)) * 100
            print(MAGENTA + f"\nCurrent completion rate: {completed_questions}/{question_count_total} ({completion_percent:.1f}%)" + RESET)
        elif choice == "3":
            initialize_state_file(questions_id)
            print(BLUE + "State has been reset." + RESET)
        elif choice == "4":
            break
        else:
            print(RED + "Incorrect input detected." + RESET)
    except KeyboardInterrupt:
        break

print("Exiting...")
