flowchart TD
    Start --> GenerateHighLevelQuery["generate_high_level_query()"]
    GenerateHighLevelQuery --> IdentifyMarketNiches["identify_market_niches(high_level_query)"]
    IdentifyMarketNiches --> ListNiches["List of Identified Niches"]
    ListNiches --> LoopCheck{"More Niches to Process?"}

    LoopCheck -->|Yes| ProcessNiche
    LoopCheck -->|No| CompileComprehensiveReport["compile_comprehensive_report()"]

    subgraph ProcessNiche[Process Each Niche (up to 10)]
        GenerateNicheSearchQuery["generate_niche_search_query(niche)"] --> SearchNicheMarket["search_niche_market(niche, search_query)"]
        SearchNicheMarket --> CollectNicheDetails["Collect Niche Details"]
        CollectNicheDetails --> AddToNichesList["Add Niche to Niches List"]
        AddToNichesList --> LoopCheck
    end

    CompileComprehensiveReport --> GenerateInvestorSentiment["Generate Investor Sentiment"]
    GenerateInvestorSentiment --> GenerateIdealCustomerProfile["Generate Ideal Customer Profile"]
    GenerateIdealCustomerProfile --> CreateReport["Create CustomerDiscoveryReport"]
    CreateReport --> ReturnReport["Return Comprehensive Report"]

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
