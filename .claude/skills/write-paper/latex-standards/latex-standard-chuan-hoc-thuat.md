


---
2026-01-25
Bây giờ tôi sẽ tạo báo cáo cuối cùng toàn diện.

## Báo Cáo: Các Chuẩn Mực LaTeX Học Thuật Hiện Nay (2025-2026)

### Tổng Quan Thực Thi

LaTeX vẫn là tiêu chuẩn trong xuất bản học thuật, đặc biệt đối với các tạp chí và hội thảo có nội dung toán học, khoa học máy tính và kỹ thuật. Năm 2025 chứng kiến sự hợp nhất các tiêu chuẩn và tập trung vào khả năng tiếp cận (accessibility), với các tổ chức lớn như ACM, IEEE, NeurIPS, và Springer Nature cung cấp các template chính thức và hướng dẫn rõ ràng.[1][2][3][4]

### I. Các Chuẩn Mực Chính của Tổ Chức

#### ACM (Association for Computing Machinery)

ACM đã hợp nhất tám template độc lập thành một package duy nhất - **acmart.cls**. Đây là tiêu chuẩn quan trọng nhất cho các tập chí và hội thảo khoa học máy tính.[1]

**Yêu cầu chính:**
- **Document Class**: acmsmall (hầu hết journals), acmlarge (IMWUT, JOCCH, TAP), acmtog (TOG), sigconf (hầu hết proceedings)[1]
- **Font**: Libertine (bắt buộc, không được thay thế)[2]
- **Lề**: Cố định - không được điều chỉnh[2]
- **Phiên bản**: Cập nhật gần nhất là 2 tháng 1 năm 2025[2]
- **Yêu cầu submit**: Sử dụng mode "manuscript" cho peer review; loại bỏ tất cả hướng dẫn từ template trước khi submit[5][2]

**Đặc điểm quan trọng**: ACM rất nghiêm ngặt về việc không cho phép tùy chỉnh margins hoặc fonts. Nếu file metadata chứa ký tự không-ASCII (accents, diacritics), sẽ bị từ chối. Chỉ chấp nhận plain ASCII cho title, author, keywords.[6][2]

#### IEEE (Institute of Electrical and Electronics Engineers)

IEEE là chuẩn phổ biến cho các hội thảo điện tử, viễn thông, và kỹ thuật.

**Quy định định dạng:**
- **Kích thước giấy**: US Letter (8.5" × 11") hoặc A4 (210mm × 297mm)[7][8]
- **Định dạng**: Hai cột[8]
- **Lề** (tính bằng inches):[8]
  - Top: 0.75" (19mm)
  - Bottom: 1.69" (43mm)  
  - Left/Right: 0.56" (14.32mm)
  - Khoảng cách giữa cột: 0.17" (4.22mm)
- **Font text**: Times New Roman hoặc Times (bắt buộc)[8]
- **Cỡ chữ** (theo bảng chuẩn):[8]
  - Title: 24pt Regular
  - Author: 11pt Regular
  - Affiliation: 10pt Italic
  - Body: 10pt Regular
  - References: 8pt
- **Cấm**: Type 3 fonts[8]

**Tiêu đề**: Mỗi từ phải viết hoa ngoại trừ: "a", "an", "and", "as", "at", "by", "for", "from", "if", "in", "into", "on", "or", "of", "the", "to", "with"[8]

#### NeurIPS (Neural Information Processing Systems)

Chuẩn chặt cho hội thảo machine learning hàng đầu.

**Yêu cầu chi tiết:**
- **Vùng văn bản**: 5.5 inches (33 picas) rộng × 9 inches (54 picas) dài[3]
- **Lề trái**: 1.5 inch (9 picas)[3]
- **Cỡ chữ**: 10 point[3]
- **Leading (khoảng dòng)**: 11 points[3]
- **Font ưu tiên**: Times New Roman[3]
- **Tiêu đề bài**: 17 point, bold, centered giữa hai horizontal rules[9]
- **Khoảng cách đoạn**: 1/2 line space (5.5 points), không indent[3]
- **Bắt buộc**: Sử dụng official NeurIPS LaTeX style files từ website chính[10][3]

**Ngôn ngữ**: Mặc dù không yêu cầu giống ACM, NeurIPS cũng khuyến cáo tránh UTF-8 đặc biệt trong metadata để tránh vấn đề processing[10]

#### Springer Nature

Springer đã áp dụng phương pháp "content-first" với emphasis trên accessibility.[4][11][12]

