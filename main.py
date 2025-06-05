import random
import json
import os

KEY_FILE_PATH = "key.txt"
STATE_FILE_PATH = "state.json"
MODEL_NAME = "gemini-1.5-flash"
QUESTIONS = {
    "1": {
        "topic_name": "Anatomy of a manipulation system",
        "questions": [
            "Describe the four main components of a modern robotic manipulation system (perception, planning, control, and behavior). Explain the role of each component and how they interact with each other.",
            "Explain the concept of 'open-world' manipulation and discuss the key challenges robots face when operating in unstructured environments. What types of understanding are required for successful open-world manipulation?",
            "Compare the different planning approaches in a robotic manipulation system (task planning, grasp planning, and motion planning). Provide specific examples of how these planning types work together in a real-world task.",
        ],
    },
    "2": {
        "topic_name": "Robot Setup & Simulation Basics",
        "questions": [
            "Describe the basic anatomy of a robot by explaining the four main components: structural design (links/joints), actuation, end-effectors, and cognitive architecture. How do these components work together to enable manipulation tasks?",
            "Compare the different types of robot joints (revolute, prismatic, spherical, etc.) and explain how they contribute to a robot's degrees of freedom.",
            "Evaluate the different types of actuators used in robotics (electric, pneumatic, hydraulic, and piezoelectric). What factors should be considered when selecting an appropriate actuator for a specific robotic manipulation task?",
            "Discuss the importance of simulation in robotic manipulation. Compare different robot simulation frameworks and explain how the URDF enables robot modeling across different simulation environments.",
        ],
    },
    "3": {
        "topic_name": "Mechanics of Manipulation",
        "questions": [
            "Explain the concept of configuration space in robotics. Compare configuration space, task space, and workspace using specific examples of robotic manipulators.",
            "Explain the forward kinematics problem for robotic manipulators.",
            "Analyze the inverse kinematics problem in robotic manipulation. Compare analytical and numerical approaches to solving inverse kinematics and discuss scenarios where multiple solutions may exist.",
        ],
    },
    "4": {
        "topic_name": "Perception for Manipulation",
        "questions": [
            "Compare traditional geometric approaches with modern deep learning methods, and discuss how perception for robotics differs from general computer vision tasks.",
            "Explain briefly the Transporter Networks architecture for visual manipulation tasks. Explain how it represents and processes visual information, its key technical innovations, and why it's particularly effective for rearrangement tasks in robotics compared to traditional approaches.",
            "Explain briefly the concept of universal visual representations for robotic manipulation as demonstrated by the R3M framework. Discuss how it utilizes human demonstration videos, the training objectives it employs, and the advantages it offers for transfer learning across different manipulation tasks.",
            "Explain briefly the DenseFusion approach to 6D object pose estimation. Describe its architecture, how it fuses RGB and depth information, and the iterative refinement process. Analyze its strengths and limitations for real-world robotic manipulation applications.",
            "Compare conventional perception versus embodied/interactive perception for robotic manipulation. Discuss the concept of affordances in robotic manipulation and how affordance segmentation can be used for task-oriented robot-human handovers. Analyze briefly the challenges in learning affordances from synthetic data.",
        ],
    },
    "5": {
        "topic_name": "Object Grasping and Robot Grippers",
        "questions": [
            "Explain briefly the theoretical foundations of robotic grasping by discussing contact types, grasp wrench space, and closure types. Compare form closure and force closure grasps, and explain how these concepts influence practical gripper design and selection for different manipulation scenarios.",
            "Analyze the concept of grasp quality metrics, particularly the 'largest sphere' and 'hull volume' approaches. Explain how these metrics are calculated from the grasp wrench hull, and discuss their practical implications for evaluating and selecting optimal grasps in robotic manipulation systems.",
            "Compare the major prehension principles used in robotic grippers (e.g., impactive, ingressive, astrictive, and contigutive). Provide examples of each type, and evaluate their relative advantages, limitations, and appropriate application scenarios in industrial and service robotics.",
            "Describe the key design considerations for finger grippers, including kinematic designs (parallel, rotational, angular, and flexible), actuation principles, and jaw design. Explain how these characteristics influence gripper performance for different object manipulation tasks.",
            "Outline a systematic approach for gripper selection and design, from grasp determination to final integration. Discuss how task constraints and object characteristics influence the selection of prehension principles, gripper types, and actuation methods for optimal manipulation performance.",
        ],
    },
    "6": {
        "topic_name": "Task & Motion Planning for Robotic Manipulation",
        "questions": [
            "Explain the fundamental challenge of integrating task planning and motion planning for robotic manipulation. Analyze briefly how the 'Infinite Motion Plans' (P1) and 'Downward Refinability' (P2) problems work in practical robot manipulation scenarios.",
            "Compare the three major approaches to Task and Motion Planning (TAMP) integration: hierarchical, interleaved, and integrated. Analyze their respective advantages, limitations, and appropriate application domains, providing examples of real-world robotics tasks where each approach would be most suitable.",
            "Analyze PDDL (Planning Domain Definition Language) as a foundation for task planning in robotics. Explain its core components, demonstrate how a simple manipulation task can be represented in PDDL, and discuss the limitations that make it insufficient for complete robotic manipulation planning.",
            "Evaluate the industrial implementation of skill-based programming systems for robotic manipulation. Explain the architecture of skill-based systems, how they bridge the gap between high-level tasks and low-level device commands, and analyze their advantages and limitations compared to more general TAMP approaches.",
            "Present PDDLStream as an advanced approach to integrating task and motion planning. Describe briefly its architecture, explain how it extends PDDL with streams to handle geometric reasoning, and discuss how it addresses the fundamental challenges of TAMP. Compare it with emerging learning-based approaches like those from Google, NVIDIA, and DeepMind.",
        ],
    },
    "7": {
        "topic_name": "Robots in Contact I",
        "questions": [
            "Explain the concept of human-robot collaboration and its importance in modern manufacturing. Discuss the key components of collaborative workspaces as defined by ISO/TS 15066:2016 and analyze how different types of workspaces (non-collaborative, mixed, and collaborative) affect safety considerations and programming approaches.",
            "Compare different modalities for programming by demonstration in collaborative robotics.",
            "Analyze briefly the concept of Dynamic Movement Primitives (DMPs) framework for representing and reproducing robot motions. Explain briefly the mathematical foundation of DMPs including the transformation system, forcing term, and canonical phase system, and discuss why DMPs are particularly well-suited for robotic manipulation tasks.",
            "Discuss how orientation is represented in Cartesian-space DMPs using quaternions and explain the advantages of this representation.",
            "Evaluate the benefits of using DMPs for motion representation in collaborative robotics compared to traditional trajectory generation methods.",
        ],
    },
    "8": {
        "topic_name": "Robots in Contact II",
        "questions": [
            "Compare the different robot control strategies for interaction with the environment. Explain the limitations of traditional position control and why force control approaches are necessary for contact tasks.",
            "Analyze the methods for force and torque measurement in robotic systems. Compare and evaluate the advantages and limitations of using force/torque sensors at the tool versus joint torque sensors.",
            "Explain the concept of impedance control for robotic manipulation tasks. Discuss which types of robots are best suited for impedance control and why it's particularly useful for interaction tasks.",
            "Compare admittance control and impedance control in terms of their fundamental principles and practical implementation considerations.",
            "Evaluate how force control strategies can be coupled with trajectory generation techniques such as Dynamic Movement Primitives (DMPs) for adaptive robotic manipulation.",
        ],
    },
    "9": {
        "topic_name": "Foundation Models in OMTP",
        "questions": [
            "Explain briefly the concept of foundation models in robotics and how they differ from traditional machine learning and deep learning approaches.",
            "Analyze the key architectural components of transformer-based models, particularly the attention mechanism, and discuss why they are well-suited for robotic manipulation tasks.",
            "Compare different approaches to using language models for robot policy learning.",
            "Analyze briefly the SayCan framework for language-image goal-conditioned value learning in robotics. Explain briefly how it addresses the challenge of grounding language in robotic affordances and discuss how it combines large language models with value functions to enable robots to execute high-level instructions.",
            "Explain briefly the architectural design, training methodology, and capabilities for manipulation tasks of Robot Transformers (RT-1, RT-2).",
            "Analyze the RoboPoint case study as an example of a vision-language model for spatial affordance prediction.",
        ],
    },
    "99": {
        "topic_name": "Mini-project",
        "questions": [
            "Explain about mini-project",
            "Anything you wish to add about your mini-project",  # this piece of lore was acquired in ROB group chat
        ],
    },
}
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

