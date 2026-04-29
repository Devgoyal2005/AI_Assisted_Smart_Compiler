# AI-Assisted Smart Compiler

A high-performance, hybrid compiler pipeline that integrates traditional deterministic compilation with cutting-edge Machine Learning and LLM layers. It accelerates compilation by predicting AST structures, dispatch paths, and optimization strategies, and provides intelligent error recovery using a dedicated LLM repair layer.

The project features a modular Python core, a FastAPI backend, and a modern web interface for real-time visualization of the compilation process.

## Features

- **6-Phase Pipeline**: Lexer, Parser, Semantic Analyzer, IR Generator, Code Optimizer, and Assembly Generator.
- **3 ML Layers**: Accelerates parsing and optimization without sacrificing correctness.
- **LLM Error Repair**: Collects errors across all reachable phases and queries an LLM to provide holistic repair suggestions.
- **Live Visualization**: A modern web frontend to visualize each compilation phase, including tokens, AST, IR, and Assembly.
- **Latency Comparison**: Real-time performance comparisons between the ML-assisted pipeline and a traditional compiler setup.
- **FastAPI Backend**: Exposes clean `/compile` and `/info` REST endpoints.

## Compiler Pipeline

1. **Lexer**: Converts raw Python source code into a flat stream of typed tokens. Tracks indentation and handles comments.
2. **Parser**: Builds an Abstract Syntax Tree (AST) from tokens via recursive descent. **ML Layers 1 & 2** are injected here to accelerate parsing.
3. **Semantic Analyzer**: Walks the AST to enforce meaning-level correctness (variable definitions, type checks, scope, etc.).
4. **IR Generator**: Lowers the AST into a language-neutral, three-address Intermediate Representation (IR).
5. **Code Optimizer**: Optimizes IR (constant folding, dead code elimination, loop unrolling, inlining). **ML Layer 3** predicts the most effective passes.
6. **Assembly Generator**: Translates optimized IR into target assembly instructions.

## ML Integration

The compiler incorporates three Machine Learning layers to bypass expensive deterministic operations:

- **ML Layer 1 (Statement Cache)**: Sits before the Parser. An online frequency table that maps token-type patterns to cached AST nodes. Skips the parser entirely on a cache hit.
- **ML Layer 2 (Parser Dispatch Hint)**: Inside the Parser. A TF-IDF + Random Forest model that predicts the statement type, eliminating conditional branching overhead. If the prediction is rejected by the grammar, it falls back safely.
- **ML Layer 3 (Optimization Strategy Predictor)**: Sits before the Optimizer. A MultiOutputClassifier that takes numeric IR features and predicts which optimization passes will be effective, skipping passes that won't yield improvements.

## LLM Repair Layer

Instead of halting at the first syntax error, the compiler continues through all reachable phases (e.g., using partial tokens for parsing). It gathers Lexer, Parser, and Semantic errors and sends the complete error context to an LLM. This provides the LLM with a full picture of the issues, resulting in highly accurate repair suggestions that are streamed back to the user interface.

## Getting Started

### Prerequisites

- Python 3.9+
- Pip package manager

### Installation

1. Clone the repository and navigate to the project directory:
   ```bash
   cd AI_Assisted_Smart_Compiler
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install fastapi uvicorn pydantic # plus any other requirements (scikit-learn, etc.)
   ```

### Running the Project

**1. Start the FastAPI Backend**
```bash
python backend/main.py
```
The backend will start on `http://0.0.0.0:8000`.

**2. Open the Frontend**
You can serve the `frontend` directory using any static file server, or simply open `frontend/index.html` in your web browser. 
*(If CORS is configured correctly, it will communicate seamlessly with the local backend).*

**3. CLI Compilation (Optional)**
You can also run the compiler entirely via the CLI without the web interface:
```bash
python main.py test.txt
```
Outputs for each phase will be saved as JSON files in the root directory (e.g., `lexer_output.json`, `ast_output.json`, etc.).

## API Endpoints

- `GET /health`: Returns the health status of the API and compiler core.
- `GET /info`: Returns extensive metadata about the compiler phases, ML models, and FAQs.
- `POST /compile`: Accepts raw code and returns phased JSON output, ML statistics, errors, LLM suggestions, and latency comparisons.

## Project Structure

```text
AI_Assisted_Smart_Compiler/
├── backend/          # FastAPI server
│   └── main.py       # API routes and pipeline integration
├── frontend/         # Web interface (HTML, CSS, JS)
│   ├── index.html    # Main compiler view
│   ├── info.html     # Documentation and metrics view
│   ├── script.js     # Frontend logic
│   └── style.css     # UI styling
├── ML/               # ML models and inference logic
├── LLM/              # LLM error repair integration
├── lexer/            # Lexer components
├── AST/              # AST definitions
├── semantic/         # Semantic analysis
├── IR/               # Intermediate Representation
├── optimizer/        # Code optimizer
├── assembly/         # Assembly generation
└── main.py           # Core CLI entry point and pipeline orchestrator
```