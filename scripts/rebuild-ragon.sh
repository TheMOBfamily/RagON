#!/bin/bash
# rebuild-ragon.sh - Rebuild RagON index và test với 30 keywords
# Tạo: 2026-01-30 | Tác giả: Fong + Claude
# Vị trí deploy: ~/Desktop/rebuild-ragon.sh (máy Quyên)

set -e

# === CONFIG ===
RAGON_DIR="/home/fong/Projects/RagON"
DKM_DIR="$RAGON_DIR/DKM-PDFs"
INDEX_DIR="$DKM_DIR/.mini_rag_index"
LOG_FILE="$RAGON_DIR/rebuild-$(date +%Y%m%d_%H%M%S).log"
VENV_DIR="$RAGON_DIR/venv"

# === COLORS ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# === FUNCTIONS ===
log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✅ $1${NC}" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}⚠️  $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}❌ $1${NC}" | tee -a "$LOG_FILE"
    exit 1
}

# === 30 TEST KEYWORDS (cover 20 sách mới) ===
# Mỗi sách có 1-2 keywords đặc trưng
TEST_KEYWORDS=(
    # 1. Laravel Beyond CRUD - Brent Roose
    "Laravel Beyond CRUD"
    "Brent Roose domain"
    # 2. Docker for Web Developers
    "Docker container web"
    "Docker compose"
    # 3. JavaScript Cookbook - Adam Powers
    "JavaScript array methods"
    "Promise async await"
    # 4. Mastering TypeScript - Nathan Rozentals
    "TypeScript enterprise modules"
    # 5. TypeScript 4 Design Patterns
    "TypeScript design patterns"
    # 6. Laravel Queues in Action - Mohamed Said
    "Laravel queue job"
    "Redis queue Laravel"
    # 7. Learning TypeScript - Josh Goldberg
    "TypeScript basics generics"
    "TypeScript interfaces"
    # 8. phparchitect Domain-Driven
    "PHP domain driven"
    # 9. React Key Concepts - Schwarzmüller
    "React hooks useState"
    "React component lifecycle"
    # 10. Consuming APIs in Laravel - Ash Allen
    "Laravel HTTP client"
    # 11. Laravel Concepts Part 1 - Martin Joo
    "Laravel service container"
    # 12. Laravel Concepts Part 2 - Martin Joo
    "Laravel middleware events"
    # 13. Mastering JavaScript Functional Programming
    "functional programming JavaScript"
    # 14. Next.js Cookbook - Andrei Tazetdinov
    "Next.js server components"
    "Next.js routing"
    # 15. TypeScript Cookbook - Stefan Baumgartner
    "TypeScript type-level"
    # 16. Effective TypeScript - Dan Vanderkam
    "TypeScript best practices"
    "TypeScript narrowing"
    # 17. phparchitect Command Line Picasso
    "PHP CLI Artisan"
    "PHP command line"
    # 18. Professional JavaScript - Matt Frisbie
    "JavaScript DOM manipulation"
    # 19. The Road to React - Robin Wieruch
    "React state management"
    "Robin Wieruch React"
    # 20. TypeScript 5 Design Patterns
    "TypeScript decorators"
)

# === MAIN ===
echo ""
echo "=============================================="
echo "   RagON Index Rebuild Script"
echo "   $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================================="
echo ""

cd "$RAGON_DIR" || error "Không tìm thấy thư mục RagON"

# Step 1: Count PDFs
log "Đếm số PDF hiện tại..."
PDF_COUNT=$(ls "$DKM_DIR"/*.PDF "$DKM_DIR"/*.pdf 2>/dev/null | wc -l)
success "Tổng số PDF: $PDF_COUNT"

# Step 2: Backup index (nếu có)
log "Backup index cũ..."
if [ -d "$INDEX_DIR" ]; then
    BACKUP_DIR="${INDEX_DIR}.$(date +%Y%m%d_%H%M%S).b"
    cp -r "$INDEX_DIR" "$BACKUP_DIR"
    success "Backup tại: $BACKUP_DIR"
else
    warn "Không có index để backup"
fi

# Step 3: Remove old index
log "Xóa index cũ..."
rm -rf "$INDEX_DIR"
success "Đã xóa index cũ"

# Step 4: Activate venv
log "Kích hoạt môi trường ảo..."
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
    success "Venv activated"
else
    error "Không tìm thấy venv tại $VENV_DIR"
fi

# Step 5: Rebuild index
log "Rebuild index (có thể mất 30-60 phút)..."
echo ""
echo "----------------------------------------"
python "$RAGON_DIR/main-minirag.py" "Test rebuild query" "$DKM_DIR" 2>&1 | tee -a "$LOG_FILE"
echo "----------------------------------------"
echo ""
success "Rebuild hoàn tất"

# Step 6: Test với 30 keywords
log "Test với 30 keywords..."
echo ""
PASS_COUNT=0
FAIL_COUNT=0

for i in "${!TEST_KEYWORDS[@]}"; do
    keyword="${TEST_KEYWORDS[$i]}"
    idx=$((i + 1))

    echo -n "[$idx/30] Testing: \"$keyword\"... "

    # Chạy query và kiểm tra output
    OUTPUT=$(python "$RAGON_DIR/main-minirag.py" "$keyword" "$DKM_DIR" 2>&1)

    # Kiểm tra xem có kết quả không (không phải error)
    if echo "$OUTPUT" | grep -qi "error\|exception\|không tìm thấy"; then
        echo -e "${RED}FAIL${NC}"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    else
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    fi
done

echo ""
echo "=============================================="
echo "   KẾT QUẢ TEST"
echo "=============================================="
echo -e "   ${GREEN}PASS: $PASS_COUNT${NC}"
echo -e "   ${RED}FAIL: $FAIL_COUNT${NC}"
echo "   TOTAL: ${#TEST_KEYWORDS[@]}"
echo "=============================================="

# Summary
echo ""
if [ $FAIL_COUNT -eq 0 ]; then
    success "Tất cả test PASS! Index rebuild thành công."
else
    warn "$FAIL_COUNT keywords không tìm thấy kết quả."
fi

log "Log file: $LOG_FILE"
echo ""
echo "Done!"
