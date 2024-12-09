# MetaPrompt Forge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

LLM Prompt Engineering on steroids. Transform simple queries into structured prompts that push language models to their limits while maintaining factual accuracy.

## 🎯 What it Does

- **Eliminates Hallucinations**: Forces LLMs to cite sources for every claim
- **Maximizes Useful Output**: Pushes models to provide comprehensive, detailed responses
- **Ensures Verifiability**: Every piece of information can be fact-checked against specified sources
- **Structures Knowledge**: Transforms chaotic information dumps into organized, academic-grade responses

## 🚀 Key Benefits

- **Deep Dive Responses**: Pushes LLMs beyond surface-level answers
- **Source Validation**: Get responses you can actually verify
- **No More "I think"**: Forces concrete statements with evidence
- **Quality Control**: Built-in checks for information accuracy
- **Maximum Value**: Extracts the most detailed knowledge the model has

## 🛠 Technical Stack

- **GUI**: Built with tkinter
- **API**: Requests for Ollama communication
- **Threading**: Non-blocking operations
- **Font Handling**: Custom font configuration
- **Error Management**: Comprehensive error handling

## ⚡ Quick Start

```bash
# Clone repo
git clone https://github.com/yourusername/metaprompt-forge.git
cd metaprompt-forge

# Install dependency
pip install requests

# Run
python main.py
```

### Requirements
- Python 3.7+
- requests library
- Ollama running locally (default: http://localhost:11434) or remotely

## 💡 Features

### Core Features
- Model selection dropdown with auto-refresh
- Configurable Ollama API URL
- Real-time status updates
- Copy to clipboard functionality
- Asynchronous prompt generation

### UI Components
- Input text area with scrolling
- Output text area with scrolling
- Status bar for feedback
- Generate and Copy buttons
- Model refresh button

## 🎬 Example

Your query: "Tell me about quantum computing"

Becomes a structured prompt that:
- Requires peer-reviewed sources
- Demands specific examples and applications
- Forces real-world implementation citations
- Requires current research references
- Separates established facts from theoretical concepts

## 📦 Project Structure

```
main.py     # Main application file
```

## 🤝 Contributing

PRs welcome! Open an issue first for major changes.

## 📄 License

MIT

## 💬 Support

Open an issue in the GitHub repository.
