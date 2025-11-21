# Centralized notices/messages for multi-query tools
import os

_DKM_PATH = os.getenv("DKM_PDF_PATH", "$DKM_PDF_PATH")

THINK_ULTRA_NOTICE = (
    "Activate Think Ultra (deep analytical mode) and select up to nine books from the\n"
    "list that are most relevant to the current problem.\n"
    "\n"
    "CRITICAL: Each book has a pre-generated knowledge index available at:\n"
    f"  {_DKM_PATH}/<file_hash>/index-toc.json\n"
    "\n"
    "This index contains:\n"
    "  • Complete table of contents (with page numbers)\n"
    "  • Comprehensive multi-point summary (key concepts, patterns, methods, principles)\n"
    "  • 5W1H analysis (who, what, when, where, why, how)\n"
    "  • Topical tags for quick reference\n"
    "  • Book metadata (title, authors, year, publisher, ISBN, edition)\n"
    "\n"
    "THINK ULTRA: If needed to understand a book's structure and applicability, locate\n"
    "and read its index-toc.json file. Use this prepared knowledge intelligently and\n"
    "creatively—think 'out of the box' to apply concepts across domains. Optimize for\n"
    "intelligence, effectiveness, speed, accuracy, rigor, and standards compliance."
)

PDF_LIST_NOTICE = (
    "⚠️  IMPORTANT NOTICE ⚠️\n"
    "\n"
    "Due to the large number of books (hundreds), use smart filtering to find relevant books:\n"
    "  • grep/rg: echo '<json>' | jq -r '.[] | select(.filename | contains(\"keyword\"))'\n"
    "  • jq pattern: jq '[.[] | select(.filename | test(\"pattern\"; \"i\"))]'\n"
    "  • Multiple filters: jq '[.[] | select((.filename | contains(\"python\")) or (.filename | contains(\"clean\")))]'\n"
    "\n"
    "TIP: Each book has index-toc.json with full metadata and summary for quick evaluation."
)
