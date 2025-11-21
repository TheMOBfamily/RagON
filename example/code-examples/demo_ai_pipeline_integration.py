#!/usr/bin/env python3
"""
Demo script showing how to integrate Mini-RAG output into AI pipelines
"""
import subprocess
import sys
from pathlib import Path

def get_rag_context(question: str, pdf_path: str) -> str:
    """Extract context from PDF collection using Mini-RAG"""
    main_script = Path(__file__).parent.parent.parent / "main-minirag.py"
    
    try:
        result = subprocess.run([
            sys.executable, str(main_script), question, pdf_path
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: RAG processing timed out"
    except Exception as e:
        return f"Error: {e}"

def demonstrate_ai_pipeline_integration():
    """Demonstrate various use cases for AI pipeline integration"""
    
    pdf_dir = str(Path(__file__).parent.parent / "pdf-documents")
    
    print("🤖 Mini-RAG AI Pipeline Integration Demo")
    print("=" * 50)
    
    # Use Case 1: Research Analysis
    print("\n📊 Use Case 1: Research Methodology Analysis")
    print("-" * 40)
    question1 = "What research methodologies are discussed in these papers?"
    context1 = get_rag_context(question1, pdf_dir)
    
    print(f"Query: {question1}")
    print("\nRAG Output:")
    print(context1[:500] + "..." if len(context1) > 500 else context1)
    
    print("\n💡 Pipeline Usage:")
    print("This output can be fed into an AI model for:")
    print("- Methodology comparison analysis")
    print("- Research gap identification") 
    print("- Literature review synthesis")
    
    # Use Case 2: Concept Extraction
    print("\n\n📚 Use Case 2: Technical Concept Extraction")
    print("-" * 40)
    question2 = "Extract key technical concepts and definitions"
    context2 = get_rag_context(question2, pdf_dir)
    
    print(f"Query: {question2}")
    print("\nRAG Output:")
    print(context2[:500] + "..." if len(context2) > 500 else context2)
    
    print("\n💡 Pipeline Usage:")
    print("Perfect for:")
    print("- Building knowledge graphs")
    print("- Creating glossaries")
    print("- Domain-specific training data")
    
    # Use Case 3: Shell Integration Example
    print("\n\n🔧 Use Case 3: Shell Pipeline Integration")
    print("-" * 40)
    
    shell_example = f"""#!/bin/bash
# Extract document summary
CONTEXT=$(python main-minirag.py "Summarize key findings" {pdf_dir})

# Feed to AI analysis tool (pseudo-code)
echo "Based on this research context: $CONTEXT" | ai-analysis-tool --analyze

# Or save for batch processing
echo "$CONTEXT" > research_context.txt
"""
    
    print("Shell script example:")
    print(shell_example)
    
    # Use Case 4: Python Integration Example
    print("\n🐍 Use Case 4: Python Integration Pattern")
    print("-" * 40)
    
    python_example = '''
def analyze_research_papers(pdf_directory, analysis_prompt):
    # Step 1: Extract context using Mini-RAG
    context = get_rag_context("Summarize methodologies and findings", pdf_directory)
    
    # Step 2: Prepare AI prompt with context
    full_prompt = f"""
    Based on the following research context:
    
    {context}
    
    {analysis_prompt}
    """
    
    # Step 3: Send to AI model (your choice of API)
    # response = ai_model.complete(full_prompt)
    # return response
    
# Usage:
# result = analyze_research_papers("/path/to/pdfs", "Identify research gaps")
'''
    
    print("Python integration pattern:")
    print(python_example)
    
    print("\n" + "=" * 50)
    print("✅ Demo completed! Mini-RAG is ready for AI pipeline integration.")
    print("\nKey Benefits:")
    print("- Works offline (no API keys required)")
    print("- Structured output suitable for AI consumption")
    print("- Smart caching for fast repeated queries")
    print("- Comprehensive logging for debugging")

if __name__ == "__main__":
    demonstrate_ai_pipeline_integration()