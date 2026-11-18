"""
Comprehensive OBE Exam Question & Bloom's Taxonomy Dataset
Covers multiple Computer Science disciplines with cognitive levels and topical domains.
"""

TRAINING_DATA = [
    # --- PROGRAMMING FUNDAMENTALS (CS1134) ---
    {
        "question": "Define computational thinking and explain the four fundamental cornerstones of problem solving.",
        "course": "CS1134",
        "clo_index": 0,
        "bloom_level": 0,  # Level 1: Remember/Understand
        "verbs": ["define", "explain"],
        "keywords": ["computational thinking", "problem solving", "cornerstones", "algorithm"]
    },
    {
        "question": "What is the difference between a compiler and an interpreter? Describe how machine code is generated.",
        "course": "CS1134",
        "clo_index": 0,
        "bloom_level": 0,
        "verbs": ["describe", "difference"],
        "keywords": ["compiler", "interpreter", "machine code", "syntax"]
    },
    {
        "question": "Write a C++ function that takes an array of integers and reverses its elements in-place using two pointers.",
        "course": "CS1134",
        "clo_index": 1,
        "bloom_level": 1,  # Level 2: Apply/Solve
        "verbs": ["write", "implement"],
        "keywords": ["array", "function", "pointers", "reverse", "constructs"]
    },
    {
        "question": "Implement a nested loop structure to print Pascal's triangle for n rows given as user input.",
        "course": "CS1134",
        "clo_index": 1,
        "bloom_level": 1,
        "verbs": ["implement", "write"],
        "keywords": ["loop", "nested", "pascal triangle", "input", "programming"]
    },
    {
        "question": "Identify and fix the segmentation fault error in the given dynamic memory allocation code snippet.",
        "course": "CS1134",
        "clo_index": 2,
        "bloom_level": 1,
        "verbs": ["identify", "fix", "debug"],
        "keywords": ["segmentation fault", "debugging", "memory allocation", "pointers", "bug"]
    },
    {
        "question": "Trace the execution of this recursive factorial function and show the stack frames for n = 4.",
        "course": "CS1134",
        "clo_index": 2,
        "bloom_level": 1,
        "verbs": ["trace", "show"],
        "keywords": ["trace", "call stack", "recursion", "stack frame", "debugging"]
    },
    {
        "question": "Analyze the time and space complexity of the recursive Fibonacci implementation versus iterative dynamic programming.",
        "course": "CS1134",
        "clo_index": 3,
        "bloom_level": 2,  # Level 3: Analyze/Evaluate/Design
        "verbs": ["analyze", "evaluate"],
        "keywords": ["efficiency", "modularity", "complexity", "coding standards", "optimization"]
    },
    {
        "question": "Refactor the provided monolithic 300-line script into modular functions adhering to clean code standards.",
        "course": "CS1134",
        "clo_index": 3,
        "bloom_level": 2,
        "verbs": ["refactor", "evaluate", "design"],
        "keywords": ["refactor", "modularity", "clean code", "standards", "architecture"]
    },

    # --- OBJECT ORIENTED PROGRAMMING (CS2104) ---
    {
        "question": "Explain the concept of encapsulation and data hiding with an appropriate class definition example.",
        "course": "CS2104",
        "clo_index": 0,
        "bloom_level": 0,
        "verbs": ["explain", "describe"],
        "keywords": ["encapsulation", "data hiding", "class", "access specifiers", "oop"]
    },
    {
        "question": "Define class, object, and instance variables. What is the role of the this pointer?",
        "course": "CS2104",
        "clo_index": 0,
        "bloom_level": 0,
        "verbs": ["define", "explain"],
        "keywords": ["class", "object", "instance", "this pointer", "constructor"]
    },
    {
        "question": "Implement a BankAccount class with copy constructor, parameterized constructor, and destructor handling dynamic resources.",
        "course": "CS2104",
        "clo_index": 1,
        "bloom_level": 1,
        "verbs": ["implement", "write"],
        "keywords": ["constructor", "destructor", "deep copy", "inheritance", "overloading"]
    },
    {
        "question": "Write a program demonstrating multiple inheritance and demonstrate how to resolve the diamond problem using virtual base classes.",
        "course": "CS2104",
        "clo_index": 1,
        "bloom_level": 1,
        "verbs": ["write", "demonstrate"],
        "keywords": ["multiple inheritance", "diamond problem", "virtual base class", "hierarchy"]
    },
    {
        "question": "Design an abstract Shape class hierarchy utilizing virtual functions and runtime polymorphism in C++.",
        "course": "CS2104",
        "clo_index": 2,
        "bloom_level": 2,
        "verbs": ["design", "construct"],
        "keywords": ["polymorphism", "abstract class", "pure virtual", "templates", "stl"]
    },
    {
        "question": "Evaluate the performance trade-offs of using std::vector versus std::list for frequent insertions at arbitrary indices.",
        "course": "CS2104",
        "clo_index": 2,
        "bloom_level": 2,
        "verbs": ["evaluate", "analyze", "compare"],
        "keywords": ["stl", "vector", "list", "iterators", "templates", "trade-offs"]
    },
    {
        "question": "Implement custom file stream serialization and deserialization for an Employee records management system.",
        "course": "CS2104",
        "clo_index": 3,
        "bloom_level": 1,
        "verbs": ["implement", "serialize"],
        "keywords": ["serialization", "file streams", "binary files", "exception handling", "io"]
    },
    {
        "question": "Develop a robust error-handling framework using try-catch blocks and custom exception classes for invalid user transactions.",
        "course": "CS2104",
        "clo_index": 3,
        "bloom_level": 1,
        "verbs": ["develop", "implement"],
        "keywords": ["exceptions", "try catch", "custom exception", "stream error", "robustness"]
    },

    # --- DATA STRUCTURES & ALGORITHMS (CS2124) ---
    {
        "question": "Define Big-O, Big-Omega, and Big-Theta asymptotic notations. What are tight asymptotic bounds?",
        "course": "CS2124",
        "clo_index": 0,
        "bloom_level": 0,
        "verbs": ["define", "explain"],
        "keywords": ["asymptotic notation", "big o", "complexity", "fundamental concepts", "bounds"]
    },
    {
        "question": "Explain the difference between a complete binary tree and a full binary tree with diagrams.",
        "course": "CS2124",
        "clo_index": 0,
        "bloom_level": 0,
        "verbs": ["explain", "describe"],
        "keywords": ["binary tree", "complete binary tree", "definitions", "tree terminology"]
    },
    {
        "question": "Implement a Doubly Linked List with operations for inserting at head, deleting a node by value, and traversing in reverse.",
        "course": "CS2124",
        "clo_index": 1,
        "bloom_level": 1,
        "verbs": ["implement", "code"],
        "keywords": ["doubly linked list", "pointers", "queue", "stack", "data structure"]
    },
    {
        "question": "Write an iterative algorithm to evaluate a postfix expression using an array-based stack.",
        "course": "CS2124",
        "clo_index": 1,
        "bloom_level": 1,
        "verbs": ["write", "solve"],
        "keywords": ["postfix", "stack", "evaluation", "algorithm", "implementation"]
    },
    {
        "question": "Analyze the worst-case, average-case, and best-case time complexity of Quicksort with randomized pivot selection.",
        "course": "CS2124",
        "clo_index": 2,
        "bloom_level": 2,
        "verbs": ["analyze", "derive"],
        "keywords": ["quicksort", "randomized", "worst case", "average case", "trade-offs", "analysis"]
    },
    {
        "question": "Compare Dijkstra's algorithm and Bellman-Ford for single-source shortest paths on graphs with negative edge weights.",
        "course": "CS2124",
        "clo_index": 2,
        "bloom_level": 2,
        "verbs": ["compare", "contrast", "analyze"],
        "keywords": ["dijkstra", "bellman ford", "graphs", "trade-offs", "shortest path"]
    },
    {
        "question": "Design an optimal data structure to implement an LRU (Least Recently Used) Cache supporting O(1) get and put operations.",
        "course": "CS2124",
        "clo_index": 3,
        "bloom_level": 2,
        "verbs": ["design", "justify"],
        "keywords": ["lru cache", "hash map", "doubly linked list", "justify", "real problems"]
    },
    {
        "question": "Justify whether a Red-Black Tree or a B-Tree is more appropriate for index storage in a relational database management system.",
        "course": "CS2124",
        "clo_index": 3,
        "bloom_level": 2,
        "verbs": ["justify", "evaluate"],
        "keywords": ["red black tree", "b tree", "database indexing", "justify", "data structures"]
    },

    # --- OPERATING SYSTEMS (CS3104) ---
    {
        "question": "Describe the dual-mode operation of the CPU (User Mode vs Kernel Mode) and explain system calls.",
        "course": "CS3104",
        "clo_index": 0,
        "bloom_level": 0,
        "verbs": ["describe", "explain"],
        "keywords": ["user mode", "kernel mode", "system call", "os components", "architecture"]
    },
    {
        "question": "What is the difference between a process and a thread? Explain thread control blocks (TCB).",
        "course": "CS3104",
        "clo_index": 1,
        "bloom_level": 0,
        "verbs": ["explain", "describe"],
        "keywords": ["process", "thread", "tcb", "pcb", "memory structure"]
    },
    {
        "question": "Calculate the average waiting time and turnaround time for the given processes using Round Robin with time quantum = 4.",
        "course": "CS3104",
        "clo_index": 2,
        "bloom_level": 1,
        "verbs": ["calculate", "solve"],
        "keywords": ["round robin", "scheduling", "waiting time", "turnaround", "algorithms"]
    },
    {
        "question": "Implement synchronization between producer and consumer threads using counting semaphores and mutex locks.",
        "course": "CS3104",
        "clo_index": 2,
        "bloom_level": 1,
        "verbs": ["implement", "solve"],
        "keywords": ["semaphores", "mutex", "producer consumer", "synchronization", "deadlock"]
    },
    {
        "question": "Analyze the conditions necessary for deadlock to occur and evaluate the safety algorithm in Banker's Deadlock Avoidance.",
        "course": "CS3104",
        "clo_index": 3,
        "bloom_level": 2,
        "verbs": ["analyze", "evaluate"],
        "keywords": ["deadlock", "coffman conditions", "bankers algorithm", "resource analysis", "safety"]
    },
    {
        "question": "Critically analyze page replacement policies (FIFO, LRU, Optimal) and explain Belady's Anomaly.",
        "course": "CS3104",
        "clo_index": 3,
        "bloom_level": 2,
        "verbs": ["analyze", "critique"],
        "keywords": ["page replacement", "beladys anomaly", "virtual memory", "efficiency", "thrashing"]
    },

    # --- SOFTWARE DESIGN & ARCHITECTURE (SE3213) ---
    {
        "question": "Define the phases of the Unified Process (Inception, Elaboration, Construction, Transition) and core workflow milestones.",
        "course": "SE3213",
        "clo_index": 0,
        "bloom_level": 0,
        "verbs": ["define", "explain"],
        "keywords": ["unified process", "inception", "elaboration", "design activities", "lifecycle"]
    },
    {
        "question": "Explain the architectural styles: Layered Architecture versus Event-Driven Microservices.",
        "course": "SE3213",
        "clo_index": 1,
        "bloom_level": 0,
        "verbs": ["explain", "describe"],
        "keywords": ["architectural style", "layered", "microservices", "event-driven", "consistency"]
    },
    {
        "question": "Construct a complete UML Class Diagram with inheritance, aggregation, and composition for an Online Flight Booking System.",
        "course": "SE3213",
        "clo_index": 2,
        "bloom_level": 1,
        "verbs": ["construct", "draw", "model"],
        "keywords": ["class diagram", "uml", "aggregation", "composition", "oo design models"]
    },
    {
        "question": "Design an architectural blueprint using the Observer and Factory design patterns to decouple sensor event publishers from alerts.",
        "course": "SE3213",
        "clo_index": 3,
        "bloom_level": 2,
        "verbs": ["design", "architect"],
        "keywords": ["design patterns", "observer", "factory", "architectural documentation", "uml"]
    },
    {
        "question": "Write the production implementation of the Singleton and Strategy patterns in Java or C++.",
        "course": "SE3213",
        "clo_index": 4,
        "bloom_level": 1,
        "verbs": ["write", "implement"],
        "keywords": ["singleton", "strategy pattern", "implementation", "oop language", "code"]
    },

    # --- ARTIFICIAL INTELLIGENCE (CS4223) ---
    {
        "question": "Describe the Turing Test and discuss the distinctions between Weak AI and Strong General AI.",
        "course": "CS4223",
        "clo_index": 0,
        "bloom_level": 0,
        "verbs": ["describe", "discuss"],
        "keywords": ["turing test", "weak ai", "strong ai", "ai paradigms", "definitions"]
    },
    {
        "question": "Trace the A* Search algorithm on the provided graph using Euclidean distance heuristic and show the open and closed lists.",
        "course": "CS4223",
        "clo_index": 1,
        "bloom_level": 1,
        "verbs": ["trace", "solve"],
        "keywords": ["a* search", "heuristic", "csp", "search tree", "uninformed informed search"]
    },
    {
        "question": "Formulate the Map Coloring problem of 5 provinces as a Constraint Satisfaction Problem (CSP) and solve using Backtracking + MRV.",
        "course": "CS4223",
        "clo_index": 1,
        "bloom_level": 1,
        "verbs": ["formulate", "solve"],
        "keywords": ["csp", "constraint satisfaction", "mrv", "backtracking", "search"]
    },
    {
        "question": "Critique and justify the choice between Minimax with Alpha-Beta pruning versus Monte Carlo Tree Search (MCTS) for Game of Go.",
        "course": "CS4223",
        "clo_index": 2,
        "bloom_level": 2,
        "verbs": ["critique", "justify"],
        "keywords": ["minimax", "alpha beta", "mcts", "design justification", "technical communication"]
    },
    {
        "question": "Analyze ethical, societal, and algorithmic bias implications when deploying deep neural networks for automated loan underwriting.",
        "course": "CS4223",
        "clo_index": 3,
        "bloom_level": 2,
        "verbs": ["analyze", "evaluate"],
        "keywords": ["ethical", "fairness", "bias", "societal implications", "responsible ai"]
    },

    # --- SOFTWARE QUALITY ENGINEERING (SE3053) ---
    {
        "question": "Define Verification versus Validation in software engineering. Outline the V-Model of software testing.",
        "course": "SE3053",
        "clo_index": 0,
        "bloom_level": 0,
        "verbs": ["define", "outline"],
        "keywords": ["verification", "validation", "v-model", "sqa principles", "testing basics"]
    },
    {
        "question": "Prepare a comprehensive test suite including boundary value analysis (BVA) and equivalence partitioning for an age validation field.",
        "course": "SE3053",
        "clo_index": 1,
        "bloom_level": 1,
        "verbs": ["prepare", "create"],
        "keywords": ["test case", "bva", "equivalence partitioning", "test suite preparation"]
    },
    {
        "question": "Calculate Cyclomatic Complexity for the given control flow graph and list the independent basis paths.",
        "course": "SE3053",
        "clo_index": 1,
        "bloom_level": 1,
        "verbs": ["calculate", "determine"],
        "keywords": ["cyclomatic complexity", "control flow graph", "basis paths", "white box"]
    },
    {
        "question": "Analyze software reliability metrics using MTTF, MTTR, and MTBF. Evaluate failure intensity decay models.",
        "course": "SE3053",
        "clo_index": 2,
        "bloom_level": 2,
        "verbs": ["analyze", "evaluate"],
        "keywords": ["reliability", "mttf", "mttr", "mtbf", "tools and techniques", "analysis"]
    },
    {
        "question": "Conduct a formal technical inspection and compile an SQA Audit Report detailing code smell violations and security vulnerabilities.",
        "course": "SE3053",
        "clo_index": 3,
        "bloom_level": 2,
        "verbs": ["compile", "audit"],
        "keywords": ["audit", "inspection", "qa findings", "compliance", "report compilation"]
    },

    # --- SOFTWARE PROJECT MANAGEMENT (SE-4231) ---
    {
        "question": "Explain the five PMBOK Process Groups: Initiating, Planning, Executing, Monitoring & Controlling, and Closing.",
        "course": "SE-4231",
        "clo_index": 0,
        "bloom_level": 0,
        "verbs": ["explain", "describe"],
        "keywords": ["process groups", "pmbok", "life-cycle", "project management"]
    },
    {
        "question": "Calculate the project duration, critical path, and total float for the given activity network table using Critical Path Method (CPM).",
        "course": "SE-4231",
        "clo_index": 1,
        "bloom_level": 1,
        "verbs": ["calculate", "solve"],
        "keywords": ["cpm", "critical path", "float", "estimation", "wbs", "cocomo"]
    },
    {
        "question": "Calculate the Earned Value (EV), Cost Variance (CV), and Schedule Performance Index (SPI) given PV=$50k, AC=$55k, and EV=$45k.",
        "course": "SE-4231",
        "clo_index": 2,
        "bloom_level": 2,
        "verbs": ["calculate", "evaluate", "analyze"],
        "keywords": ["evm", "earned value", "cost variance", "schedule control", "risk metrics"]
    },
    {
        "question": "Design an Agile Sprint Backlog and configure Kanban workflow boards in Jira for a 2-week iteration.",
        "course": "SE-4231",
        "clo_index": 3,
        "bloom_level": 1,
        "verbs": ["design", "configure"],
        "keywords": ["agile", "jira", "sprint backlog", "kanban", "tooling"]
    },

    # --- THEORY OF AUTOMATA (CS3683) ---
    {
        "question": "Define deterministic finite automata (DFA) formally as a 5-tuple. What is the extended transition function?",
        "course": "CS3683",
        "clo_index": 0,
        "bloom_level": 0,
        "verbs": ["define", "explain"],
        "keywords": ["dfa", "5-tuple", "formal proofs", "transition function", "automata"]
    },
    {
        "question": "What is the Church-Turing thesis? Describe the standard model of a Single-Tape Turing Machine.",
        "course": "CS3683",
        "clo_index": 1,
        "bloom_level": 0,
        "verbs": ["describe", "define"],
        "keywords": ["turing machine", "church-turing", "transition function", "tape"]
    },
    {
        "question": "Construct a DFA over alphabet {0, 1} that accepts all binary strings containing an even number of 0s and odd number of 1s.",
        "course": "CS3683",
        "clo_index": 2,
        "bloom_level": 1,
        "verbs": ["construct", "design"],
        "keywords": ["construct dfa", "finite automata", "cfg", "regular expression", "language"]
    },
    {
        "question": "Convert the given non-deterministic finite automaton (NFA) with epsilon transitions to an equivalent minimal DFA.",
        "course": "CS3683",
        "clo_index": 2,
        "bloom_level": 1,
        "verbs": ["convert", "solve"],
        "keywords": ["nfa to dfa", "subset construction", "minimization", "cfg representation"]
    },
    {
        "question": "Use the Pumping Lemma for Regular Languages to formally prove that L = {0^n 1^n | n >= 0} is not regular.",
        "course": "CS3683",
        "clo_index": 3,
        "bloom_level": 2,
        "verbs": ["prove", "analyze"],
        "keywords": ["pumping lemma", "formal proof", "non-regular", "grammar manipulation"]
    },
    {
        "question": "Eliminate left recursion and left factor the provided Context-Free Grammar (CFG) for parsing arithmetic expressions.",
        "course": "CS3683",
        "clo_index": 3,
        "bloom_level": 2,
        "verbs": ["eliminate", "transform"],
        "keywords": ["left recursion", "left factoring", "cfg", "grammar manipulation", "parsing"]
    }
]

BLOOM_VERB_MAP = {
    "define": 0, "describe": 0, "identify": 0, "explain": 0, "discuss": 0,
    "list": 0, "state": 0, "name": 0, "outline": 0, "summarize": 0,
    "recall": 0, "recognize": 0, "clarify": 0, "distinguish": 0,

    "apply": 1, "solve": 1, "calculate": 1, "compute": 1, "implement": 1,
    "develop": 1, "write": 1, "construct": 1, "execute": 1, "trace": 1,
    "demonstrate": 1, "modify": 1, "operate": 1, "simulate": 1, "fix": 1,
    "prepare": 1, "convert": 1,

    "analyze": 2, "evaluate": 2, "design": 2, "justify": 2, "compare": 2,
    "contrast": 2, "critique": 2, "optimize": 2, "refactor": 2, "prove": 2,
    "derive": 2, "audit": 2, "investigate": 2, "differentiate": 2, "formulate": 2,
    "architect": 2, "eliminate": 2, "synthesize": 2
}
