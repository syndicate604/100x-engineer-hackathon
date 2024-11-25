from typing import List, Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field
import matplotlib.pyplot as plt
import io
import base64

from app.routers.customer_discovery import CustomerDiscoveryReport
from app.routers.market_analysis import MarketAnalysisReport
from app.routers.market_expansion import MarketExpansionStrategy
from app.llm import LiteLLMKit
from app.schemas.llm import ChatRequest, Message
from app.schemas.visualization import TrendVisualizationResponse

router = APIRouter(prefix="/product-evolution", tags=["product_evolution"])

class ProductEvolutionPhase(BaseModel):
    """Detailed product evolution phase"""
    
    phase_number: int
    name: str
    description: str
    target_customer_segments: List[str]
    key_features: List[str]
    value_proposition: str
    expected_market_reaction: str
    success_metrics: Dict[str, Any]
    estimated_timeline: Dict[str, str]
    risk_mitigation_strategies: List[str]

class UserAdoptionTrend(BaseModel):
    """User adoption trend visualization data"""
    
    x_axis_labels: List[str]
    y_axis_labels: List[str]
    data: List[List[float]]
    x_axis_name: str
    y_axis_name: str
    reasoning: str
    key_insights: List[str]

class ProductEvolutionStrategy(BaseModel):
    """Comprehensive product evolution roadmap"""
    
    primary_domain: str
    phases: List[ProductEvolutionPhase]
    overall_vision: str
    long_term_goals: List[str]
    competitive_differentiation: Dict[str, str]
    user_adoption_trend: Optional[UserAdoptionTrend] = None

