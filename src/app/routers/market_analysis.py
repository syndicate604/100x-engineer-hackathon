import asyncio
import matplotlib.pyplot as plt
import io
import base64
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Response

from app.llm import LiteLLMKit
from app.jina import JinaReader
from app.exa import ExaAPI
from app.schemas.llm import ChatRequest, Message
from app.config import get_settings

router = APIRouter(prefix="/market-analysis", tags=["market_analysis"])


class ProblemBreakdown(BaseModel):
    """Represents a breakdown of a complex problem into sub-problems"""

    questions: List[str] = Field(
        ..., description="List of sub-problems derived from the main query"
    )


class MarketTrendVisualization(BaseModel):
    """Detailed market trend visualization data with analytical reasoning"""

    x_axis_labels: List[str] = Field(
        ..., description="Labels for the x-axis (time period)"
    )
    y_axis_labels: List[str] = Field(..., description="Labels for the y-axis (metrics)")
    x_axis_name: str = Field(..., description="Name of the x-axis")
    y_axis_name: str = Field(..., description="Name of the y-axis")
    data: List[List[float]] = Field(
        ..., description="Data points for the trend visualization"
    )
    reasoning: str = Field(
        ..., description="Detailed explanation and insights behind the trend data"
    )
    key_insights: List[str] = Field(
        ..., description="Key strategic insights derived from the trend analysis"
    )


class MarketAnalysisReport(BaseModel):
    """Comprehensive market analysis report"""

    original_query: str
    problem_breakdown: ProblemBreakdown
    search_results: Dict[str, Dict[str, Any]]
    comprehensive_report: str


