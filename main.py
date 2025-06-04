import random
import json
import os

MAX_TIME_PR_QUESTION_S = 300
STATE_FILE_PATH = "state.json"
QUESTIONS_FILE_PATH = "questions_by_topic.json"


def get_all_questions():
    with open(QUESTIONS_FILE_PATH, "r") as questions_file:
        questions_json = json.load(questions_file)
        return questions_json


def get_state():
    with open(STATE_FILE_PATH, "r") as state_file:
        return json.load(state_file)


def dump_state(state: dict):
    with open(STATE_FILE_PATH, "w") as state_file:
        json.dump(state, state_file, indent=4)


def initialize_state_file():
    questions = get_all_questions()
    state = {}
    for topic_id in questions:
        question_count = len(questions[topic_id]["questions"])
        state[topic_id] = [False for _ in range(question_count)]
    dump_state(state)


def does_state_file_exist():
    return os.path.exists(STATE_FILE_PATH)


def mark_question_as_complete(topic_id: str, question_idx: int):
    state = get_state()
    state[topic_id][question_idx] = True
    dump_state(state)


def get_random_question_and_mark_as_complete():
    state = get_state()
    unseen_question_tuples = []
    for topic, question_states in state.items():
        for question_state_idx, question_state in enumerate(question_states):
            if not question_state:
                unseen_question_tuples.append((topic, question_state_idx))

    if len(unseen_question_tuples) == 0:
        print("No questions remaining")
        return

    topic_id, question_idx = random.choice(unseen_question_tuples)
    mark_question_as_complete(topic_id, question_idx)

    questions = get_all_questions()
    topic_name = questions[topic_id]["topic_name"]
    question_content = questions[topic_id]["questions"][question_idx]

    return topic_id, topic_name, question_content


if not does_state_file_exist():
    initialize_state_file()

while True:
    try:
        print("\nOMTP Practice June 2025")
        print("1 - Get question")
        print("2 - Reset state")
        print("3 - Exit")

        choice = input("")
        if choice == "1":
            topic_id, topic_name, question_content = get_random_question_and_mark_as_complete()
            print(f"\nTopic #{topic_id}: {topic_name}")
            print(question_content)
            input("\nPress any key to continue.")
        elif choice == "2":
            initialize_state_file()
        elif choice == "3":
            break
        else:
            print("Incorrect input detected.")
    except KeyboardInterrupt:
        break

print("Exiting...")
