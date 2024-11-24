from typing import List, Dict, Any
from pydantic import BaseModel
from app.llm import LiteLLMKit
from app.jina import JinaReader
from app.exa import ExaAPI
from app.config import get_settings
from app.schemas.llm import ChatRequest, Message
from fastapi import APIRouter


class CustomerNiche(BaseModel):
    """Represents a specific customer niche"""

    name: str
    description: str
    search_query: str
    search_results: List[str]
    market_size: int = 0
    growth_potential: float = 0.0
    key_characteristics: List[str] = []


class CustomerDiscoveryReport(BaseModel):
    """Comprehensive customer discovery report"""

    primary_domain: str
    total_market_size: int
    niches: List[CustomerNiche]
    ideal_customer_profile: Dict[str, Any]
    market_trends: Dict[str, Any]
    investor_sentiment: Dict[str, Any]


class IdentifyMarketNiche(BaseModel):
    niches: List[str]


class CustomerDiscoverer:
    """Advanced customer discovery and market segmentation tool"""

    def __init__(
        self, domain: str, llm_model: str = "gpt-4o", temperature: float = 0.7
    ):
        """Initialize Customer Discoverer with LLM and external search APIs"""
        self.settings = get_settings()
        self.llm = LiteLLMKit(model_name=llm_model, temperature=temperature)
        self.jina = JinaReader(self.settings.JINA_API_KEY)
        self.exa = ExaAPI(self.settings.EXA_API_KEY)

        self.domain = domain
        self.niches: List[CustomerNiche] = []
        self.comprehensive_report: CustomerDiscoveryReport | None

    def generate_high_level_query(self) -> str:
        """Generate a high-level market research query"""
        prompt = f"""
        Generate a comprehensive market research query for understanding customer markets in the {self.domain} domain.
        Focus on identifying key customer segments, workflows, and market characteristics.
        """
        return self.llm.generate(
            ChatRequest(messages=[Message(role="user", content=prompt)])
        )

    def identify_market_niches(self, high_level_query: str) -> List[str]:
        """Identify potential market niches within the domain"""
        prompt = f"""
        Based on the high-level market research query: '{high_level_query}'
        Identify and list 5-10 specific market niches within the {self.domain} domain.
        For each niche, provide a brief description and potential market significance.
        """
        niches_response = self.llm.generate(
            ChatRequest(
                messages=[Message(role="user", content=prompt)],
            ),
            response_format=IdentifyMarketNiche,
        )
        niches = IdentifyMarketNiche(**niches_response).niches
        return niches

    def generate_niche_search_query(self, niche: str) -> str:
        """Generate a targeted search query for a specific niche"""
        prompt = f"""
        Create a precise internet search query to research the following market niche: '{niche}'
        in the context of the {self.domain} domain. 
        Focus on customer characteristics, market size, and key trends.
        """
        return self.llm.generate(
            ChatRequest(messages=[Message(role="user", content=prompt)])
        )

    def search_niche_market(self, niche: str, search_query: str) -> CustomerNiche:
        """Perform comprehensive market research for a specific niche"""
        # Use Exa and Jina for diverse internet search
        try:
            # exa_results = self.exa.search(search_query, num_results=10)
            search_contents = self.exa.search_and_contents(search_query)
            search_results = [
                search_contents.results[i].text
                for i in range(len(search_contents.results))
            ]
            search_results_str = " \n".join(search_results)

        except Exception as e:
            print(f"Exa search failed: {e}, falling back to Jina")
            search_results_str = self.jina.search(search_query)

        # Analyze search results
        analysis_prompt = f"""
        Analyze the search results for the niche '{niche}' in the {self.domain} domain.
        Provide insights on:
        1. Market size
        2. Growth potential
        3. Key customer characteristics
        4. Emerging trends
        """
        niche_analysis = self.llm.generate(
            ChatRequest(
                messages=[
                    Message(role="user", content=analysis_prompt),
                    Message(role="system", content=search_results_str),
                ]
            )
        )

        return CustomerNiche(
            name=niche,
            description=niche_analysis,
            search_query=search_query,
            search_results=[search_results_str],
        )

    def compile_comprehensive_report(self):
        """Compile a comprehensive customer discovery report"""
        investor_sentiment_query = f"""
        Research investor sentiment and future outlook for the {self.domain} domain.
        Include perspectives from top consulting firms like McKinsey, BCG, and Bain.
        """
        investor_insights = self.llm.generate(
            ChatRequest(
                messages=[Message(role="user", content=investor_sentiment_query)]
            )
        )

        self.comprehensive_report = CustomerDiscoveryReport(
            primary_domain=self.domain,
            total_market_size=sum(niche.market_size for niche in self.niches),
            niches=self.niches,
            investor_sentiment={"insights": investor_insights},
            ideal_customer_profile={},  # To be implemented
            market_trends={},  # To be implemented
        )

    def discover(self):
        """Execute full customer discovery workflow"""
        print(f"Initiating customer discovery for domain: {self.domain}...")
        high_level_query = self.generate_high_level_query()
        print(f"High-level query: {high_level_query}")
        niches = self.identify_market_niches(high_level_query)
        print(f"Identified niches: {niches}")

        for niche in niches[:10]:  # Limit to 10 niches
            search_query = self.generate_niche_search_query(niche)
            print(f"Search query for '{niche}': {search_query}")
            niche_details = self.search_niche_market(niche, search_query)
            print(f"Details for '{niche}': {niche_details}")
            self.niches.append(niche_details)

        print("Compiling comprehensive report...")

        self.compile_comprehensive_report()
        return self.comprehensive_report


router = APIRouter(prefix="/customer-discovery", tags=["customer_discovery"])


@router.post("/discover")
def customer_discovery_endpoint(domain: str):
    """FastAPI endpoint for customer discovery"""
    discoverer = CustomerDiscoverer(domain)
    return discoverer.discover()
