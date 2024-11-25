flowchart TD
    Start --> ExtractKeyInsights["_extract_key_insights()"]
    ExtractKeyInsights --> GenerateEvolutionStrategy["generate_product_evolution_strategy()"]
    GenerateEvolutionStrategy --> GeneratePrompt["Create Evolution Strategy Prompt"]
    GeneratePrompt --> LLMGenerateStrategy["LLM Generates Evolution Strategy"]
    LLMGenerateStrategy --> ParseStrategyResponse["Parse Response into ProductEvolutionStrategy"]
    ParseStrategyResponse --> GenerateUserAdoptionTrend["_generate_user_adoption_trend()"]
    GenerateUserAdoptionTrend --> GenerateAdoptionPrompt["Create User Adoption Trend Prompt"]
    GenerateAdoptionPrompt --> LLMGenerateAdoption["LLM Generates User Adoption Trend"]
    LLMGenerateAdoption --> ParseAdoptionResponse["Parse Response into UserAdoptionTrend"]
    ParseAdoptionResponse --> AddTrendToStrategy["Add User Adoption Trend to Evolution Strategy"]
    AddTrendToStrategy --> ReturnStrategy["Return Evolution Strategy"]

    %% Optional Visualization Path
    ReturnStrategy --> CheckUserAdoptionTrend{"User Adoption Trend Available?"}
    CheckUserAdoptionTrend -->|Yes| VisualizeAdoptionTrend["visualize_user_adoption_trend()"]
    VisualizeAdoptionTrend --> ReturnVisualization["Return Visualization Data"]
    CheckUserAdoptionTrend -->|No| End

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef optional fill:#e0f7fa,stroke:#333,stroke-width:1px;
    class VisualizeAdoptionTrend,ReturnVisualization,CheckUserAdoptionTrend optional;
