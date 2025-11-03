#!/usr/bin/env python3
"""
Example usage of the Course Selection AI Analyzer
This demonstrates how to use the system programmatically
"""

from course_analyzer import CourseAnalyzer


def example_basic_usage():
    """Basic usage example"""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    analyzer = CourseAnalyzer()
    
    # Use sample data
    analyzer._use_sample_data()
    
    # Set some predefined interests
    analyzer.user_interests = [
        "Field: Computer Science",
        "Preference: practical",
        "Career goal: software engineer",
        "Projects: yes",
        "Work style: both"
    ]
    
    # Set graduation requirements
    analyzer.graduation_requirements = {
        'total_credits': '120',
        'major_credits': '45',
        'elective_credits': '30',
        'required_courses': 'CS 101, MATH 201'
    }
    
    # Evaluate courses
    evaluated = analyzer.step3_tokenize_and_evaluate()
    
    # Generate recommendations
    analyzer.step4_generate_recommendations(evaluated)


def example_with_specific_interests():
    """Example with specific interests in AI/ML"""
    print("\n" + "=" * 60)
    print("Example 2: AI/ML Focused Student")
    print("=" * 60)
    
    analyzer = CourseAnalyzer()
    analyzer._use_sample_data()
    
    # Student interested in AI/ML
    analyzer.user_interests = [
        "Field: Artificial Intelligence",
        "Preference: both theoretical and practical",
        "Career goal: machine learning engineer",
        "Projects: yes",
        "Experience: intermediate",
        "Emerging tech: yes",
        "Problem solving: yes"
    ]
    
    analyzer.graduation_requirements = {
        'total_credits': '120',
        'major_credits': '48',
        'elective_credits': '24'
    }
    
    evaluated = analyzer.step3_tokenize_and_evaluate()
    analyzer.step4_generate_recommendations(evaluated)


def example_web_development_focus():
    """Example with web development focus"""
    print("\n" + "=" * 60)
    print("Example 3: Web Development Focus")
    print("=" * 60)
    
    analyzer = CourseAnalyzer()
    analyzer._use_sample_data()
    
    # Student interested in web development
    analyzer.user_interests = [
        "Field: Web Development",
        "Preference: practical",
        "Career goal: full stack developer",
        "Projects: yes",
        "Work style: people",
        "Experience: beginner"
    ]
    
    analyzer.graduation_requirements = {
        'total_credits': '120',
        'major_credits': '42',
        'elective_credits': '36'
    }
    
    evaluated = analyzer.step3_tokenize_and_evaluate()
    analyzer.step4_generate_recommendations(evaluated)


if __name__ == "__main__":
    # Run all examples
    example_basic_usage()
    example_with_specific_interests()
    example_web_development_focus()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
