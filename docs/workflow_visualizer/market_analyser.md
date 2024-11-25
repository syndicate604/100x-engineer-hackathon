flowchart TD
    Start[Start Market Analysis] --> GenerateHighLevelQuery["Generate High-Level Query"]
    GenerateHighLevelQuery --> BreakdownProblem["Breakdown Problem"]
    BreakdownProblem --> PerformAnalysis["Perform Market Analysis"]
    PerformAnalysis --> GenerateSearchQueries["Generate Search Queries"]
    GenerateSearchQueries --> SearchInternet["Search Internet"]
    SearchInternet --> AnalyzeSearchResults["Analyze Search Results"]
    AnalyzeSearchResults --> CompileReports["Compile Individual Reports"]
    CompileReports --> GenerateTrendVisualization["Generate Trend Visualization"]
    GenerateTrendVisualization --> VisualizeMarketTrend["Visualize Market Trend"]
    VisualizeMarketTrend --> ComprehensiveReport["Compile Comprehensive Report"]
    ComprehensiveReport --> ReturnReport["Return Market Analysis Report"]

    classDef start fill:#4a90e2,stroke:#2c3e50,stroke-width:4px;
    classDef process fill:#3498db,stroke:#2c3e50,stroke-width:2px;
    classDef decision fill:#2ecc71,stroke:#2c3e50,stroke-width:2px;
    classDef end fill:#e74c3c,stroke:#2c3e50,stroke-width:4px;

    class Start start;
    class GenerateHighLevelQuery,BreakdownProblem,PerformAnalysis,GenerateSearchQueries,SearchInternet,AnalyzeSearchResults,CompileReports,GenerateTrendVisualization,VisualizeMarketTrend,ComprehensiveReport process;
    class ReturnReport end;
