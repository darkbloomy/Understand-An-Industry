---
name: extracting-job-info
description: extracting-job-info is a skill designed to extract and structure job-related information from unstructured text sources such as job descriptions, resumes, or postings. It leverages natural language processing techniques to identify key details like job titles, responsibilities, qualifications, and company information.
---

# Extract Job Information

This skill enables extraction and structuring of job-related information from various sources such as URLs, unstructured text documents, job descriptions, resumes, or online postings.

## Background

In the rapidly evolving job market, efficiently parsing specific role requirements is essential. This skill abstracts the complexity of unstructured text, converting diverse job listings into a standardized, machine-readable format. This enables downstream analysis for industry trends, salary benchmarking, and skill gap analysis.

## Workflow

1.  **Input Acquisition**: Receive input as a URL, raw text, or document file.
2.  **Content Extraction**: If a URL is provided, fetch the webpage content and clean HTML tags.
3.  **Parsing & Analysis**: Analyze the text to identify semantic sections (Title, Company, Requirements, Benefits).
4.  **Entity Extraction**: Extract specific entities like salary ranges, location, and years of experience.
5.  **Standardization**: Map extracted data to a common schema.
6.  **Output Generation**: Return the structured data in JSON or a summarized report.

## Extraction Schema

The skill targets the following key data points for extraction:

### Core Identity
-   **Job Title**: Standardized role name.
-   **Company Name**: Hiring organization.
-   **Industry**: Sector of operation (e.g., Construction, Tech).

### Logistics
-   **Location**: City, State, Country, and Remote/Hybrid status.
-   **Employment Type**: Full-time, Contract, Part-time.
-   **Salary**: Base range, bonus potential, and currency.
-   **Posting Date**: Date the job was listed.

### Role Details
-   **Summary**: A concise overview of the role's purpose.
-   **Key Responsibilities**: List of primary duties and expectations.
-   **Skills**:
    -   *Required*: Must-have technical and soft skills.
    -   *Preferred*: Nice-to-have qualifications.
-   **Tools/Technologies**: Specific software (e.g., Revit, Python) or platforms mentioned.
-   **Education/Certifications**: Degree requirements and professional licenses.

### Context
-   **Benefits**: Healthcare, PTO, 401k, etc.
-   **Company Culture**: Keywords describing the work environment.
-   **Application Link**: Direct URL to apply.