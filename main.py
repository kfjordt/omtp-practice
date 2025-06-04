import random
import json
import os


STATE_FILE_PATH = "state.json"
QUESTIONS_FILE_PATH = "questions_by_topic.json"
QUESTIONS = {
    "1": {
        "topic_name": "Anatomy of a manipulation system",
        "questions": [
            "Describe the four main components of a modern robotic manipulation system (perception, planning, control, and behavior). Explain the role of each component and how they interact with each other.",
            "Explain the concept of 'open-world' manipulation and discuss the key challenges robots face when operating in unstructured environments. What types of understanding are required for successful open-world manipulation?",
            "Compare the different planning approaches in a robotic manipulation system (task planning, grasp planning, and motion planning). Provide specific examples of how these planning types work together in a real-world task."
        ]
    },
    "2": {
        "topic_name": "Robot Setup & Simulation Basics",
        "questions": [
            "Describe the basic anatomy of a robot by explaining the four main components: structural design (links/joints), actuation, end-effectors, and cognitive architecture. How do these components work together to enable manipulation tasks?",
            "Compare the different types of robot joints (revolute, prismatic, spherical, etc.) and explain how they contribute to a robot's degrees of freedom.",
            "Evaluate the different types of actuators used in robotics (electric, pneumatic, hydraulic, and piezoelectric). What factors should be considered when selecting an appropriate actuator for a specific robotic manipulation task?",
            "Discuss the importance of simulation in robotic manipulation. Compare different robot simulation frameworks and explain how the URDF enables robot modeling across different simulation environments."
        ]
    },
    "3": {
        "topic_name": "Mechanics of Manipulation",
        "questions": [
            "Explain the concept of configuration space in robotics. Compare configuration space, task space, and workspace using specific examples of robotic manipulators.",
            "Explain the forward kinematics problem for robotic manipulators.",
            "Analyze the inverse kinematics problem in robotic manipulation. Compare analytical and numerical approaches to solving inverse kinematics and discuss scenarios where multiple solutions may exist."
        ]
    },
    "4": {
        "topic_name": "Perception for Manipulation",
        "questions": [
            "Compare traditional geometric approaches with modern deep learning methods, and discuss how perception for robotics differs from general computer vision tasks.",
            "Explain briefly the Transporter Networks architecture for visual manipulation tasks. Explain how it represents and processes visual information, its key technical innovations, and why it's particularly effective for rearrangement tasks in robotics compared to traditional approaches.",
            "Explain briefly the concept of universal visual representations for robotic manipulation as demonstrated by the R3M framework. Discuss how it utilizes human demonstration videos, the training objectives it employs, and the advantages it offers for transfer learning across different manipulation tasks.",
            "Explain briefly the DenseFusion approach to 6D object pose estimation. Describe its architecture, how it fuses RGB and depth information, and the iterative refinement process. Analyze its strengths and limitations for real-world robotic manipulation applications.",
            "Compare conventional perception versus embodied/interactive perception for robotic manipulation. Discuss the concept of affordances in robotic manipulation and how affordance segmentation can be used for task-oriented robot-human handovers. Analyze briefly the challenges in learning affordances from synthetic data."
        ]
    },
    "5": {
        "topic_name": "Object Grasping and Robot Grippers",
        "questions": [
            "Explain briefly the theoretical foundations of robotic grasping by discussing contact types, grasp wrench space, and closure types. Compare form closure and force closure grasps, and explain how these concepts influence practical gripper design and selection for different manipulation scenarios.",
            "Analyze the concept of grasp quality metrics, particularly the 'largest sphere' and 'hull volume' approaches. Explain how these metrics are calculated from the grasp wrench hull, and discuss their practical implications for evaluating and selecting optimal grasps in robotic manipulation systems.",
            "Compare the major prehension principles used in robotic grippers (e.g., impactive, ingressive, astrictive, and contigutive). Provide examples of each type, and evaluate their relative advantages, limitations, and appropriate application scenarios in industrial and service robotics.",
            "Describe the key design considerations for finger grippers, including kinematic designs (parallel, rotational, angular, and flexible), actuation principles, and jaw design. Explain how these characteristics influence gripper performance for different object manipulation tasks.",
            "Outline a systematic approach for gripper selection and design, from grasp determination to final integration. Discuss how task constraints and object characteristics influence the selection of prehension principles, gripper types, and actuation methods for optimal manipulation performance."
        ]
    },
    "6": {
        "topic_name": "Task & Motion Planning for Robotic Manipulation",
        "questions": [
            "Explain the fundamental challenge of integrating task planning and motion planning for robotic manipulation. Analyze briefly how the 'Infinite Motion Plans' (P1) and 'Downward Refinability' (P2) problems work in practical robot manipulation scenarios.",
            "Compare the three major approaches to Task and Motion Planning (TAMP) integration: hierarchical, interleaved, and integrated. Analyze their respective advantages, limitations, and appropriate application domains, providing examples of real-world robotics tasks where each approach would be most suitable.",
            "Analyze PDDL (Planning Domain Definition Language) as a foundation for task planning in robotics. Explain its core components, demonstrate how a simple manipulation task can be represented in PDDL, and discuss the limitations that make it insufficient for complete robotic manipulation planning.",
            "Evaluate the industrial implementation of skill-based programming systems for robotic manipulation. Explain the architecture of skill-based systems, how they bridge the gap between high-level tasks and low-level device commands, and analyze their advantages and limitations compared to more general TAMP approaches.",
            "Present PDDLStream as an advanced approach to integrating task and motion planning. Describe briefly its architecture, explain how it extends PDDL with streams to handle geometric reasoning, and discuss how it addresses the fundamental challenges of TAMP. Compare it with emerging learning-based approaches like those from Google, NVIDIA, and DeepMind."
        ]
    },
    "7": {
        "topic_name": "Robots in Contact I",
        "questions": [
            "Explain the concept of human-robot collaboration and its importance in modern manufacturing. Discuss the key components of collaborative workspaces as defined by ISO/TS 15066:2016 and analyze how different types of workspaces (non-collaborative, mixed, and collaborative) affect safety considerations and programming approaches.",
            "Compare different modalities for programming by demonstration in collaborative robotics.",
            "Analyze briefly the concept of Dynamic Movement Primitives (DMPs) framework for representing and reproducing robot motions. Explain briefly the mathematical foundation of DMPs including the transformation system, forcing term, and canonical phase system, and discuss why DMPs are particularly well-suited for robotic manipulation tasks.",
            "Discuss how orientation is represented in Cartesian-space DMPs using quaternions and explain the advantages of this representation.",
            "Evaluate the benefits of using DMPs for motion representation in collaborative robotics compared to traditional trajectory generation methods."
        ]
    },
    "8": {
        "topic_name": "Robots in Contact II",
        "questions": [
            "Compare the different robot control strategies for interaction with the environment. Explain the limitations of traditional position control and why force control approaches are necessary for contact tasks.",
            "Analyze the methods for force and torque measurement in robotic systems. Compare and evaluate the advantages and limitations of using force/torque sensors at the tool versus joint torque sensors.",
            "Explain the concept of impedance control for robotic manipulation tasks. Discuss which types of robots are best suited for impedance control and why it's particularly useful for interaction tasks.",
            "Compare admittance control and impedance control in terms of their fundamental principles and practical implementation considerations.",
            "Evaluate how force control strategies can be coupled with trajectory generation techniques such as Dynamic Movement Primitives (DMPs) for adaptive robotic manipulation."
        ]
    },
    "9": {
        "topic_name": "Foundation Models in OMTP",
        "questions": [
            "Explain briefly the concept of foundation models in robotics and how they differ from traditional machine learning and deep learning approaches.",
            "Analyze the key architectural components of transformer-based models, particularly the attention mechanism, and discuss why they are well-suited for robotic manipulation tasks.",
            "Compare different approaches to using language models for robot policy learning.",
            "Analyze briefly the SayCan framework for language-image goal-conditioned value learning in robotics. Explain briefly how it addresses the challenge of grounding language in robotic affordances and discuss how it combines large language models with value functions to enable robots to execute high-level instructions.",
            "Explain briefly the architectural design, training methodology, and capabilities for manipulation tasks of Robot Transformers (RT-1, RT-2).",
            "Analyze the RoboPoint case study as an example of a vision-language model for spatial affordance prediction."
        ]
    }
}

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
        print("No questions remaining")
        return

    topic_id, question_idx = random.choice(unseen_question_tuples)
    mark_question_as_complete(topic_id, question_idx)

    topic_name = QUESTIONS[topic_id]["topic_name"]
    question_content = QUESTIONS[topic_id]["questions"][question_idx]

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
