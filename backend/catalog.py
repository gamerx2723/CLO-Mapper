"""
Built-in Course Catalog for Computer Science & Software Engineering Programs
Preloaded with 9 Core Courses and Bloom-rated CLO definitions.
"""

COURSE_CATALOG = [
    {
        "code": "CS1134",
        "title": "Programming Fundamentals",
        "description": "Foundations of computational problem solving, control structures, and modular design.",
        "clos": [
            "CLO-1 (C1): Identify problem-solving strategies & computational thinking paradigms",
            "CLO-2 (C2): Implement programming constructs including arrays, control flow, and functions",
            "CLO-3 (C3): Apply debugging techniques, trace call stacks, and resolve execution bugs",
            "CLO-4 (C4): Analyze algorithmic efficiency, modularity, and adherence to clean code standards"
        ]
    },
    {
        "code": "CS2104",
        "title": "Object Oriented Programming",
        "description": "Object-oriented design, abstraction, polymorphism, generic programming, and I/O streams.",
        "clos": [
            "CLO-1 (C2): Explain OOP principles, encapsulation, access control, and class structures",
            "CLO-2 (C3): Implement constructors, operator overloading, and inheritance hierarchies",
            "CLO-3 (C4): Design polymorphic systems using abstract base classes, virtual methods, and STL",
            "CLO-4 (C3): Develop file serialization streams and robust exception-handling frameworks"
        ]
    },
    {
        "code": "CS2124",
        "title": "Data Structures & Algorithms",
        "description": "Linear and non-linear data structures, asymptotic complexity, and graph algorithms.",
        "clos": [
            "CLO-1 (C2): Define fundamental concepts, asymptotic Big-O notations, and complexity bounds",
            "CLO-2 (C3): Implement data structures including linked lists, stacks, queues, and balanced trees",
            "CLO-3 (C4): Analyze trade-offs between sorting, searching, and graph traversal algorithms",
            "CLO-4 (C4): Justify and design optimal data structures for complex real-world computing problems"
        ]
    },
    {
        "code": "CS3104",
        "title": "Operating Systems",
        "description": "Kernel architecture, process management, CPU scheduling, concurrency, and virtual memory.",
        "clos": [
            "CLO-1 (C2): Describe operating system architecture, kernel dual-mode, and system call interfaces",
            "CLO-2 (C2): Contrast process states, thread models (TCB/PCB), and memory allocation structures",
            "CLO-3 (C3): Calculate CPU scheduling metrics and implement thread synchronization using semaphores",
            "CLO-4 (C4): Analyze virtual memory page replacement policies and deadlock avoidance safety"
        ]
    },
    {
        "code": "SE3213",
        "title": "Software Design & Architecture",
        "description": "Software architecture styles, architectural blueprints, GoF design patterns, and UML modeling.",
        "clos": [
            "CLO-1 (C1): Describe Unified Process phases, architectural design activities, and quality attributes",
            "CLO-2 (C2): Explain layered, microservice, and event-driven software architecture patterns",
            "CLO-3 (C3): Construct detailed UML class, sequence, and component diagrams for complex domains",
            "CLO-4 (C4): Design software architectures applying GoF creational, structural, and behavioral patterns",
            "CLO-5 (C5): Implement and evaluate architectural designs in an object-oriented language"
        ]
    },
    {
        "code": "CS4223",
        "title": "Artificial Intelligence",
        "description": "Search algorithms, constraint satisfaction, adversarial games, and ethical AI implications.",
        "clos": [
            "CLO-1 (C2): Discuss core AI paradigms, agent environments, and the distinction between Weak and Strong AI",
            "CLO-2 (C3): Solve state-space problems using informed A* search, adversarial Minimax, and CSPs",
            "CLO-3 (C4): Formulate technical justifications for search algorithms and heuristic evaluations",
            "CLO-4 (C5): Evaluate societal, ethical, privacy, and fairness implications of autonomous AI systems"
        ]
    },
    {
        "code": "SE3053",
        "title": "Software Quality Engineering",
        "description": "Software verification, validation, test design techniques, static analysis, and quality audits.",
        "clos": [
            "CLO-1 (C1): Define software verification, validation, SQA principles, and the V-Model lifecycle",
            "CLO-2 (C2): Prepare test suites using boundary value analysis, equivalence classes, and control flow graphs",
            "CLO-3 (C4): Analyze software reliability models (MTBF/MTTF) and static code analysis violations",
            "CLO-4 (C5): Conduct technical inspections and compile formal SQA audit defect reports"
        ]
    },
    {
        "code": "SE-4231",
        "title": "Software Project Management",
        "description": "Project estimation, scheduling, earned value management, risk control, and modern agile tooling.",
        "clos": [
            "CLO-1 (C2): Explain PMBOK process groups, life-cycle models, and software estimation methods",
            "CLO-2 (C3): Compute critical path durations (CPM), slack float, and WBS resource schedules",
            "CLO-3 (C4): Analyze project health using Earned Value Management (EVM) cost and schedule metrics",
            "CLO-4 (C3): Configure Agile sprint workflows, backlog user stories, and Kanban boards"
        ]
    },
    {
        "code": "CS3683",
        "title": "Theory of Automata",
        "description": "Formal languages, automata theory, computability, Turing machines, and Chomsky hierarchy.",
        "clos": [
            "CLO-1 (C2): Define finite automata, regular expressions, transition tables, and formal proofs",
            "CLO-2 (C1): Describe Turing machine transition functions and the Church-Turing computability thesis",
            "CLO-3 (C3): Construct deterministic finite automata, non-deterministic FA, and context-free grammars",
            "CLO-4 (C4): Apply Pumping Lemma proofs and eliminate left recursion in grammar manipulation"
        ]
    }
]
