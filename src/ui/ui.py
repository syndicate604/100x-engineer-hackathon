import os
import json
import tempfile
import streamlit as st
import asyncio
from datetime import datetime
import base64
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import io
import matplotlib.pyplot as plt

from app.routers.customer_discovery import CustomerDiscoverer, CustomerDiscoveryReport
from app.routers.market_analysis import MarketAnalyzer, MarketAnalysisReport
from app.routers.market_expansion import MarketExpander, MarketExpansionStrategy
from app.llm import LiteLLMKit


class MarketInsightUI:
    def __init__(self):
        st.set_page_config(
            page_title="Market Insight Generator", page_icon="🚀", layout="wide"
        )
        self.temp_dir = tempfile.mkdtemp()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pdf_report_path = os.path.join(self.temp_dir, f"{self.session_id}_market_insights.pdf")
        self.reports = None

    def _save_report_to_json(self, report, report_type):
        """Save report to a JSON file in the temp directory"""
        filename = os.path.join(
            self.temp_dir, f"{self.session_id}_{report_type}_report.json"
        )
        with open(filename, "w") as f:
            json.dump(report.model_dump(), f, indent=2)
        return filename

    def customer_onboarding(self):
        """Initial customer onboarding and problem statement collection"""
        st.title("🌟 Market Insight Generator")

        st.markdown("""
        ### Welcome to Your Market Strategy Companion
        Let's help you explore and understand your market potential.
        """)

        with st.form("problem_statement_form"):
            domain = st.text_input(
                "What domain or industry are you exploring?",
                placeholder="e.g., AI-powered healthcare solutions",
            )
            problem_statement = st.text_area(
                "Describe the problem you want to solve",
                placeholder="Provide a detailed description of your market challenge",
            )
            solution_approach = st.text_area(
                "How do you plan to approach this problem?",
                placeholder="Outline your initial strategy or approach",
            )
            submitted = st.form_submit_button("Start Market Analysis")

        return (
            domain,
            problem_statement,
            solution_approach if submitted else (None, None, None),
        )

    async def generate_market_reports(self, domain):
        """Asynchronously generate market reports"""
        st.markdown("### 🔍 Generating Market Insights")
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Customer Discovery Report
        status_text.text("Stage 1: Initiating Customer Discovery...")
        progress_bar.progress(10)
        customer_discoverer = CustomerDiscoverer(domain)

        status_text.text("Stage 2: Exploring Customer Niches...")
        progress_bar.progress(30)
        customer_discovery_report = customer_discoverer.discover()

        # Market Analysis Report
        status_text.text("Stage 3: Performing Market Analysis...")
        progress_bar.progress(50)
        market_analyzer = MarketAnalyzer()
        market_analyzer.breakdown_problem(domain)
        market_analyzer.perform_analysis()
        market_analyzer.compile_comprehensive_report()
        market_analysis_report = market_analyzer.get_report()

        # Market Expansion Strategy
        status_text.text("Stage 4: Generating Market Expansion Strategy...")
        progress_bar.progress(70)
        market_expander = MarketExpander(
            customer_discovery_report, market_analysis_report
        )
        market_expansion_strategy = market_expander.expand_market()

        status_text.text("Stage 5: Finalizing Reports...")
        progress_bar.progress(90)

        # Save reports to JSON
        customer_discovery_file = self._save_report_to_json(
            customer_discovery_report, "customer_discovery"
        )
        market_analysis_file = self._save_report_to_json(
            market_analysis_report, "market_analysis"
        )
        market_expansion_file = self._save_report_to_json(
            market_expansion_strategy, "market_expansion"
        )

        progress_bar.progress(100)
        status_text.text("Market Insights Generated Successfully!")

        return (
            customer_discovery_report,
            market_analysis_report,
            market_expansion_strategy,
        )

    def display_reports(self, reports):
        """Display generated market reports with visualizations and export options"""
        customer_discovery, market_analysis, market_expansion = reports
        self.reports = reports  # Store reports for potential PDF export

        st.title("🚀 Market Insights Dashboard")

        # Sidebar navigation
        report_options = [
            "Customer Discovery Report",
            "Market Analysis Report",
            "Market Expansion Strategy",
            "Visualizations"
        ]
        selected_report = st.sidebar.radio("Select Report", report_options)

        # Report display logic
        if selected_report == "Customer Discovery Report":
            st.subheader("Customer Discovery Insights")
            st.json(customer_discovery.model_dump())

        elif selected_report == "Market Analysis Report":
            st.subheader("Market Analysis Insights")
            st.json(market_analysis.model_dump())

        elif selected_report == "Market Expansion Strategy":
            st.subheader("Market Expansion Strategy")
            st.json(market_expansion.model_dump())

        elif selected_report == "Visualizations":
            self._display_visualizations(reports)

        # PDF Export Button
        if st.sidebar.button("Export Reports as PDF"):
            self._export_pdf()

    def _display_visualizations(self, reports):
        """Display various visualizations from reports"""
        st.title("Market Insights Visualizations")
        
        # Placeholder for visualization methods
        # You'll need to implement these methods in respective report classes
        # Example placeholders:
        st.subheader("Customer Discovery Visualization")
        # customer_discovery_viz = reports[0].generate_visualization()
        # st.pyplot(customer_discovery_viz)

        st.subheader("Market Analysis Trend")
        # market_analysis_trend = reports[1].generate_trend_visualization()
        # st.pyplot(market_analysis_trend)

        st.subheader("Market Expansion Strategy")
        # market_expansion_viz = reports[2].generate_strategy_visualization()
        # st.pyplot(market_expansion_viz)

    def _export_pdf(self):
        """Export reports to PDF and provide download link"""
        if self.reports:
            PDFReportGenerator.generate_pdf(self.reports, self.pdf_report_path)
            
            with open(self.pdf_report_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
            
            st.download_button(
                label="Download Market Insights PDF",
                data=pdf_bytes,
                file_name=f"market_insights_{self.session_id}.pdf",
                mime="application/pdf"
            )
        else:
            st.error("No reports available for PDF export")

    def run(self):
        """Main application workflow"""
        domain, problem_statement, solution_approach = self.customer_onboarding()

        if domain:
            # Display problem statement details
            st.sidebar.markdown("### Problem Statement")
            st.sidebar.write(f"**Domain:** {domain}")
            st.sidebar.write(f"**Problem:** {problem_statement}")
            st.sidebar.write(f"**Approach:** {solution_approach}")

            # Generate reports asynchronously
            reports = asyncio.run(self.generate_market_reports(domain))

            # Display reports
            self.display_reports(reports)


def main():
    ui = MarketInsightUI()
    ui.run()


if __name__ == "__main__":
    main()

# Note: You'll need to install additional dependencies
# pip install reportlab
