#!/usr/bin/env python3
"""
Test suite for Course Selection AI Analyzer
Tests all components and steps of the system
"""

import sys
import os
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from course_analyzer import CourseAnalyzer


def test_step0_upload_pdf():
    """Test PDF upload validation"""
    print("Testing Step 0: PDF Upload Validation...")
    analyzer = CourseAnalyzer()
    
    # Test with non-existent file
    result = analyzer.step0_upload_pdf("/nonexistent/file.pdf")
    assert result == False, "Should fail for non-existent file"
    
    # Test with non-PDF file
    result = analyzer.step0_upload_pdf("README.md")
    assert result == False, "Should fail for non-PDF file"
    
    print("✓ Step 0 tests passed")


def test_step2_sample_data():
    """Test sample data loading"""
    print("\nTesting sample data generation...")
    analyzer = CourseAnalyzer()
    analyzer._use_sample_data()
    
    assert len(analyzer.courses) > 0, "Should have sample courses"
    assert all('name' in course for course in analyzer.courses), "All courses should have names"
    assert all('description' in course for course in analyzer.courses), "All courses should have descriptions"
    
    print(f"✓ Loaded {len(analyzer.courses)} sample courses")


def test_step3_evaluation():
    """Test course evaluation with fallback scoring"""
    print("\nTesting Step 3: Course Evaluation...")
    analyzer = CourseAnalyzer()
    analyzer._use_sample_data()
    
    # Set some interests
    analyzer.user_interests = [
        "Field: Computer Science",
        "Career goal: software engineer",
        "Projects: yes"
    ]
    
    evaluated = analyzer.step3_tokenize_and_evaluate()
    
    assert len(evaluated) > 0, "Should have evaluated courses"
    assert all('ai_score' in course for course in evaluated), "All courses should have AI scores"
    
    # Check that scores are properly sorted
    scores = [course['ai_score'] for course in evaluated]
    assert scores == sorted(scores, reverse=True), "Courses should be sorted by score"
    
    print(f"✓ Evaluated {len(evaluated)} courses successfully")


def test_step4_recommendations():
    """Test recommendation generation"""
    print("\nTesting Step 4: Recommendations...")
    analyzer = CourseAnalyzer()
    analyzer._use_sample_data()
    
    analyzer.user_interests = ["Computer Science", "AI"]
    analyzer.graduation_requirements = {
        'total_credits': '120',
        'major_credits': '45'
    }
    
    evaluated = analyzer.step3_tokenize_and_evaluate()
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    analyzer.step4_generate_recommendations(evaluated)
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "AI-Generated Course Recommendations" in output, "Should show recommendations header"
    assert "AI Match Score" in output, "Should show AI scores"
    
    print("✓ Recommendations generated successfully")


def test_graduation_requirements():
    """Test graduation requirements handling"""
    print("\nTesting Step 2.5: Graduation Requirements...")
    analyzer = CourseAnalyzer()
    
    requirements = {
        'total_credits': '120',
        'major_credits': '45',
        'elective_credits': '30',
        'required_courses': 'CS 101, MATH 201'
    }
    
    analyzer.graduation_requirements = requirements
    
    assert analyzer.graduation_requirements == requirements
    print("✓ Graduation requirements stored correctly")


def test_interest_matching():
    """Test that interest matching works correctly"""
    print("\nTesting interest matching algorithm...")
    analyzer = CourseAnalyzer()
    analyzer._use_sample_data()
    
    # Test with AI-focused interests
    analyzer.user_interests = [
        "Field: Artificial Intelligence",
        "Machine Learning",
        "Neural Networks"
    ]
    
    evaluated = analyzer.step3_tokenize_and_evaluate()
    
    # The ML course should rank highly for AI interests
    ml_courses = [c for c in evaluated if 'Machine Learning' in c.get('name', '')]
    if ml_courses:
        ml_score = ml_courses[0]['ai_score']
        # ML course should have a non-zero score
        assert ml_score > 0, "ML course should match AI interests"
    
    # Test with Web Development interests
    analyzer.user_interests = [
        "Field: Web Development",
        "JavaScript",
        "Frontend"
    ]
    
    evaluated = analyzer.step3_tokenize_and_evaluate()
    
    # Web Dev course should rank highly
    web_courses = [c for c in evaluated if 'Web Development' in c.get('name', '')]
    if web_courses:
        web_score = web_courses[0]['ai_score']
        assert web_score > 0, "Web Dev course should match web interests"
    
    print("✓ Interest matching algorithm working correctly")


def test_full_pipeline():
    """Test complete analysis pipeline"""
    print("\nTesting full analysis pipeline...")
    analyzer = CourseAnalyzer()
    analyzer._use_sample_data()
    
    # Simulate full workflow
    analyzer.user_interests = [
        "Field: Computer Science",
        "Preference: practical",
        "Career goal: software engineer"
    ]
    
    analyzer.graduation_requirements = {
        'total_credits': '120',
        'major_credits': '45',
        'elective_credits': '30'
    }
    
    evaluated = analyzer.step3_tokenize_and_evaluate()
    
    # Capture recommendations output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    analyzer.step4_generate_recommendations(evaluated)
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    # Verify output contains expected elements
    assert len(evaluated) > 0, "Should have evaluated courses"
    assert "TOP" in output, "Should show top recommendations"
    
    print("✓ Full pipeline completed successfully")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("COURSE SELECTION AI ANALYZER - TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_step0_upload_pdf,
        test_step2_sample_data,
        test_step3_evaluation,
        test_step4_recommendations,
        test_graduation_requirements,
        test_interest_matching,
        test_full_pipeline
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
