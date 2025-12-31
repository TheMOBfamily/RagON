# VSCode Tasks & Keybindings

## Phím tắt (Keybindings)

| Phím tắt | Task | Mô tả |
|----------|------|-------|
| `Ctrl+Alt+Shift+C` | Copy File to System Clipboard | Copy file vào clipboard, paste được trong Nautilus |

## Tasks (F1 > Run Task)

| Task | Mô tả |
|------|-------|
| Open PDF with Evince | Mở file PDF đang chọn bằng Evince |
| Copy File to System Clipboard | Copy file vào system clipboard |
| Deutschfuns: Run Claude-Code in Terminal | Mở Claude Code trong gnome-terminal |

## Cách sử dụng

### Copy file vào clipboard
1. Click file trong Explorer
2. Nhấn `Ctrl+Alt+Shift+C`
3. Paste vào Nautilus bằng `Ctrl+V`

### Mở PDF
1. Click file PDF trong Explorer
2. `F1` > gõ "Run Task" > chọn "Open PDF with Evince"

## Files

- `tasks.json` - Định nghĩa các tasks
- `copy-to-clipboard.py` - Script copy file vào clipboard
- `open-pdf.py` - Script mở PDF bằng Evince
- `~/.config/Code/User/keybindings.json` - Keybindings (user-level, không phải workspace)

## Dependencies

- `xclip`: `sudo apt install xclip`
- `evince`: `sudo apt install evince`
