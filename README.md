# Corsa - Course Selection Futuristic AI Analyzer 3000 🎓🤖

An AI-powered course recommendation system that helps students select the perfect courses based on their interests, graduation requirements, and career goals.

## Features

- **PDF Upload & Parsing**: Upload your course selection book PDF and automatically extract course information
- **Interactive Assessment**: Answer personalized questions to help the AI understand your interests
- **Graduation Requirements**: Input your specific graduation requirements for tailored recommendations
- **AI-Powered Analysis**: Uses advanced NLP models to evaluate course compatibility with your profile
- **Smart Recommendations**: Get top course recommendations ranked by AI-calculated match scores

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shinkensen/Corsa.git
cd Corsa
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Note: The AI model will automatically download on first run (requires internet connection).

## Usage

### Basic Usage (Interactive Mode)

Run the analyzer in interactive mode:
```bash
python course_analyzer.py
```

The system will guide you through:
- Step 0: Upload your course selection PDF
- Step 1: Automatic PDF parsing
- Step 2: Interactive questions about your interests
- Step 2.5: Graduation requirements input
- Step 3: AI model evaluation
- Step 4: Personalized course recommendations

### With PDF Path

Provide the PDF path as a command-line argument:
```bash
python course_analyzer.py /path/to/course_catalog.pdf
```

### Demo Mode

If no PDF is provided, the system runs in demo mode with sample course data.

## How It Works

### Step 0: PDF Upload
Users can upload their course selection book in PDF format. The system validates the file and prepares it for parsing.

### Step 1: PDF Parser
The parser extracts text from the PDF and identifies courses, descriptions, and other relevant information using pattern recognition.

### Step 2: Interactive Questions
A series of targeted questions helps the system understand:
- Field of interest
- Theoretical vs. practical preference
- Career goals
- Learning style
- Experience level

### Step 2.5: Graduation Requirements
The system collects information about:
- Total required credits
- Major-specific credits
- Elective credits
- Required courses

### Step 3: AI Tokenization & Evaluation
- User interests and course descriptions are tokenized
- An open-source transformer model evaluates compatibility
- Each course receives an AI-calculated match score

### Step 4: AI Recommendations
The system generates a ranked list of recommended courses based on:
- AI match scores
- User interests
- Graduation requirements
- Career alignment

## Example Output

```
🎓 COURSE SELECTION FUTURISTIC AI ANALYZER 3000 🎓
============================================================

=== Step 4: AI-Generated Course Recommendations ===

📚 Based on your interests and graduation requirements,
   here are your TOP 5 recommended courses:

1. CS 301 - Machine Learning
   AI Match Score: 95.23%
   Introduction to machine learning algorithms, neural networks...

2. CS 420 - Artificial Intelligence
   AI Match Score: 92.18%
   Advanced AI concepts including search algorithms...

...
```

## Requirements

- Python 3.8+
- PyPDF2 (PDF parsing)
- transformers (AI models)
- torch (ML framework)
- sentence-transformers (text embeddings)
- numpy (numerical operations)

## Architecture

The system follows a modular pipeline architecture:

```
CourseAnalyzer
├── step0_upload_pdf()          # File validation
├── step1_parse_pdf()           # Text extraction
├── step2_interactive_questions() # User profiling
├── step2_5_graduation_requirements() # Requirements gathering
├── step3_tokenize_and_evaluate() # AI analysis
└── step4_generate_recommendations() # Final output
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Future Enhancements

- Web interface for easier interaction
- Support for multiple PDF formats
- Custom AI model training on course data
- Integration with university course APIs
- Schedule optimization
- Prerequisite checking
- Professor ratings integration