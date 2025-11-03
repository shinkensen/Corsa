# Course Selection AI Analyzer - Architecture Documentation

## System Overview

The Course Selection Futuristic AI Analyzer 3000 is a modular, step-by-step system that helps students select courses based on their interests, graduation requirements, and career goals using AI-powered analysis.

## Architecture

### Core Components

```
CourseAnalyzer (Main Class)
│
├── Step 0: PDF Upload (step0_upload_pdf)
│   └── Validates PDF files before processing
│
├── Step 1: PDF Parser (step1_parse_pdf)
│   └── Extracts course information from PDFs
│   └── Fallback: Uses sample data if PDF parsing unavailable
│
├── Step 2: Interactive Questions (step2_interactive_questions)
│   └── Collects user interests through targeted questions
│   └── Builds user profile for matching
│
├── Step 2.5: Graduation Requirements (step2_5_graduation_requirements)
│   └── Collects credit requirements
│   └── Identifies required courses
│
├── Step 3: AI Evaluation (step3_tokenize_and_evaluate)
│   ├── Primary: Transformer-based AI model (if available)
│   └── Fallback: Keyword-based scoring algorithm
│
└── Step 4: Recommendations (step4_generate_recommendations)
    └── Generates ranked course recommendations
    └── Displays top matches with scores
```

## Design Principles

### 1. Graceful Degradation
The system is designed to work with or without external dependencies:
- **No PyPDF2**: Uses sample data or manual course input
- **No AI libraries**: Falls back to keyword-based scoring
- **No user input**: Can be used programmatically

### 2. Modularity
Each step is a separate method that can be:
- Called independently
- Tested in isolation
- Extended or replaced

### 3. Flexibility
- Works in interactive mode (CLI)
- Works in programmatic mode (Python API)
- Supports both PDF and manual course input

## Data Flow

```
1. INPUT STAGE
   PDF File OR Sample Data
   ↓
   User Interests (Q&A)
   ↓
   Graduation Requirements

2. PROCESSING STAGE
   Course Parsing
   ↓
   Interest Keywords Extraction
   ↓
   AI/Keyword Matching
   ↓
   Score Calculation

3. OUTPUT STAGE
   Ranked Course List
   ↓
   Top 5 Recommendations
   ↓
   Match Scores & Descriptions
```

## Scoring Algorithm

### AI-Powered Scoring (Primary)
When transformers library is available:
1. Combines user interests with course description
2. Uses DistilBERT sentiment analysis model
3. Generates compatibility score (0-1)
4. Ranks courses by score

### Keyword-Based Scoring (Fallback)
When AI libraries unavailable:
1. Extracts keywords from user interests (words > 3 chars)
2. Searches for keyword matches in course text
3. Calculates match ratio: matches / total_keywords
4. Ranks courses by match ratio

## File Structure

```
Corsa/
├── course_analyzer.py          # Main application
├── example_usage.py            # Usage examples
├── test_analyzer.py            # Test suite
├── create_sample_pdf.py        # PDF generator utility
├── requirements.txt            # Minimal dependencies
├── requirements-optional.txt   # Full AI features
├── README.md                   # User documentation
└── .gitignore                  # Git ignore patterns
```

## Extension Points

### Adding New Question Types
Add questions to `step2_interactive_questions()`:
```python
questions.append("Your new question here?")
```

### Custom Course Parsers
Override `step1_parse_pdf()` for different PDF formats:
```python
def custom_parser(self, pdf_path):
    # Your parsing logic
    return parsed_courses
```

### Alternative AI Models
Modify `step3_tokenize_and_evaluate()`:
```python
self.ai_model = pipeline("text-classification", model="your-model")
```

### Custom Scoring Algorithms
Implement custom `_scoring_method()`:
```python
def _custom_scoring(self):
    # Your scoring logic
    return scored_courses
```

## Performance Considerations

### Memory Usage
- Sample data: ~10 KB
- AI model: ~250-500 MB (first download)
- PDF parsing: ~1-10 MB per PDF

### Processing Time
- PDF parsing: 1-5 seconds per PDF
- AI evaluation: 2-10 seconds (first run, includes model loading)
- Keyword scoring: < 1 second
- Subsequent runs: < 1 second (model cached)

## Security Considerations

1. **PDF Parsing**: Uses PyPDF2 which is safe for text extraction
2. **User Input**: All inputs are treated as strings, no code execution
3. **File Access**: Only reads specified PDF files
4. **AI Model**: Uses pre-trained HuggingFace models (verified)

## Future Enhancements

### Planned Features
- [ ] Web interface (Flask/FastAPI)
- [ ] Database integration for course storage
- [ ] Multi-language support
- [ ] Schedule conflict detection
- [ ] Prerequisite validation
- [ ] Professor rating integration
- [ ] Course difficulty estimation
- [ ] Peer comparison

### Possible Improvements
- [ ] Custom AI model training on course data
- [ ] Natural language query interface
- [ ] Integration with university APIs
- [ ] Mobile app version
- [ ] Collaborative filtering recommendations
- [ ] Career path alignment scoring

## Testing

Run tests with:
```bash
python3 test_analyzer.py
```

Run examples with:
```bash
python3 example_usage.py
```

Test with sample data:
```bash
python3 course_analyzer.py
# Press Enter to skip PDF upload
# Answer questions or press Enter for defaults
```

## Troubleshooting

### "PyPDF2 not installed"
Solution: `pip install PyPDF2` or use sample data

### "AI libraries not installed"
Solution: `pip install transformers torch` or use keyword scoring

### "Error parsing PDF"
- Check PDF is not encrypted/password-protected
- Verify PDF contains extractable text (not scanned images)
- Try converting PDF to text first

### "No courses found"
- System falls back to sample data automatically
- Check PDF format and content
- Use sample data for testing

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - See LICENSE file for details