class ProductEvolver:
    """Advanced product evolution strategy generator"""
    
    def __init__(
        self, 
        customer_discovery: CustomerDiscoveryReport,
        market_analysis: MarketAnalysisReport,
        market_expansion: MarketExpansionStrategy,
        llm_model: str = "gpt-4o", 
        temperature: float = 0.7
    ):
        """Initialize Product Evolver with comprehensive market insights"""
        self.llm = LiteLLMKit(model_name=llm_model, temperature=temperature)
        
        self.customer_discovery = customer_discovery
        self.market_analysis = market_analysis
        self.market_expansion = market_expansion
        
        self.primary_domain = customer_discovery.primary_domain
        self.evolution_strategy: Optional[ProductEvolutionStrategy] = None
    
    def _extract_key_insights(self):
        """Extract most valuable and clear data points from reports"""
        # Customer Discovery Insights
        key_niches = [niche for niche in self.customer_discovery.niches[:3] if niche.market_size > 0]
        ideal_customer_profile = self.customer_discovery.ideal_customer_profile.get('insights', '')
        
        # Market Analysis Insights
        market_trends = self.market_analysis.comprehensive_report
        
        # Market Expansion Insights
        expansion_domains = self.market_expansion.expansion_domains
        strategic_rationale = self.market_expansion.strategic_rationale
        
        return {
            'key_niches': key_niches,
            'ideal_customer_profile': ideal_customer_profile,
            'market_trends': market_trends,
            'expansion_domains': expansion_domains,
            'strategic_rationale': strategic_rationale
        }
    
    def generate_product_evolution_strategy(self) -> ProductEvolutionStrategy:
        """Generate a comprehensive product evolution strategy"""
        insights = self._extract_key_insights()
        
        evolution_strategy_prompt = f"""
        Design a multi-phase product evolution strategy for the {self.primary_domain} domain.
        
        Context:
        - Key Market Niches: {insights['key_niches']}
        - Ideal Customer Profile: {insights['ideal_customer_profile']}
        - Market Trends: {insights['market_trends']}
        - Potential Expansion Domains: {insights['expansion_domains']}
        
        Strategy Requirements:
        1. Create a 3-phase product evolution roadmap
        2. Each phase should build upon the previous one
        3. Focus on incremental value addition
        4. Maintain customer engagement
        5. Prepare for future market expansion
        
        For each phase, provide:
        - Target customer segments
        - Key features
        - Value proposition
        - Expected market reaction
        - Success metrics
        - Estimated timeline
        - Risk mitigation strategies
        """
        
        messages = [
            Message(
                role="system", 
                content="You are a strategic product evolution expert. Design a roadmap that balances innovation, market needs, and customer value."
            ),
            Message(role="user", content=evolution_strategy_prompt)
        ]
        
        request = ChatRequest(messages=messages)
        evolution_strategy_response = self.llm.generate(
            request, 
            response_format=ProductEvolutionStrategy
        )
        
        self.evolution_strategy = ProductEvolutionStrategy(**evolution_strategy_response)
        
        # Generate user adoption trend visualization
        self.evolution_strategy.user_adoption_trend = self._generate_user_adoption_trend()
        
        return self.evolution_strategy

    def _generate_user_adoption_trend(self) -> UserAdoptionTrend:
        """Generate user adoption trend visualization"""
        # Simulate user adoption trend data generation
        user_adoption_query = f"""
        Generate a user adoption trend visualization for the {self.primary_domain} domain.
        
        Requirements:
        1. Create trend lines for:
           - Beta Users
           - Actual Paying Users
           - Total Users
        2. Cover product evolution phases
        3. Show realistic user growth patterns
        4. Include reasoning and key insights
        """
        
        messages = [
            Message(
                role="system", 
                content="You are an expert in user adoption trend analysis. Generate realistic, strategic user growth data."
            ),
            Message(role="user", content=user_adoption_query)
        ]
        
        request = ChatRequest(messages=messages)
        user_adoption_response = self.llm.generate(
            request, 
            response_format=UserAdoptionTrend
        )
        
        return UserAdoptionTrend(**user_adoption_response)

    def visualize_user_adoption_trend(self, trend_data: UserAdoptionTrend) -> TrendVisualizationResponse:
        """
        Visualize user adoption trend data using matplotlib

        Args:
            trend_data (UserAdoptionTrend): User adoption trend visualization data

        Returns:
            TrendVisualizationResponse: Visualization with image and insights
        """
        plt.figure(figsize=(12, 6))

        # Plot each trend line
        for i, y_label in enumerate(trend_data.y_axis_labels):
            plt.plot(
                trend_data.x_axis_labels, trend_data.data[i], label=y_label, marker="o"
            )

        plt.title(f"User Adoption Trend: {trend_data.y_axis_name}")
        plt.xlabel(trend_data.x_axis_name)
        plt.ylabel(trend_data.y_axis_name)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save plot to a base64 encoded image
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        plt.close()
        
        return {
            "img": image_base64,
            "reason": trend_data.reasoning,
            "insights": trend_data.key_insights,
        }

@router.post("/evolve")
def product_evolution_endpoint(
    customer_discovery: CustomerDiscoveryReport,
    market_analysis: MarketAnalysisReport,
    market_expansion: MarketExpansionStrategy
):
    """FastAPI endpoint for product evolution strategy generation"""
    evolver = ProductEvolver(
        customer_discovery, 
        market_analysis, 
        market_expansion
    )
    return evolver.generate_product_evolution_strategy()

@router.post("/user-adoption-trend")
def user_adoption_trend_endpoint(
    customer_discovery: CustomerDiscoveryReport,
    market_analysis: MarketAnalysisReport,
    market_expansion: MarketExpansionStrategy
):
    """FastAPI endpoint for user adoption trend visualization"""
    evolver = ProductEvolver(
        customer_discovery, 
        market_analysis, 
        market_expansion
    )
    evolution_strategy = evolver.generate_product_evolution_strategy()
    
    if evolution_strategy.user_adoption_trend:
        return evolver.visualize_user_adoption_trend(evolution_strategy.user_adoption_trend)
    
    return {"error": "User adoption trend not available"}
