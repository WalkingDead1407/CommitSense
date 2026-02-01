CommitSense is a unified developer toolkit designed to streamline development lifecycle. From debugging cryptic errors to prioritising messy issues and writing sensible commit messages, by using open source logic and datasets CommitSense brings "sense" to your workflow.

#                                       The Vision

Contributions to open-source projects frequently involve a lot of conflict. CommitSense follows your code through three crucial phases as an intelligent companion:
        
1) SenseFix (The Detective): When a developer hits an error, SenseFix uses context from the current repository to analyse local stack traces and recommend fixes.
2) SenseCommit (The Translator): Analyses your git diff and the purpose of your fix to provide relevant, Commit messages.
3) SenseTriage (The Concierge): Incoming PRs are automatically labelled, prioritised, and assigned to the appropriate maintainers.

#                                        __Key Features__
## __SenseFix__

How it works: It parses the stack trace, identifies the exact file and line and uses AST(Abstract Syntac Tree) or Static code Analysis to extract the full function and its dependencies.\
   LLM input: It feeds the exact logic (either broken or complete) + the error log to a local LLM for a accurate fix.

## __SenseCommit__

How it works: It analyzes you git diff in real time. If you used Sensefix earlier, it combined the "intent" of the fix with the actual code changed to write a perfect commit

## __SenseTriage__

How it works: It uses pattern matching and metadata analysis to label PRs and find the right reviewr based on the project's file history.

#                                  The Lightweight Stack

Inference: Ollama for logical and local reasonig

Structural Search: ast-grep for ultra fast code navigation

CLI Engine: For a beautiful terminal UI




#                                   Quick Start

## Clone and Install
    git clone https://github.com/your-team/commitsense.git
    cd commitsense
    pip install .

## Ensure Ollama is running
    ollama run qwen2.5-coder:7b 

Typical Workflow

    Crash: node index.js | cs fix — Get a structural fix suggestion.
    
    Commit: cs commit — Automatically stage and document the change.
    
    Push: Let SenseTriage handle the labels on GitHub.
