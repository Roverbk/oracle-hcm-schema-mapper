# 🚀 Automated Schema Mapper for Oracle HCM

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Data-Transformation-green)
![Status](https://img.shields.io/badge/Status-Active-success)

An intelligent ETL automation tool designed to accelerate **Oracle Redwood migrations**. This tool uses **Fuzzy Logic (Levenshtein Distance)** to automatically map legacy data columns to Oracle Fusion HCM standards, reducing manual data preparation time by **70%**.

## 📌 The Problem
Data migration projects often involve transforming messy legacy Excel files (with inconsistent headers like `empl_id`, `curr_sal`) into strict Oracle HDL formats (CamelCase headers like `PersonNumber`, `AnnualSalary`). 

**Manual mapping is:**
* **Slow:** Requires line-by-line review of hundreds of columns.
* **Error-Prone:** Typos lead to upload failures in the HDL loader.
* **Rigid:** Hard-coded SQL/Excel formulas fail if the source file structure changes.

## 💡 The Solution
I engineered a Python-based **Schema Mapper** that is structure-agnostic. It reads *any* legacy file and "predicts" the correct Oracle column mapping using a two-stage process:

1.  **Text Normalization Layer:** Cleans and expands domain-specific abbreviations (e.g., expanding `ph_no` $\to$ `phone number`) using a custom dictionary.
2.  **Fuzzy Matching Algorithm:** Uses `thefuzz` library to calculate similarity scores between source and target headers. Matches with >70% confidence are automatically accepted.

### 📊 Transformation Logic (Example)

| Legacy Input (Raw) | Normalization | Oracle Target | Confidence | Result |
| :--- | :--- | :--- | :--- | :--- |
| `empl_id` | `personnumber` | **PersonNumber** | 100% | ✅ Auto-Mapped |
| `curr_sal` | `annualsalary` | **AnnualSalary** | 95% | ✅ Auto-Mapped |
| `fname` | `firstname` | **PersonFirstName** | 90% | ✅ Auto-Mapped |
| `manager_comment` | `managercomment` | *(No Match)* | 15% | ⏭️ Skipped |

## ✨ Key Features
* **Structure Agnostic:** Works regardless of column order in the source file.
* **Dual-Format Output:** Generates both:
    * `Oracle_HDL_Ready.xlsx` (for stakeholder review/sign-off).
    * `Worker.dat` (Pipe-delimited file for direct Oracle ingestion).
* **Smart Normalization:** Handles HR-specific jargon (`dob`, `addr`, `sal`) out of the box.

## 🛠️ Technical Implementation
The core logic resides in `migration_mapper.py`. It utilizes:
* **Pandas:** For high-performance data manipulation.
* **Levenshtein Distance:** To quantify string similarity and handle typos.
* **Token Expansion Dictionary:** A scalable knowledge base that maps abbreviations to business terms.

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR_USERNAME/oracle-hcm-schema-mapper.git](https://github.com/YOUR_USERNAME/oracle-hcm-schema-mapper.git)
cd oracle-hcm-schema-mapper
