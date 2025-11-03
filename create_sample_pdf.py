#!/usr/bin/env python3
"""
Sample PDF Generator for Testing
Creates a sample course catalog PDF for testing the PDF parser
"""

# Note: This is a demonstration script showing what a PDF would contain
# To actually generate PDFs, you would need: pip install reportlab

SAMPLE_COURSE_CATALOG = """
UNIVERSITY COURSE CATALOG 2024-2025

COMPUTER SCIENCE DEPARTMENT

CS 101 - Introduction to Programming
Prerequisites: None
Credits: 3
Learn fundamental programming concepts using Python. Topics include variables, 
loops, functions, and basic data structures. Perfect for beginners with no prior 
programming experience. Hands-on lab sessions included.

CS 201 - Data Structures and Algorithms
Prerequisites: CS 101
Credits: 4
Advanced study of data structures including trees, graphs, hash tables, and heaps.
Learn algorithm analysis, complexity theory, and design patterns. Essential for
technical interviews and advanced coursework.

CS 301 - Machine Learning
Prerequisites: CS 201, MATH 201
Credits: 4
Introduction to machine learning algorithms including supervised and unsupervised
learning. Cover neural networks, deep learning, and practical AI applications.
Hands-on projects with real-world datasets using Python and TensorFlow.

CS 305 - Database Systems
Prerequisites: CS 201
Credits: 3
Comprehensive study of relational databases, SQL, normalization, ACID properties,
and transaction processing. Learn database design principles and includes practical
projects building complete database applications.

CS 315 - Web Development
Prerequisites: CS 101
Credits: 3
Full-stack web development covering HTML, CSS, JavaScript, React, Node.js, and
modern frameworks. Build complete web applications from scratch. Learn responsive
design and modern web development practices.

CS 350 - Computer Networks
Prerequisites: CS 201
Credits: 4
Exploration of network protocols, TCP/IP stack, internet architecture, and
distributed systems. Lab work includes network programming, packet analysis,
and building networked applications.

CS 401 - Software Engineering
Prerequisites: CS 201
Credits: 4
Learn software development lifecycle, agile methodologies, version control,
testing strategies, and team collaboration. Includes large-scale team project
applying industry best practices.

CS 405 - Cybersecurity
Prerequisites: CS 350
Credits: 3
Learn security principles, cryptography, network security, web security, and
ethical hacking techniques. Hands-on labs covering penetration testing and
security auditing.

CS 420 - Artificial Intelligence
Prerequisites: CS 301
Credits: 4
Advanced AI concepts including search algorithms, knowledge representation,
planning, natural language processing, and computer vision. Explore cutting-edge
AI research and applications.

MATH 201 - Linear Algebra
Prerequisites: MATH 101
Credits: 3
Study of vector spaces, matrices, eigenvalues, eigenvectors, and linear
transformations. Essential foundation for computer graphics, machine learning,
and scientific computing.
"""


def create_sample_txt():
    """Create a sample text file showing course catalog content"""
    filename = "sample_course_catalog.txt"
    
    with open(filename, 'w') as f:
        f.write(SAMPLE_COURSE_CATALOG)
    
    print(f"✓ Created {filename}")
    print("\nThis text file shows the content of a course catalog.")
    print("To test with an actual PDF, convert this to PDF using:")
    print("  - Online converters (e.g., text-to-pdf.com)")
    print("  - Microsoft Word or Google Docs (Save as PDF)")
    print("  - Command line: enscript -B -p output.ps input.txt && ps2pdf output.ps output.pdf")
    print("\nOr install reportlab: pip install reportlab")


def create_sample_pdf_with_reportlab():
    """Create a sample PDF using reportlab (if available)"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import inch
        
        filename = "sample_course_catalog.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Split content into paragraphs
        paragraphs = SAMPLE_COURSE_CATALOG.strip().split('\n\n')
        
        for para in paragraphs:
            if para.strip():
                # Use title style for course names and headers
                if any(para.startswith(x) for x in ['UNIVERSITY', 'COMPUTER SCIENCE', 'CS ', 'MATH ']):
                    style = styles['Heading2'] if para.startswith('CS ') or para.startswith('MATH ') else styles['Heading1']
                else:
                    style = styles['Normal']
                
                p = Paragraph(para.strip().replace('\n', '<br/>'), style)
                story.append(p)
                story.append(Spacer(1, 0.2 * inch))
        
        doc.build(story)
        print(f"✓ Created {filename}")
        print("\nYou can now test the PDF parser with:")
        print(f"  python3 course_analyzer.py {filename}")
        return True
        
    except ImportError:
        print("reportlab not installed. Cannot create PDF directly.")
        print("Install with: pip install reportlab")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("SAMPLE COURSE CATALOG GENERATOR")
    print("=" * 60)
    print()
    
    # Always create text version
    create_sample_txt()
    print()
    
    # Try to create PDF if reportlab available
    if not create_sample_pdf_with_reportlab():
        print("\nFalling back to text file only.")
        print("You can manually convert sample_course_catalog.txt to PDF.")
