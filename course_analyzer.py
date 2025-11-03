#!/usr/bin/env python3
"""
COURSE SELECTION FUTURISTIC AI ANALYZER 3000
A sophisticated AI-powered course recommendation system
"""

import os
import sys
from typing import List, Dict, Optional, Any

# Optional PDF parsing - gracefully degrade if not available
try:
    import PyPDF2
    HAS_PDF = True
except ImportError:
    HAS_PDF = False
    print("Note: PyPDF2 not installed. PDF parsing disabled.")
    print("To enable PDF parsing, install: pip install PyPDF2")

# Optional AI imports - gracefully degrade if not available
try:
    from transformers import pipeline
    HAS_AI = True
except ImportError:
    HAS_AI = False
    print("Note: AI libraries not installed. Using fallback scoring algorithm.")
    print("To enable full AI features, install: pip install transformers torch")

try:
    import numpy as np
except ImportError:
    np = None


class CourseAnalyzer:
    """Main class for the Course Selection AI Analyzer"""
    
    # Configuration constants
    MAX_COURSES_TO_EVALUATE = 10  # Limit for AI evaluation to manage processing time
    MAX_TOKEN_LENGTH = 512  # Maximum token length for AI model input
    
    def __init__(self):
        self.courses = []
        self.user_interests = []
        self.graduation_requirements = {}
        self.ai_model = None
        
    def step0_upload_pdf(self, pdf_path: str) -> bool:
        """
        Step 0: Ask user to upload course selection book (PDF)
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            bool: True if file exists and is accessible
        """
        if not os.path.exists(pdf_path):
            print(f"Error: File '{pdf_path}' not found!")
            return False
        
        if not pdf_path.lower().endswith('.pdf'):
            print(f"Error: File '{pdf_path}' is not a PDF!")
            return False
        
        print(f"✓ Successfully loaded PDF: {pdf_path}")
        return True
    
    def step1_parse_pdf(self, pdf_path: str) -> List[Dict[str, str]]:
        """
        Step 1: PDF parser - Extract course information from PDF
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of course dictionaries
        """
        print("\n=== Step 1: Parsing PDF ===")
        
        if not HAS_PDF:
            print("❌ PDF parsing not available. PyPDF2 is not installed.")
            print("Using sample course data instead...")
            return []
        
        courses = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num, page in enumerate(pdf_reader.pages):
                    text += page.extract_text()
                    print(f"  Processed page {page_num + 1}/{len(pdf_reader.pages)}")
                
                # Parse the text into courses
                # This is a simplified parser - in production, this would be more sophisticated
                lines = text.split('\n')
                current_course = {}
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Simple heuristic: lines with course codes (e.g., CS 101)
                    if len(line.split()) >= 2 and any(char.isdigit() for char in line.split()[1]):
                        if current_course:
                            courses.append(current_course)
                        current_course = {
                            'name': line,
                            'description': '',
                            'topics': []
                        }
                    elif current_course:
                        current_course['description'] += ' ' + line
                
                if current_course:
                    courses.append(current_course)
                
                self.courses = courses
                print(f"✓ Extracted {len(courses)} courses from PDF")
                return courses
                
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return []
    
    def step2_interactive_questions(self) -> List[str]:
        """
        Step 2: Interactive 20 Questions style narrowing based on interest
        
        Returns:
            List of user interests
        """
        print("\n=== Step 2: Interactive Interest Assessment ===")
        print("Let's narrow down your course options based on your interests!")
        print("Answer the following questions (type your responses):\n")
        
        questions = [
            "What field are you most interested in? (e.g., Computer Science, Mathematics, Physics, etc.)",
            "Do you prefer theoretical or practical courses? (theoretical/practical/both)",
            "What's your career goal? (e.g., software engineer, researcher, data scientist, etc.)",
            "Are you interested in hands-on projects? (yes/no)",
            "Do you prefer working with people or independently? (people/independently/both)",
            "What's your experience level? (beginner/intermediate/advanced)",
            "Are you interested in emerging technologies? (yes/no)",
            "Do you enjoy problem-solving and puzzles? (yes/no)"
        ]
        
        interests = []
        for i, question in enumerate(questions, 1):
            try:
                answer = input(f"Q{i}: {question}\n> ").strip()
                if answer:
                    interests.append(f"{question.split('?')[0]}: {answer}")
                print()
            except (EOFError, KeyboardInterrupt):
                print("\n(Using default responses for non-interactive mode)")
                break
        
        self.user_interests = interests
        print(f"✓ Collected {len(interests)} interest indicators")
        return interests
    
    def step2_5_graduation_requirements(self) -> Dict[str, Any]:
        """
        Step 2.5: Ask about graduation requirements
        
        Returns:
            Dictionary of graduation requirements
        """
        print("\n=== Step 2.5: Graduation Requirements ===")
        print("Let's understand your graduation requirements:\n")
        
        requirements = {}
        
        try:
            requirements['total_credits'] = input("How many total credits do you need? (e.g., 120)\n> ").strip()
            requirements['major_credits'] = input("How many major-specific credits? (e.g., 45)\n> ").strip()
            requirements['elective_credits'] = input("How many elective credits? (e.g., 30)\n> ").strip()
            requirements['required_courses'] = input("List any required courses (comma-separated):\n> ").strip()
            
        except (EOFError, KeyboardInterrupt):
            print("\n(Using default requirements for non-interactive mode)")
            requirements = {
                'total_credits': '120',
                'major_credits': '45',
                'elective_credits': '30',
                'required_courses': ''
            }
        
        self.graduation_requirements = requirements
        print(f"✓ Recorded graduation requirements")
        return requirements
    
    def step3_tokenize_and_evaluate(self) -> List[Dict]:
        """
        Step 3: Tokenizer and AI model evaluation
        
        Returns:
            List of evaluated courses with scores
        """
        print("\n=== Step 3: AI Model Evaluation ===")
        
        if HAS_AI:
            print("Initializing AI model...")
            try:
                # Use a lightweight sentiment/classification model for evaluation
                # In production, you might use a more specialized model
                self.ai_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
                print("✓ AI model loaded successfully")
                
                evaluated_courses = []
                
                # Create a context string from user interests
                interest_context = " ".join(self.user_interests)
                
                print(f"\nEvaluating {len(self.courses)} courses...")
                for course in self.courses[:self.MAX_COURSES_TO_EVALUATE]:
                    # Combine course info with user interests for evaluation
                    evaluation_text = f"User interests: {interest_context}. Course: {course.get('name', '')} {course.get('description', '')[:200]}"
                    
                    # Truncate if too long
                    if len(evaluation_text) > self.MAX_TOKEN_LENGTH:
                        evaluation_text = evaluation_text[:self.MAX_TOKEN_LENGTH]
                    
                    try:
                        result = self.ai_model(evaluation_text)[0]
                        course['ai_score'] = result['score'] if result['label'] == 'POSITIVE' else 1 - result['score']
                        course['ai_label'] = result['label']
                        evaluated_courses.append(course)
                    except Exception as e:
                        print(f"  Warning: Could not evaluate course - {str(e)[:50]}")
                        continue
                
                # Sort by AI score
                evaluated_courses.sort(key=lambda x: x.get('ai_score', 0), reverse=True)
                
                print(f"✓ Evaluated {len(evaluated_courses)} courses")
                return evaluated_courses
                
            except Exception as e:
                print(f"Error in AI evaluation: {e}")
                print("Falling back to keyword-based scoring...")
                return self._fallback_scoring()
        else:
            print("Using keyword-based scoring algorithm (AI libraries not available)...")
            return self._fallback_scoring()
    
    def _fallback_scoring(self) -> List[Dict]:
        """
        Fallback scoring method when AI is not available
        Uses keyword matching between user interests and course descriptions
        """
        evaluated_courses = []
        
        # Extract keywords from user interests
        interest_keywords = set()
        for interest in self.user_interests:
            words = interest.lower().split()
            interest_keywords.update(word.strip(',.!?:;') for word in words if len(word) > 3)
        
        print(f"Analyzing courses based on {len(interest_keywords)} interest keywords...")
        
        for course in self.courses:
            # Combine course text
            course_text = f"{course.get('name', '')} {course.get('description', '')}".lower()
            
            # Count keyword matches
            matches = sum(1 for keyword in interest_keywords if keyword in course_text)
            
            # Calculate score (0 to 1)
            score = min(matches / max(len(interest_keywords), 1), 1.0)
            
            course['ai_score'] = score
            course['ai_label'] = 'MATCHED' if score > 0.3 else 'LOW_MATCH'
            evaluated_courses.append(course)
        
        # Sort by score
        evaluated_courses.sort(key=lambda x: x.get('ai_score', 0), reverse=True)
        
        print(f"✓ Scored {len(evaluated_courses)} courses using keyword matching")
        return evaluated_courses
    
    def step4_generate_recommendations(self, evaluated_courses: List[Dict]) -> None:
        """
        Step 4: Use the AI to generate final recommendations
        
        Args:
            evaluated_courses: List of courses with AI scores
        """
        print("\n" + "="*60)
        print("=== Step 4: AI-Generated Course Recommendations ===")
        print("="*60)
        
        if not evaluated_courses:
            print("No courses available for recommendation.")
            return
        
        print(f"\n📚 Based on your interests and graduation requirements,")
        print(f"   here are your TOP {min(5, len(evaluated_courses))} recommended courses:\n")
        
        for i, course in enumerate(evaluated_courses[:5], 1):
            score = course.get('ai_score', 0)
            name = course.get('name', 'Unknown Course')
            description = course.get('description', 'No description available')[:150]
            
            print(f"{i}. {name}")
            print(f"   AI Match Score: {score:.2%}")
            print(f"   {description}...")
            print()
        
        print("="*60)
        print("\n✨ Analysis complete! These courses align well with your goals.")
        
    def run_full_analysis(self, pdf_path: Optional[str] = None):
        """
        Run the complete course analysis pipeline
        
        Args:
            pdf_path: Optional path to PDF file
        """
        print("\n" + "="*60)
        print("🎓 COURSE SELECTION FUTURISTIC AI ANALYZER 3000 🎓")
        print("="*60)
        
        # Step 0: Upload PDF
        if pdf_path is None:
            try:
                pdf_path = input("\nStep 0: Enter path to your course selection PDF:\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nNo PDF provided. Using demo mode with sample data.")
                self._use_sample_data()
                pdf_path = None
        
        if pdf_path and self.step0_upload_pdf(pdf_path):
            # Step 1: Parse PDF
            self.step1_parse_pdf(pdf_path)
        else:
            print("Using sample course data for demonstration...")
            self._use_sample_data()
        
        # Step 2: Interactive questions
        self.step2_interactive_questions()
        
        # Step 2.5: Graduation requirements
        self.step2_5_graduation_requirements()
        
        # Step 3: Tokenize and evaluate with AI
        evaluated_courses = self.step3_tokenize_and_evaluate()
        
        # Step 4: Generate recommendations
        self.step4_generate_recommendations(evaluated_courses)
    
    def _use_sample_data(self):
        """Load sample course data for demonstration"""
        self.courses = [
            {
                'name': 'CS 101 - Introduction to Programming',
                'description': 'Learn fundamental programming concepts using Python. Topics include variables, loops, functions, and basic data structures. Perfect for beginners.',
                'topics': ['Python', 'Programming', 'Algorithms']
            },
            {
                'name': 'CS 201 - Data Structures and Algorithms',
                'description': 'Advanced study of data structures including trees, graphs, and hash tables. Learn algorithm analysis and design patterns.',
                'topics': ['Algorithms', 'Data Structures', 'Complexity']
            },
            {
                'name': 'CS 301 - Machine Learning',
                'description': 'Introduction to machine learning algorithms, neural networks, and AI applications. Hands-on projects with real-world datasets.',
                'topics': ['AI', 'Machine Learning', 'Neural Networks']
            },
            {
                'name': 'CS 305 - Database Systems',
                'description': 'Study of relational databases, SQL, normalization, and transaction processing. Includes practical database design projects.',
                'topics': ['Databases', 'SQL', 'Data Management']
            },
            {
                'name': 'CS 401 - Software Engineering',
                'description': 'Learn software development lifecycle, agile methodologies, testing, and team collaboration. Large-scale project included.',
                'topics': ['Software Engineering', 'Agile', 'Project Management']
            },
            {
                'name': 'MATH 201 - Linear Algebra',
                'description': 'Study of vector spaces, matrices, eigenvalues, and linear transformations. Essential for computer graphics and ML.',
                'topics': ['Mathematics', 'Linear Algebra', 'Vectors']
            },
            {
                'name': 'CS 350 - Computer Networks',
                'description': 'Exploration of network protocols, internet architecture, and distributed systems. Lab work with network programming.',
                'topics': ['Networking', 'Protocols', 'Distributed Systems']
            },
            {
                'name': 'CS 420 - Artificial Intelligence',
                'description': 'Advanced AI concepts including search algorithms, knowledge representation, and natural language processing.',
                'topics': ['AI', 'NLP', 'Search Algorithms']
            },
            {
                'name': 'CS 315 - Web Development',
                'description': 'Full-stack web development covering HTML, CSS, JavaScript, and modern frameworks. Build complete web applications.',
                'topics': ['Web Development', 'JavaScript', 'Frontend']
            },
            {
                'name': 'CS 405 - Cybersecurity',
                'description': 'Learn security principles, cryptography, network security, and ethical hacking techniques.',
                'topics': ['Security', 'Cryptography', 'Ethical Hacking']
            }
        ]


def main():
    """Main entry point"""
    analyzer = CourseAnalyzer()
    
    # Check if PDF path provided as command line argument
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    analyzer.run_full_analysis(pdf_path)


if __name__ == "__main__":
    main()
