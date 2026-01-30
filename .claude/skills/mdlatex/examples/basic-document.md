---
title: "Tài liệu mẫu"
subtitle: "Ví dụ cơ bản với Mermaid và PlantUML"
author: "Fong"
date: "2026-01-26"
version: "1.0.0"
---


## Tóm tắt


Tài liệu mẫu minh họa cách sử dụng Textor để tạo PDF từ Markdown với diagram.


## Tổng quan


Textor hỗ trợ 3 loại diagram: Mermaid (nhanh), PlantUML (UML), TikZ (toán học).


## Ví dụ Mermaid


### Flowchart


```mermaid
graph LR
    A[Bắt đầu] --> B{Kiểm tra}
    B -->|Đạt| C[Xuất PDF]
    B -->|Không đạt| D[Sửa lỗi]
    D --> B
```


### Mindmap


```mermaid
mindmap
  root((Textor))
    Mermaid
      Flowchart
      Sequence
      Mindmap
    PlantUML
      Class
      Activity
      Salt
    TikZ
      Math
      Vector
```


## Ví dụ PlantUML


### Sequence Diagram


```plantuml
@startuml sequence-demo
skinparam dpi 300
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam defaultFontColor #2C3E50
skinparam shadowing false

title Quy trình xuất PDF

actor "Người dùng" as user
participant "Markdown" as md
participant "Textor" as textor
participant "PDF" as pdf

user -> md: Viết nội dung
md -> textor: export-md-to-pdf
textor -> textor: Render diagrams
textor -> pdf: Xuất file
pdf --> user: Nhận PDF

@enduml
```


## Kết luận


Textor giúp chuyển đổi Markdown thành PDF chuyên nghiệp với diagram chất lượng cao[^1].


[^1]: Textor Doc Converter v3.1.0. Script: /home/fong/Projects/textor-doc-converter/run-807f321188c6.sh.
