# Market Analyzer Workflow Diagram

> Visualizes the comprehensive process of market analysis using advanced AI techniques

## Overview
This Mermaid.js diagram illustrates the step-by-step workflow of the MarketAnalyzer class, 
demonstrating how complex market research is conducted through intelligent decomposition, 
search, analysis, and visualization.

## Key Processes
- Problem Breakdown
- Search Query Generation
- Internet Research
- Trend Visualization
- Strategic Reporting

```mermaid
graph TD
    A[Start Market Analysis] --> B{Breakdown Problem}
    B --> |Generate Sub-Problems| C[Problem Breakdown]
    
    C --> D[Generate Search Queries]
    D --> E{Perform Internet Search}
    E --> |Exa Search| F[Retrieve Exa Results]
    E --> |Jina Fallback| G[Retrieve Jina Results]
    
    F --> H[Analyze Search Results]
    G --> H
    
    H --> I[Year-by-Year Market Analysis]
    I --> J[Generate Trend Visualization]
    
    J --> K[Visualize Trend Data]
    K --> L[Create Market Trend Chart]
    
    H --> M[Compile Comprehensive Report]
    M --> N[Generate Strategic Insights]
    
    N --> O[Final Market Analysis Report]
    
    style A fill:#f9f,stroke:#333,stroke-width:4px
    style O fill:#bbf,stroke:#333,stroke-width:4px
    style J fill:#bfb,stroke:#333,stroke-width:2px
```
