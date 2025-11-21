#!/usr/bin/env python3
"""
Example script demonstrating how to use main-minirag.py with PDF documents
"""
import os
import subprocess
import sys
from pathlib import Path

def main():
    # Get absolute path to PDF documents folder
    current_dir = Path(__file__).parent
    pdf_dir = current_dir.parent / "pdf-documents"
    pdf_dir_abs = pdf_dir.resolve()
    
    # Path to main-minirag.py (2 levels up from this script)
    main_script = current_dir.parent.parent / "main-minirag.py"
    
    if not main_script.exists():
        print(f"❌ main-minirag.py not found at {main_script}")
        return 1
        
    if not pdf_dir_abs.exists():
        print(f"❌ PDF directory not found at {pdf_dir_abs}")
        return 1
        
    # Example questions to ask
    example_questions = [
        "Nội dung chính của các tài liệu là gì?",
        "Có những phương pháp research nào được đề cập?",
        "Kết luận chính của nghiên cứu là gì?"
    ]
    
    print("🤖 Mini-RAG Example Script")
    print(f"📁 PDF Directory: {pdf_dir_abs}")
    print(f"🔧 Main Script: {main_script}")
    print()
    
    # Interactive mode
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        print("📝 Example questions:")
        for i, q in enumerate(example_questions, 1):
            print(f"  {i}. {q}")
        print()
        question = input("❓ Enter your question (or press Enter for example): ").strip()
        
        if not question:
            question = example_questions[0]
    
    print(f"🔍 Question: {question}")
    print(f"📂 Processing PDFs in: {pdf_dir_abs}")
    print("-" * 50)
    
    # Run main-minirag.py
    try:
        cmd = [sys.executable, str(main_script), question, str(pdf_dir_abs)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("📤 Output:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️  Warnings/Errors:")
            print(result.stderr)
            
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running main-minirag.py: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())