**Đặc điểm:**
- **Font**: Không dùng custom fonts[12]
- **Encoding**: Chuyển đổi ký tự đặc biệt thành TeX code (ä → \"a)[12]
- **Citation**: Hỗ trợ cả numerical và author-year styles[11]
- **Cấu trúc**: Decimal numbering system cho headings[11]
- **Minimal formatting**: Không format toàn bộ đoạn bằng italics[11]

**Template**: Springer cung cấp template chính thức trên Overleaf cập nhật tháng 12 năm 2024[4]

### II. Cấu Trúc Document & Best Practices Hiện Đại

#### Document Hierarchy

LaTeX cung cấp các mức tiêu đề tiêu chuẩn:[13]
- **\\chapter{}** - Chỉ trong book/report classes
- **\\section{}** - Level 1 (mục chính)
- **\\subsection{}** - Level 2 (mục phụ)
- **\\subsubsection{}** - Level 3 (mục nhỏ, tối đa)

**Best practice**: Tránh sử dụng \\newline hay \\\\ để tạo paragraph spacing. Thay vào đó, sử dụng blank lines[14][13]

#### Bibliography Management

Có ba cách chính để quản lý tài liệu tham khảo:[15][16]

1. **BibTeX + natbib** (phổ biến nhất)[15]
   - `\usepackage[options]{natbib}`
   - `\bibliographystyle{stylename}`
   - Commands: `\cite{}`, `\citet{}`, `\citep{}`
   - Style phổ biến: abbrvnat, plainnat, dinat[15]

2. **BibLaTeX** (khuyến cáo cho project mới)[15]
   - Tích hợp tốt hơn với TeX engines hiện đại
   - Hỗ trợ localization đầy đủ
   - `\usepackage[options]{biblatex}`
   - `\printbibliography`

3. **Tệp .bib structure**[16]
   - Format: `@article{bibID, author={...}, title={...}, year={...}}`
   - Các loại phổ biến: @article, @book, @proceedings, @online, @inproceedings
   - Cần compile hai lần để generate bibliography đúng[16]

**Lỗi thường gặp**: Không sử dụng hard space (tilde ~) trước citations. Đúng: `James~\cite{James96}`[17]

#### Figures & Tables

**Vị trí captions**:[18][19]
- **Figures**: Caption đặt **dưới** figure
- **Tables**: Caption đặt **trên** table (chuẩn mực quốc tế)[19]

**Format caption**:
- Figure: "**Fig. 1.** Descriptive caption text"
- Table: "**Table 1.** Descriptive caption text"

**Best practices**:
- Luôn sử dụng `\label{}` để cross-reference[20]
- Sử dụng floating environments (figure, table)[20]
- Tránh `\includegraphics` với manual positioning - dùng commands tự động[3]
- Sử dụng caption package để tùy chỉnh spacing[21]

#### Mathematics & Equations

**Package bắt buộc**:[22][23]
```latex
\usepackage{amsmath}      % Xử lý equations
\usepackage{amssymb}      % AMS symbols
\usepackage{amsfonts}     % AMS fonts
```

**Environments khuyến cáo**:[23]
- `equation` - Numbered single equation
- `equation*` - Unnumbered
- `align` - Multiple equations aligned
- `gather` - Grouped equations
- **Tránh**: `eqnarray` (spacing không chính xác)[23]

**Font trong math**:[23]
- `\mathbb{}` từ amsfonts (không dùng \\bbold)
- Tránh Computer Modern cho thường xuyên trong text mode

### III. Multi-file Projects & Organization

#### Phương pháp Import[24][25]

| Lệnh | Đặc điểm | Khi nào dùng |
|------|---------|------------|
| `\input{file}` | Đơn giản, không preamble | Các file nhỏ, không cần compile độc lập |
| `\include{file}` | Có page break, hỗ trợ \\includeonly | Chapters, tối ưu hóa compile time |
| `\subfile{file}` | Compile được độc lập | Mỗi chapter tự chứa preamble |
| `\import{dir}{file}` | Quản lý nested imports tốt | Large projects với cấu trúc folder |

**Cấu trúc đề xuất**:[24]
```
main.tex
├── chapters/
│   ├── chapter1.tex
│   └── chapter2.tex
├── sections/
│   ├── introduction.tex
│   └── conclusion.tex
├── images/
└── data/
```

#### Package Import Order

Thứ tự quan trọng đối với một số packages:[26]
```latex
\usepackage{varioref}
\usepackage{hyperref}
\usepackage{cleveref}
```

Sai thứ tự có thể gây ra lỗi incompatibility[26]

### IV. Encoding & Special Characters

#### UTF-8 Setup (Khuyến cáo)[27][28]

```latex
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
```

Điều này cho phép sử dụng trực tiếp các ký tự đặc biệt như: á, é, ñ, ü, etc.[28]

**Alternatives cho Unicode đầy đủ**:[27]
- **XeLaTeX** hoặc **LuaLaTeX** - Native UTF-8 support
- `\usepackage{fontspec}` cho full font control
- Tốt cho scripts không-Latin (Cyrillic, Greek, CJK)[27]

**Tránh trong ACM/IEEE**:[6][8]
- Không dùng UTF-8 cho metadata (title, author) - sử dụng plain ASCII
- Điều này được nhấn mạnh để đảm bảo compatibility với tất cả systems[6]

#### Custom Unicode Characters[28]

```latex
\DeclareUnicodeCharacter{codepoint}{TeX sequence}
```

Ví dụ: `\DeclareUnicodeCharacter{0177}{\^y}` cho ŷ

### V. Accessibility & Tagged PDF (Xu Hướng 2025)

Một xu hướng quan trọng là yêu cầu PDF tagged để tuân thủ các tiêu chuẩn accessibility như Section 508 (Mỹ) và WCAG 2.0.[29][30]

#### Tạo PDF Tagged[31][29]

**Phương pháp 1: accessibility package**[29]
```latex
\usepackage[tagged]{accessibility}
```

**Phương pháp 2: tagpdf (mới nhất 2025)**[32]
```latex
\RequirePackage{tagpdf}  % Trước documentclass
\documentclass{article}
\tagpdfsetup{tabsorder=structure,activate-all}
```

**Phương pháp 3: Native PDF/UA-2 (Built-in 2025+)**[32]
```latex
\DocumentMetadata{
  lang = en,
  tagging = on,
  pdfstandard = ua-2
}
\documentclass{article}
```

#### Alternative Text cho Images[30]

```latex
\includegraphics[width=0.2\textwidth, alt={Description}]{image.png}
```

Hoặc decorative images (không được đọc bởi screen readers):
```latex
\includegraphics[width=0.2\textwidth, artifact]{image.png}
```

**Lợi ích**: Cho phép screen readers mô tả chính xác hình ảnh, đáp ứng WCAG 2.0 standards[30]

### VI. Các Lỗi Thường Gặp & Cách Tránh

#### Lỗi Font[17][8]

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-----------|---------|
| Type 3 fonts | Sử dụng bitmap fonts | Dùng TrueType hoặc embedded fonts, tránh \\bbold |
| Font không embedded | PDF viewers không có font | Kiểm tra PDF properties, compile với fontspec |
| Computer Modern | Mặc định ở LaTeX | Tải package serif/sans cụ thể |

#### Lỗi Structure[33]

- **Sai**: `$$a=b$$` → Dùng `\[a=b.\]` thay vào
- **Sai**: `\\ \\ \\` để tạo spacing → Dùng blank lines
- **Sai**: Không sử dụng labels → Mọi equation/figure cần `\label{}`
- **Sai**: Manual spacing → Dùng built-in commands (e.g., `\medskip`)[33]

#### Lỗi Bibliography[17][33]

- Không sort bibliography → Sort theo last name[33]
- Inconsistent styles → Tất cả entries phải cùng format[33]
- Không hard space trước cite → Dùng: `James~\cite{James96}`[17]

#### Lỗi Submission[34]

**arxiv.org quy định**:[34]
- Absolute filenames → Sử dụng relative paths
- Spaces trong filenames → Sử dụng underscores/hyphens
- Missing files → Kiểm tra \input/\include paths
- Non-ASCII filenames → Chỉ ASCII cho filenames

### VII. Checklists Trước Submit

#### Pre-submission Checklist

1. **Format & Validation**
   - [ ] Sử dụng official template từ conference/journal
   - [ ] Loại bỏ tất cả guidance text từ template
   - [ ] Test PDF output cẩn thận
   - [ ] Kiểm tra page count vs. limit
   
2. **Typography**
   - [ ] Fonts embedded (check PDF properties)
   - [ ] Không có Type 3 fonts
   - [ ] Margins/spacing không bị thay đổi
   - [ ] Tất cả ký tự display đúng

3. **Content**
   - [ ] Metadata (title, author) đúng format (plain ASCII nếu yêu cầu)
   - [ ] Cross-references (citations, figures, tables) đầy đủ
   - [ ] Bibliography compiled đúng (chạy bibtex)
   - [ ] Không có citations tới non-existent materials

4. **Accessibility** (nếu yêu cầu)
   - [ ] PDF được tag (accessibility check)
   - [ ] Alt-text cho tất cả figures
   - [ ] Heading hierarchy consistent
   - [ ] Colors không phải thông tin duy nhất

5. **File Organization**
   - [ ] Source files organized logically
   - [ ] Tất cả paths relative (không absolute)
   - [ ] Images/data files included nếu bắt buộc
   - [ ] File sizes reasonable

#### Conference-specific Checklist

**ICML 2025**:[35]
- [ ] Upload tới papercheck.icml.cc
- [ ] Nhận 5-letter submission code
- [ ] No Type 3 font check (new this year)
- [ ] Vector graphics preferred (eps/pdf)

**IEEE INFOCOM**:[36]
- [ ] 10-point Times font, two-column
- [ ] Không override default settings từ IEEEtran.cls
- [ ] Margins/spacing từ original template

**NeurIPS 2025**:[10]
- [ ] Official style files từ NeurIPS website
- [ ] Page limit enforcement (exceeded → auto reject)
- [ ] UTF-8 encoding cẩn thận (metadata issues)

### VIII. Tools & Resources (2025)

#### Official Templates & Tools

| Platform | Ưu điểm |
|----------|---------|
| **Overleaf** | Cloud-based, collaboration, official templates, real-time compilation[5][37] |
| **GitHub** | Version control, CI/CD integration, free hosting |
| **Local TeX** | Full control, offline, tất cả TeX engines (PDFTeX, XeTeX, LuaTeX) |

#### Template Sources

- **ACM**: https://www.acm.org/publications/proceedings-template
- **IEEE**: https://www.ieee.org/conferences/publishing/templates
- **NeurIPS**: https://neurips.cc/Conferences/2025/PaperInformation/StyleFiles
- **Springer**: https://www.overleaf.com/gallery/tagged/springer
- **ICML**: https://media.icml.cc/Conferences/ICML2025/Styles/

### Kết Luận

Các chuẩn mực LaTeX học thuật năm 2025-2026 cho thấy sự hội tụ xung quanh:

1. **Công nghệ**: Sử dụng Overleaf cloud platform thay vì local installations
2. **Accessibility**: Yêu cầu ngày càng tăng về PDF tagged và WCAG compliance
3. **Consolidation**: ACM hợp nhất templates; Springer đơn giản hóa workflows
4. **Strictness**: Các tổ chức (đặc biệt ACM) không cho phép tùy chỉnh styling
5. **UTF-8 Caution**: Tránh UTF-8 trong metadata để đảm bảo processing compatibility

**Khuyến cáo chính**:
- Luôn sử dụng **official template** từ conference/journal cụ thể[1][4][2][3]
- Test PDF output cẩn thận trước khi submit[36]
- Không tùy chỉnh margins/fonts nếu template cấm[36][2]
- Sử dụng Overleaf để tránh TeX distribution issues[37][5]
- Đối với accessibility: enable tagging nếu yêu cầu[31][29]

***

**Các nguồn chính**:
 ACM - https://www.acm.org/publications/proceedings-template[1]
 ACM LaTeX Best Practices - https://www.acm.org/publications/taps/latex-best-practices[2]
 IEEE Paper Format - https://meu.edu.in/wp-content/uploads/2025/06/IEEE-Paper-Format.pdf[8]
 NeurIPS 2023 Formatting - https://media.neurips.cc/Conferences/NeurIPS2023/Styles/neurips_2023.pdf[3]
 Springer Nature LaTeX - https://www.overleaf.com/latex/templates/springer-nature-latex-template/myxmhdsbzkyd[4]

Sources
[1] Perancangan Game Edukasi berbasis Android pada Mata Pelajaran Bahasa Inggris Kelas X di SMAS Pertiwi 2 Padang Tahun Ajaran 2025/2026 https://ejournal.nusantaraglobal.ac.id/index.php/sentri/article/view/4534
[2] ACM Master Article Template https://www.acm.org/publications/proceedings-template
[3] Formatting Instructions For NeurIPS 2023 https://media.neurips.cc/Conferences/NeurIPS2023/Styles/neurips_2023.pdf
[4] Submitting a Paper in IEEE LaTeX Format https://www.reddit.com/r/LaTeX/comments/1jfs1da/submitting_a_paper_in_ieee_latex_format/
[5] ACM Conference Proceedings Primary Article Template https://www.overleaf.com/latex/templates/acm-conference-proceedings-primary-article-template/wbvnghjbzwpc
[6] Formatting Instructions for Authors Using LaTeX https://arxiv.org/html/2405.06128v1
[7] Both ACM and IEEE proceedings use letter size : r/Metric https://www.reddit.com/r/Metric/comments/a1rbxs/both_acm_and_ieee_proceedings_use_letter_size/
[8] IEEE-Paper-Format.pdf https://meu.edu.in/wp-content/uploads/2025/06/IEEE-Paper-Format.pdf
[9] Formatting instructions for NeurIPS 2018 https://media.nips.cc/Conferences/NIPS2018/Styles/nips_2018.pdf
[10] 4.1 Citations Within The... https://arxiv.org/html/2505.10292v1
[11] Manuscript Guidelines | Publish your research https://www.springernature.com/gp/authors/publish-a-book/manuscript-guidelines
[12] LaTeX author support | Publish your research https://www.springernature.com/gp/authors/campaigns/latex-author-support
[13] LaTeX/Document Structure https://en.wikibooks.org/wiki/LaTeX/Document_Structure
[14] Learn LaTeX in 30 minutes https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes
[15] Bibliography management with natbib https://www.overleaf.com/learn/latex/Bibliography_management_with_natbib
[16] BibTex - Getting Started with LaTeX https://guides.nyu.edu/LaTeX/bibtex
[17] How to Avoid Common Conversion Problems LATEX–XML https://www.itsoc.org/sites/default/files/2022-04/TIT-FinalSubmissions.pdf
[18] Images, Figures and Tables - Referencing style - IEEE https://guides.library.uwa.edu.au/IEEE/images_tables_figures
[19] Full guide to captions customization in LaTeX https://latex-tutorial.com/caption-customization-latex/
[20] LaTeX/Floats, Figures and Captions https://en.wikibooks.org/wiki/LaTeX/Floats,_Figures_and_Captions
[21] Use the “caption” package to customize your tables and ... https://lazyscientist.wordpress.com/2016/12/26/use-the-caption-package-to-customize-your-tables-and-figures-in-latex/
[22] Package amsmath https://ctan.org/pkg/amsmath?lang=en
[23] User's Guide for the amsmath Package (Version 2.1) https://www.latex-project.org/help/documentation/amsldoc.pdf
[24] Management in a large project https://www.overleaf.com/learn/latex/Management_in_a_large_project
[25] Multi-file LaTeX projects https://www.overleaf.com/learn/latex/Multi-file_LaTeX_projects
[26] LaTeX Best Practices: Lessons Learned from Writing a ... https://www.semipol.de/posts/2018/06/latex-best-practices-lessons-learned-from-writing-a-phd-thesis/
[27] How to Compile Latex Documents With Utf-8 Encoding? https://www.baeldung.com/cs/latex-utf-8-compile
[28] LaTeX/Special Characters https://en.wikibooks.org/wiki/LaTeX/Special_Characters
[29] The 'accessibility' package for tagged PDF documents https://ctan.math.washington.edu/tex-archive/macros/latex/contrib/accessibility/accessibility.pdf
[30] Make PDF submission accessible https://ieeevis.org/year/2025/info/call-participation/make-pdf-accessible
[31] Tagged and Accessible PDF with ... https://www.latex-project.org/publications/2022-FMi-PDFA-slides.pdf
[32] Some Updates on Tagged PDF documents - Accessibility in ... https://research.kent.ac.uk/pqm/2025/10/20/latex-accessibility-updates/
[33] Common Latex Errors (and how to AVOID THEM) https://u.cs.biu.ac.il/~tsaban/Pdf/LaTeXCommonErrs.pdf
[34] Common Mistakes that cause Automated Processing to Fail https://info.arxiv.org/help/faq/mistakes.html
[35] ICML 2025 Author Instructions https://icml.cc/Conferences/2025/AuthorInstructions
[36] Paper Submission Instructions [Main Conference] https://infocom2025.ieee-infocom.org/authors/paper-submission-instructions-main-conference
[37] Templates - Journals, CVs, Presentations, Reports and More https://www.overleaf.com/latex/templates
[38] The Use Of Facebook To Improve Students’ Writing Skill: An Experimental Study At The Second Grade Students Of SMAN 1 Batukliang Utara In Academic Year 2025/2026 https://ejournal.mandalanursa.org/index.php/JUPE/article/view/9928
[39] Critical Analysis of Draft UGC (Minimum Qualifications for Appointment and Promotion of Teachers and Academic Staff in Universities and Colleges and Measures for the Maintenance of Standards in Higher Education) Regulations, 2025: Teachers' Perspective https://www.questjournals.org/jrhss/papers/vol13-issue3/1303229236.pdf
[40] Critical Pedagogical Analysis of Permendikdasmen No. 9 of 2025: The Contradiction of Academic Ability Tests (TKA) in the Context of Revitalising Vocational High Schools (SMK) https://transpublika.co.id/ojs/index.php/JRPP/article/view/1084
[41] The Role Of Standards In The Regulation Of Artificial Intelligence In Uzbekistan https://theusajournals.com/index.php/ijlc/article/view/7177/6638
[42] Indonesia Economic and Development Outlook 2026: Why Five Percent Growth Is No Longer Enough for a Rising Economy https://journal.bappenas.go.id/index.php/jpp/article/view/791
[43] Faculty perceptions on quality standards in online placement tests https://www.tandfonline.com/doi/full/10.1080/2331186X.2025.2505293
[44] International Financial Reporting Standards and Earnings Management: A Global Research Landscape Analysis https://rsisinternational.org/journals/ijrsi/article.php?id=23
[45] Response to the Financial Accounting Standards Board’s Invitation to Comment on Financial Key Performance Indicators for Business Entities https://publications.aaahq.org/jfr/article/doi/10.2308/JFR-2025-022/14179/Response-to-the-Financial-Accounting-Standards
[46] Response to the Financial Accounting Standards Board’s “Proposed Accounting Standards Update—Government Grants (Topic 832): Accounting for Government Grants by Business Entities” https://publications.aaahq.org/jfr/article/10/2/1/13870/Response-to-the-Financial-Accounting-Standards
[47] LaTeX, metadata, and publishing workflows https://arxiv.org/pdf/2301.08277.pdf
[48] LIVE: LaTex Interactive Visual Editing http://arxiv.org/pdf/2405.06762.pdf
[49] StainFuser: Controlling Diffusion for Faster Neural Style Transfer in
  Multi-Gigapixel Histology Images https://arxiv.org/html/2403.09302v1
[50] Evaluating the Effectiveness of Microarchitectural Hardware Fault
  Detection for Application-Specific Requirements https://arxiv.org/html/2408.05810v1
[51] The multiple classes of ultra-diffuse galaxies: Can we tell them apart? https://arxiv.org/html/2412.01901v1
[52] Scalable Surrogate Verification of Image-based Neural Network Control
  Systems using Composition and Unrolling https://arxiv.org/html/2405.18554v2
[53] Event-scale Internal Tide Variability via X-band Marine Radar https://arxiv.org/html/2404.18218v1
[54] Human-Aligned Skill Discovery: Balancing Behaviour Exploration and
  Alignment https://arxiv.org/html/2501.17431v1
[55] Format Requirements - Graduate College - University of Illinois https://grad.illinois.edu/academics/thesis-dissertation/format-requirements
[56] LaTeX for Academic Writing - Complete Guide for Students ... https://resources.latex-cloud-studio.com/blog/latex-academic-writing-guide
[57] Formatting Guidelines - Rackham Graduate School https://rackham.umich.edu/navigating-your-degree/formatting-guidelines/
[58] Preparing Articles for the ACM Transactions with LATEX https://www.sigecom.org/exchanges/submissions/instructions.pdf
[59] Thesis formatting | Department of Computer Science and ... https://www.cst.cam.ac.uk/local/phd/typography
[60] LaTeX Best Practices https://www.acm.org/publications/taps/latex-best-practices
[61] Advice to write a PhD thesis using LaTeX? https://www.reddit.com/r/LaTeX/comments/12lxmu0/advice_to_write_a_phd_thesis_using_latex/
[62] Formatting in LaTeX - Submit and Publish Your Thesis https://guides.library.utoronto.ca/thesis/formatting_latex
[63] Manuscript Templates for Conference Proceedings https://www.ieee.org/conferences/publishing/templates
[64] KTBox: A Modular LaTeX Framework for Semantic Color, Structured Highlighting, and Scholarly Communication https://arxiv.org/abs/2510.01961
[65] AcademAI: An Intelligent Framework for Automated Research Synthesis and Conference Recommendation https://www.ijraset.com/best-journal/academai
[66] The Impact of Work-Life Balance Dimensions on Job Performance Amongst Faculty Members at Private University in Malaysia: The Mediating Role of Perceived Organizational Support https://mysitasi.mohe.gov.my/journal-website/get-meta-article?artId=a08ca7bd-f8ef-45b5-88b2-4ed1e3995f50&formatted=true
[67] Innovating Education: The Impact of Artificial Intelligence and Technology on Teaching https://invergejournals.com/index.php/ijss/article/view/125
[68] A Comprehensive Analysis of Social Media’s Influence on English Vocabulary Development in Pakistan https://invergejournals.com/index.php/ijss/article/view/161
[69] Emotion Analysis from Customer Shopping Experience using ML https://www.ijraset.com/best-journal/emotion-analysis-from-customer-shopping-experience-using-ml-864
[70] Emotion Analysis from Customer Shopping Experience using ML https://www.ijraset.com/best-journal/emotion-analysis-from-customer-shopping-experience-using-ml
[71] IMECE2022-XXXX A LATEX TEMPLATE FOR ASME CONFERENCE PAPERS: asmeconf.cls https://www.semanticscholar.org/paper/7f1cbfdbd4ab64864058c467f1e28c22891e6880
[72] IMECE2025-XXXX A LATEX TEMPLATE FOR ASME CONFERENCE PAPERS: asmeconf.cls https://www.semanticscholar.org/paper/b63451fe25fde6add940ebf569106d476c35140c
[73] Measuring Resource Efficiency of LATEX Paper Templates https://dl.gi.de/handle/20.500.12116/43357
[74] Cogito, ergo sum: A Neurobiologically-Inspired Cognition-Memory-Growth
  System for Code Generation https://arxiv.org/html/2501.18653v1
[75] Pragmatist: Multiview Conditional Diffusion Models for High-Fidelity 3D
  Reconstruction from Unposed Sparse Views https://arxiv.org/html/2412.08412v1
[76] Latent Space Symmetry Discovery https://arxiv.org/html/2310.00105v2
[77] HCL-MTSAD: Hierarchical Contrastive Consistency Learning for Accurate
  Detection of Industrial Multivariate Time Series Anomalies https://arxiv.org/html/2404.08224v1
[78] Enhancing Digital Hologram Reconstruction Using Reverse-Attention Loss
  for Untrained Physics-Driven Deep Learning Models with Uncertain Distance https://arxiv.org/html/2403.12056v1
[79] Mol-CADiff: Causality-Aware Autoregressive Diffusion for Molecule
  Generation https://arxiv.org/html/2503.05499v1
[80] Towards Robust Spacecraft Trajectory Optimization via Transformers https://arxiv.org/html/2410.05585v2
[81] Springer Nature Latex Template | PDF https://www.scribd.com/document/671818643/springer-nature-latex-template
[82] Manuscript Templates for Conference Proceedings – IEEE CAI 2025 https://cai.ieee.org/2025/manuscript-templates-for-conference-proceedings/
[83] Springer Nature LaTeX Template https://www.overleaf.com/latex/templates/springer-nature-latex-template/myxmhdsbzkyd
[84] IEEE Conference Template - Overleaf, Online LaTeX Editor https://www.overleaf.com/latex/templates/ieee-conference-template/grfzhhncsfqn
[85] NeurIPS 2024 Formatting Guidelines | PDF | Standard Error https://www.scribd.com/document/818063544/neurips-2024
[86] VSCode LaTeX Template for IEEE Conference Paper format https://github.com/alvinwilta/ieee-conference-latex
[87] NeurIPS 2022 Style Files https://neurips.cc/Conferences/2022/PaperInformation/StyleFiles
[88] Submit a LaTeX manuscript to a Springer Nature journal ... https://support.nature.com/en/support/solutions/articles/6000127538-submit-a-latex-manuscript-to-a-springer-nature-journal-using-overleaf
[89] Book review: L ATEX and Friends https://www.semanticscholar.org/paper/5ca4290a39a3d70da6ac3b38ea029227b8190949
[90] Testing MOND on small bodies in the remote solar system https://arxiv.org/html/2403.09555v1
[91] Internal Representations in Spiking Neural Networks, criticality and the
  Renormalization Group https://arxiv.org/html/2409.02238v1
[92] SiT: Symmetry-Invariant Transformers for Generalisation in Reinforcement
  Learning https://arxiv.org/html/2406.15025v1
[93] Cosmic-ray confinement in radio bubbles by micromirrors https://arxiv.org/html/2404.05110v1
[94] Semantic Neural Radiance Fields for Multi-Date Satellite Data https://arxiv.org/html/2502.16992v1
[95] Captions for Figures and Tables | Style for Students Online https://www.e-education.psu.edu/styleforstudents/c4_p12.html
[96] Aligning equations with amsmath https://www.overleaf.com/learn/latex/Aligning_equations_with_amsmath
[97] LaTeX/Bibliography Management https://en.wikibooks.org/wiki/LaTeX/Bibliography_Management
[98] Bibliography Packages - BibTeX, natbib, biblatex https://guides.library.yale.edu/bibtex/bibliography-documentation
[99] [PDF] AMS-LA TEX Version 1.2 User's Guide https://www.ndsu.edu/sites/default/files/fileadmin/math/_Old/Resources/Tex_and_LaTeX/Tex_and_LaTeX_Bibliography_and_templates/AMS-LaTeX_User_s_guide.pdf
[100] LaTeX for Publications: Creating a Bibliography with BibTeX https://libguides.uiwtx.edu/c.php?g=1337391&p=10039164
[101] User's Guide for the amsmath Package (Version 2.0) https://www.pvv.ntnu.no/~berland/latex/docs/amsldoc.pdf
[102] Best Practices for Constructing Knowledge Graphs in Retrieval-Augmented Generation (RAG) Systems https://ieeexplore.ieee.org/document/11234485/
[103] 5.M. Scientific session: Health4EUKids: Best practices implemented to European countries to combat childhood obesity https://academic.oup.com/eurpub/article/doi/10.1093/eurpub/ckaf161.283/8302222
[104] Exploring the Best Practices in Teaching Filipino 6 At Southeast Butuan District: Basis For A Proposed Enhancement of Learning Action Cell (LAC) Sessions https://www.randwickresearch.com/index.php/rielsj/article/view/1176
[105] Innovations in Monitoring and Evaluation Systems for Project Tracking: Applying Global Best Practices in Nairobi https://rsisinternational.org/journals/ijrsi/article.php?id=1070
[106] Supporting Veteran’ Society in Entrepreneurship: Best Practices for Entrepreneurship Centers in Higher Education Institutions in the United States https://www.rcis.ro/images/documente/rcis90_05.pdf
[107] Quality Assurance in Higher Education: Best Practices, Challenges, and Future Directions https://ejournal.ppsdp.org/index.php/pijed/article/view/869
[108] An Approach Related to Best Practices in Sports Medicine: A Literature Review https://prismaods.latindes.org/index.php/pods/article/view/94
[109] Communication in AYA survivorship clinical settings: Best practices and challenges. https://ascopubs.org/doi/10.1200/JCO.2025.43.16_suppl.e22020
[110] The EU instant payments regulation and payment packages – interpretation and best practices https://ejournals.eu/en/journal/financial-law-review/article/the-eu-instant-payments-regulation-and-payment-packages-interpretation-and-best-practices
[111] Molecular Testing in Solid Tumors: Best Practices from the Molecular Pathology and Precision Medicine Study Group of the Italian Society of Pathology (PMMP/SIAPeC). https://www.pathologica.it/article/view/1214
[112] NeuRaLaTeX: A machine learning library written in pure LaTeX https://arxiv.org/pdf/2503.24187.pdf
[113] BACON: Improving Clarity of Image Captions via Bag-of-Concept Graphs https://arxiv.org/html/2407.03314v2
[114] Inconsistencies in TeX-Produced Documents https://arxiv.org/pdf/2407.15511.pdf
[115] Best Practices for Data Publication in the Astronomical Literature https://arxiv.org/pdf/2106.01477.pdf
[116] Getting started with LaTeX in 2025 – 13 beginner tips https://www.structuralbasics.com/latex-getting-started/
[117] What is the best practice on importing packages ... https://stackoverflow.com/questions/78793196/what-is-the-best-practice-on-importing-packages-for-functions-in-a-multi-file-pr
[118] LaTeX Best Practices - Parker Glynn-Adey https://pgadey.ca/notes/latex-best-practices/
[119] Basic Structure | LaTeX | Writing https://pandaqi.com/tutorials/writing/latex/basic-structure/
[120] Adding Unicode Characters to LaTeX documents https://agiletribe.wordpress.com/2015/04/07/adding-unicode-characters-to-latex-documents/
[121] Overleaf - LaTeX: Structuring and Formatting https://libguides.eur.nl/overleaf/structuring-and-formatting
[122] Why does UTF-8 encoding not work for special character in ... https://stackoverflow.com/questions/69105800/why-does-utf-8-encoding-not-work-for-special-character-in-process-input-stream
[123] LibGuides: LaTeX for Publications: Special Characters https://libguides.uiwtx.edu/c.php?g=1337391&p=10783079
[124] ICST Tool Competition 2025 - Self-Driving Car Testing Track https://ieeexplore.ieee.org/document/10989045/
[125] Interdisciplinary insights into public health challenges: A synthesis of research presented at the 2025 African Voices for Research Virtual Conference https://publichealthinafrica.org/index.php/jphia/article/view/1506
[126] Measurement properties of assessment tools for affiliate stigma in parents of children with autism: a systematic review protocol https://bmjopen.bmj.com/lookup/doi/10.1136/bmjopen-2025-111592
[127] Using wearable and nearable devices in telerehabilitation for COPD: A review of digital endpoints in home-based programs http://medrxiv.org/lookup/doi/10.1101/2025.09.02.25334970
[128] A Protocol for Systematic Review of Prognostic Models for Cardiovascular Disease Applicable to Survivors of Adolescent and Young Adult Cancer https://healthopenresearch.org/articles/7-17/v1
[129] Maintenance Service Events Prediction Modeling of Aircraft Gas Turbine Engines https://papers.phmsociety.org/index.php/phmconf/article/view/4668
[130] Prevalence of suicidal behaviours among medical students in South Asia in the 1st quarter of the 21st century: a systematic review and meta-analysis protocol https://bmjopen.bmj.com/lookup/doi/10.1136/bmjopen-2025-103698
[131] Depression among medical students in Bangladesh: a systematic review and meta-analysis protocol on prevalence and associated factors https://bmjopen.bmj.com/lookup/doi/10.1136/bmjopen-2025-102916
[132] O-162 ICMART updates: Revision of the international glossary on infertility and fertility care and of the ICMART data collection forms https://academic.oup.com/humrep/article/doi/10.1093/humrep/deaf097.162/8170743
[133] A81 Simulated PEM Adventures: Integration of Narrative and Simulation for Interactive Learning in Paediatric Emergency Medicine at International Emergency Conferences https://www.johs.org.uk/article/doi/10.54531/GJDI2090
[134] FENICE: Factuality Evaluation of summarization based on Natural language
  Inference and Claim Extraction https://arxiv.org/html/2403.02270
[135] TLDR: Text Based Last-layer Retraining for Debiasing Image Classifiers https://arxiv.org/html/2311.18291
[136] SAEBench: A Comprehensive Benchmark for Sparse Autoencoders in Language
  Model Interpretability https://arxiv.org/html/2503.09532v2
[137] DeSiRe-GS: 4D Street Gaussians for Static-Dynamic Decomposition and
  Surface Reconstruction for Urban Driving Scenes https://arxiv.org/html/2411.11921v1
[138] ICIP 2025 Paper Kit https://cmsworkshops.com/ICIP2025/papers/paper_kit.php
[139] ICCV 2025 Author Guidelines https://iccv.thecvf.com/Conferences/2025/AuthorGuidelines
[140] Learn How to Write in LaTeX for Scientific Papers - SciScribe https://www.sciscribe.dev/blog/common-latex-mistakes-and-how-to-avoid-them/
[141] PAPER SUBMISSION GUIDELINES https://conferences.miccai.org/2025/en/PAPER-SUBMISSION-GUIDELINES.html
[142] 20 Most Common Mistakes Made by New Latex Users https://shantoroy.com/latex/common-mistakes-made-by-new-latex-typesetting-users/
[143] Creating Accessible LaTeX PDFs: PDF/UA-2 Compliance in ... https://esail.tamu.edu/faculty-tutorials/accessible-latex-pdf-ua-2-overleaf-2025/