def get_state():
    with open(STATE_FILE_PATH, "r") as state_file:
        return json.load(state_file)

def dump_state(state: dict):
    with open(STATE_FILE_PATH, "w") as state_file:
        json.dump(state, state_file, indent=4)

def initialize_state_file():
    state = {}
    for topic_id in QUESTIONS:
        question_count = len(QUESTIONS[topic_id]["questions"])
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
        print(RED + "No questions remaining" + RESET)
        return

    topic_id, question_idx = random.choice(unseen_question_tuples)
    mark_question_as_complete(topic_id, question_idx)

    topic_name = QUESTIONS[topic_id]["topic_name"]
    question_content = QUESTIONS[topic_id]["questions"][question_idx]

    return topic_id, topic_name, question_content

def get_completion_rate():
    completed_questions = 0
    question_count_total = 0
    state = get_state()
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

if not does_state_file_exist():
    initialize_state_file()

llm_model = get_llm_model()

print(f"LLM available? {GREEN + 'Yes' + RESET if llm_model is not None else RED + 'No' + RESET}")

while True:
    try:
        print()
        print(CYAN + "1 - Get question" + RESET)
        print(CYAN + "2 - Get completion rate" + RESET)
        print(CYAN + "3 - Reset state" + RESET)
        print(CYAN + "4 - Exit" + RESET)

        choice = input("")
        if choice == "1":
            result = get_random_question_and_mark_as_complete()
            if not result:
                continue
            topic_id, topic_name, question_content = result
            print()
            print(f"{YELLOW}Topic #{topic_id}: {topic_name}{RESET}")
            print(YELLOW + question_content + RESET)
            while True:
                print()
                print(CYAN + "1 - Finish question" + RESET)
                print(CYAN + "2 - Get LLM reply" + RESET)
                inner_choice = input("")
                if inner_choice == "1":
                    break
                elif inner_choice == "2":
                    if llm_model is not None:
                        chat_gpt_answer = prompt_llm(question_content, llm_model)
                        print()
                        print(GREEN + chat_gpt_answer + RESET)
                    else:
                        print(RED + "LLM not available." + RESET)
                else:
                    print(RED + "Incorrect input detected." + RESET)
        elif choice == "2":
            completed_questions, question_count_total = get_completion_rate()
            completion_percent = (completed_questions / float(question_count_total)) * 100
            print(
                MAGENTA
                + f"\nCurrent completion rate: {completed_questions}/{question_count_total} ({completion_percent:.1f}%)"
                + RESET
            )
        elif choice == "3":
            initialize_state_file()
            print(BLUE + "State has been reset." + RESET)
        elif choice == "4":
            break
        else:
            print(RED + "Incorrect input detected." + RESET)
    except KeyboardInterrupt:
        break

print("Exiting...")