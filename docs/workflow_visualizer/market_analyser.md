flowchart TD
    Start[Start Market Analysis] --> GenerateHighLevelQuery["Generate High-Level Query"]
    GenerateHighLevelQuery --> IdentifyMarketNiches["Identify Market Niches"]
    IdentifyMarketNiches --> LoopCheck{"More Niches to Analyze?"}

    LoopCheck -->|Yes| ProcessNiche
    LoopCheck -->|No| CompileReport["Compile Comprehensive Report"]

    subgraph ProcessNiche[Analyze Market Niches]
        GenerateSearchQuery["Generate Niche Search Query"] --> SearchMarket["Perform Market Search"]
        SearchMarket --> AnalyzeNiche["Analyze Niche Insights"]
        AnalyzeNiche --> UpdateNichesList["Update Market Niches List"]
        UpdateNichesList --> LoopCheck
    end

    CompileReport --> GenerateTrends["Generate Market Trends"]
    GenerateTrends --> VisualizeData["Visualize Market Data"]
    VisualizeData --> GenerateInsights["Generate Strategic Insights"]
    GenerateInsights --> CreateMarketReport["Create Market Analysis Report"]
    CreateMarketReport --> ReturnReport["Return Comprehensive Market Report"]

    classDef start fill:#4a90e2,stroke:#2c3e50,stroke-width:4px;
    classDef process fill:#3498db,stroke:#2c3e50,stroke-width:2px;
    classDef decision fill:#2ecc71,stroke:#2c3e50,stroke-width:2px;
    classDef end fill:#e74c3c,stroke:#2c3e50,stroke-width:4px;

    class Start start;
    class GenerateHighLevelQuery,IdentifyMarketNiches,GenerateSearchQuery,SearchMarket,AnalyzeNiche,UpdateNichesList process;
    class LoopCheck decision;
    class ReturnReport end;