class MarketAnalyzer:
    def __init__(self, llm_model: str = "gpt-4o", temperature: float = 0.7):
        """Initialize Market Analyzer with LLM and external search APIs"""
        self.llm = LiteLLMKit(model_name=llm_model, temperature=temperature)
        self.jina = JinaReader(get_settings().JINA_API_KEY)
        self.exa = ExaAPI(get_settings().EXA_API_KEY)

        self.original_query: str = ""
        self.questions: List[str] = []
        self.search_results: Dict[str, Dict[str, Any]] = {}
        self.reports: Dict[str, str] = {}
        self.comprehensive_report: str = ""

    def breakdown_problem(self, query: str) -> ProblemBreakdown:
        """Break down the original query into multiple sub-problems"""
        messages = [
            Message(
                role="system",
                content="""
            You are an expert problem decomposition assistant. 
            Break down complex queries into 5 distinct, focused sub-problems.
            Ensure each sub-problem is specific, actionable, and provides a different perspective.
            """,
            ),
            Message(
                role="user",
                content=f"Break down this query into detailed sub-problems: {query}",
            ),
        ]

        request = ChatRequest(messages=messages)
        breakdown = self.llm.generate(request, response_format=ProblemBreakdown)

        breakdown = ProblemBreakdown(**breakdown)

        self.original_query = query
        self.questions = breakdown.questions
        return breakdown

    def generate_search_query(self, question: str) -> str:
        """Generate an optimized search query for each sub-problem"""
        messages = [
            Message(
                role="system",
                content="""
            You are an expert search query generator. 
            Create precise, targeted search queries that will yield comprehensive information.
            Focus on extracting actionable insights.
            """,
            ),
            Message(
                role="user", content=f"Generate a search query to research: {question}"
            ),
        ]

        request = ChatRequest(messages=messages)
        return self.llm.generate(request)

    def search_internet(self, search_query: str, fallback: bool = True) -> List[str]:
        """Search internet with fallback mechanism"""
        try:
            # Try Exa first
            exa_results = self.exa.search(search_query)
            return [result.text for result in exa_results.results]
        except Exception as e:
            if fallback:
                try:
                    # Fallback to Jina
                    return [self.jina.search(search_query)]
                except Exception:
                    return []
            return []

    def analyze_search_results(self, question: str, search_results: List[str]) -> str:
        """Analyze search results and generate a concise report"""
        messages = [
            Message(
                role="system",
                content="""
            You are an expert research analyst. 
            Synthesize the provided search results into a clear, concise report.
            Focus on key insights, trends, and actionable information.
            """,
            ),
            Message(
                role="user",
                content=f"Question: {question}\nSearch Results: {search_results}",
            ),
        ]

        request = ChatRequest(messages=messages)
        return self.llm.generate(request)

    def search_market_for_year(self, year: int, question: str) -> Dict[str, Any]:
        """Perform targeted market search for a specific year and question"""
        market_year_query = f"""
        Analyze the market for {question} in the year {year} with focus on:
        1. Market size and economic indicators
        2. Technological innovations
        3. Key market disruptions
        4. Regulatory landscape
        5. Investment and funding trends
        6. Competitive dynamics
        """

        # Perform search using multiple sources
        try:
            search_contents = self.exa.search_and_contents(market_year_query)
            search_results = [
                search_contents.results[i].text
                for i in range(len(search_contents.results))
            ]
            search_results_str = " \n".join(search_results)
        except Exception as e:
            print(f"Exa search failed for {year}: {e}, falling back to Jina")
            search_results_str = self.jina.search(market_year_query)

        # Analyze and structure the search results
        analysis_prompt = f"""
        Comprehensively analyze the search results for the market question '{question}' in {year}.
        Provide a structured analysis covering:
        - Market size and growth
        - Key technological developments
        - Major market events
        - Investment trends
        - Competitive landscape shifts
        """

        year_analysis = self.llm.generate(
            ChatRequest(
                messages=[
                    Message(role="user", content=analysis_prompt),
                    Message(role="system", content=search_results_str),
                ]
            )
        )

        return {
            "year": year,
            "question": question,
            "analysis": year_analysis,
            "raw_search_results": search_results,
        }

    def perform_analysis(self):
        """Perform comprehensive market analysis with targeted approach"""
        years = list(range(2019, 2025))  # Expanded year range

        # Year-by-year analysis for the original query (first question)
        if self.questions:
            original_query_insights = [
                self.search_market_for_year(year, self.original_query) for year in years
            ]

            print(f"Yearly insights for original query: {original_query_insights}")

            self.search_results[self.original_query] = {
                "yearly_insights": original_query_insights
            }

            # Compile comprehensive report for original query
            original_query_analysis = [
                insight["analysis"] for insight in original_query_insights
            ]

            original_query_report = self.llm.generate(
                ChatRequest(
                    messages=[
                        Message(
                            role="user",
                            content=f"""
                        Synthesize the year-by-year market insights for the original query: '{self.original_query}'.
                        Create a comprehensive analysis that:
                        1. Identifies overarching trends
                        2. Highlights key inflection points
                        3. Provides predictive insights
                        4. Suggests strategic recommendations
                        """,
                        ),
                        Message(role="system", content=str(original_query_analysis)),
                    ]
                )
            )

            self.reports[self.original_query] = original_query_report

        # Standard internet research for remaining questions
        remaining_questions = self.questions[0:5]  # Limit to prevent excessive AI calls
        for question in remaining_questions:
            # Generate search query
            search_query = self.generate_search_query(question)

            # Perform internet search
            search_results = self.search_internet(search_query)

            # Analyze search results
            question_analysis = self.analyze_search_results(question, search_results)

            # Store results
            self.search_results[question] = {
                "search_query": search_query,
                "search_results": search_results,
            }
            self.reports[question] = question_analysis

            print(f"Processed question: {question}")

    async def generate_trend_visualization(self) -> MarketTrendVisualization:
        """Generate comprehensive trend visualization and analysis using async processing"""
        years = list(range(2019, 2025))

        async def analyze_year_trend(year: int) -> Dict[str, Any]:
            """Async function to analyze trend for a specific year"""
            trend_query = f"""
            Analyze market trends for the year {year} focusing on:
            1. Key performance indicators
            2. Growth metrics
            3. Technological advancements
            4. Market sentiment
            5. Predictive insights
            """

            messages = [
                Message(
                    role="system",
                    content="You are an expert trend analyst. Provide concise, data-driven insights.",
                ),
                Message(role="user", content=trend_query),
            ]

            request = ChatRequest(messages=messages)
            return {"year": year, "trend_analysis": await self.llm.agenerate(request)}

        # Use asyncio to process year trends concurrently
        year_trends = await asyncio.gather(
            *[analyze_year_trend(year) for year in years]
        )

        # Generate comprehensive trend visualization
        trend_visualization_query = f"""
        Based on these yearly trend analyses: {year_trends}
        Create a comprehensive trend visualization with the following requirements:

        Data Generation Guidelines:
        1. Generate 3-5 distinct trend lines representing different market metrics
        2. Ensure data points are floating-point numbers between 0 and 100
        3. Create consistent, plausible year-over-year progression
        4. Include metrics like:
           - Market Growth Rate
           - Innovation Index
           - Investment Sentiment
           - Technology Adoption
           - Competitive Intensity

        Visualization Requirements:
        1. Provide precise numerical data for each metric from 2019-2025
        2. Ensure data tells a coherent market evolution story
        3. Include realistic fluctuations and trend patterns
        4. Generate data that shows both linear and non-linear trends

        Analytical Requirements:
        1. Explain the reasoning behind each trend line
        2. Highlight key inflection points and market shifts
        3. Provide strategic implications of the observed trends
        4. Discuss potential future scenarios based on the data

        Output Format:
        - Structured, machine-readable numerical data
        - Comprehensive textual reasoning
        - Strategic insights and recommendations
        """

        messages = [
            Message(
                role="system",
                content="You are an advanced data visualization expert. Generate structured trend data with numerical values.",
            ),
            Message(role="user", content=trend_visualization_query),
        ]

        request = ChatRequest(messages=messages)
        trend_data = self.llm.generate(
            request, response_format=MarketTrendVisualization
        )

        trend_visualization = MarketTrendVisualization(**trend_data)

        return trend_visualization

    def visualize_trend(
        self, trend_data: MarketTrendVisualization
    ) -> dict[str, str | list[str]]:
        """
        Visualize market trend data using matplotlib

        Args:
            trend_data (MarketTrendVisualization): Trend visualization data
            output_format (str, optional): Output format. Defaults to 'base64'.

        Returns:
            Optional[str]: Visualization in specified format
        """
        plt.figure(figsize=(12, 6))

        # Plot each trend line
        for i, y_label in enumerate(trend_data.y_axis_labels):
            plt.plot(
                trend_data.x_axis_labels, trend_data.data[i], label=y_label, marker="o"
            )

        plt.title(f"Market Trend Analysis: {trend_data.y_axis_name}")
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

    def compile_comprehensive_report(self):
        """Compile individual reports into a comprehensive market analysis"""
        messages = [
            Message(
                role="system",
                content="""
            You are a master report compiler. 
            Synthesize individual research reports into a comprehensive, cohesive document.
            Highlight interconnections, overarching themes, and strategic insights.
            """,
            ),
            Message(
                role="user",
                content=f"Original Query: {self.original_query}\nIndividual Reports: {self.reports}",
            ),
        ]

        request = ChatRequest(messages=messages)
        self.comprehensive_report = self.llm.generate(request)

        return self.comprehensive_report

    def get_report(self) -> MarketAnalysisReport:
        """Retrieve the complete market analysis report"""
        return MarketAnalysisReport(
            original_query=self.original_query,
            problem_breakdown=ProblemBreakdown(questions=self.questions),
            search_results=self.search_results,
            comprehensive_report=self.comprehensive_report,
        )


@router.post("/analyze")
async def market_analysis(query: str):
    """Endpoint for market analysis"""
    analyzer = MarketAnalyzer()
    analyzer.breakdown_problem(query)
    analyzer.perform_analysis()
    analyzer.compile_comprehensive_report()

    return analyzer.get_report()


@router.post("/visualize-trend")
async def visualize_market_trend(query: str):
    """Endpoint for market trend visualization"""
    analyzer = MarketAnalyzer()
    analyzer.breakdown_problem(query)
    trend_data = await analyzer.generate_trend_visualization()

    visualization = analyzer.visualize_trend(trend_data)

    return visualization
