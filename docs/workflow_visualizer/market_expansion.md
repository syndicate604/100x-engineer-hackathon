flowchart TD
    Start --> InitiateExpansion["expand_market()"]
    InitiateExpansion --> GenerateExpansionDomains["generate_expansion_domains()"]
    GenerateExpansionDomains --> ListExpansionDomains["List of Potential Expansion Domains"]
    ListExpansionDomains --> AnalyzeExpansionDomains["analyze_expansion_domains(expansion_domains)"]
    AnalyzeExpansionDomains --> LoopCheck{"More Domains to Analyze?"}

    LoopCheck -->|Yes| ProcessDomain
    LoopCheck -->|No| CompileExpansionStrategy["Compile MarketExpansionStrategy"]
    
    subgraph ProcessDomain[Process Each Expansion Domain]
        PerformSearch["Perform Targeted Search and Analysis"] --> GeneratePrompt["Generate Expansion Analysis Prompt"]
        GeneratePrompt --> LLMGenerate["LLM Generates Domain Analysis"]
        LLMGenerate --> ParseAnalysis["Parse and Structure Analysis"]
        ParseAnalysis --> CollectDomainDetails["Collect Domain Details"]
        CollectDomainDetails --> AddToStrategy["Add Details to Expansion Strategy"]
        AddToStrategy --> LoopCheck
    end

    CompileExpansionStrategy --> ReturnStrategy["Return Expansion Strategy"]
    
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
