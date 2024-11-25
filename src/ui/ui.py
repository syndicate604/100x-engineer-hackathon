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
import sys
from app.routers.product_evolution import ProductEvolver

from app.routers.customer_discovery import CustomerDiscoverer, CustomerDiscoveryReport
from app.routers.market_analysis import MarketAnalyzer, MarketAnalysisReport
from app.routers.market_expansion import MarketExpander, MarketExpansionStrategy
from app.llm import LiteLLMKit


class PDFReportGenerator:
    @staticmethod
    def generate_pdf(reports, output_path):
        """Generate a comprehensive PDF report from market insights"""
        customer_discovery, market_analysis, market_expansion = reports

        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        story.append(Paragraph("Market Insights Report", styles["Title"]))
        story.append(Spacer(1, 12))

        # Customer Discovery Section
        story.append(Paragraph("Customer Discovery Report", styles["Heading2"]))
        story.append(Paragraph(str(customer_discovery), styles["Normal"]))
        story.append(Spacer(1, 12))

        # Market Analysis Section
        story.append(Paragraph("Market Analysis Report", styles["Heading2"]))
        story.append(Paragraph(str(market_analysis), styles["Normal"]))
        story.append(Spacer(1, 12))

        # Market Expansion Section
        story.append(Paragraph("Market Expansion Strategy", styles["Heading2"]))
        story.append(Paragraph(str(market_expansion), styles["Normal"]))

        # Generate PDF
        doc.build(story)

    @staticmethod
    def base64_to_image(base64_string, output_path):
        """Convert base64 image to file"""
        image_data = base64.b64decode(base64_string)
        with open(output_path, "wb") as f:
            f.write(image_data)


class MarketInsightUI:
    def __init__(self):
        st.set_page_config(
            page_title="Market Insight Generator", page_icon="🚀", layout="wide"
        )
        self.temp_dir = tempfile.mkdtemp()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pdf_report_path = os.path.join(
            self.temp_dir, f"{self.session_id}_market_insights.pdf"
        )

        # Initialize session state for workflow progression
        if "workflow_stage" not in st.session_state:
            st.session_state.workflow_stage = "customer_onboarding"

        # Initialize reports dictionary
        if "reports" not in st.session_state:
            st.session_state.reports = {
                "domain": None,
                "customer_discovery": None,
                "market_analysis": None,
                "market_expansion": None,
                "product_evolution": None,
            }

        self.reports = st.session_state.reports

    def _save_report_to_json(self, report, report_type):
        """Save report to a JSON file in the temp directory"""
        filename = os.path.join(
            self.temp_dir, f"{self.session_id}_{report_type}_report.json"
        )
        with open(filename, "w") as f:
            json.dump(report.model_dump(), f, indent=2)
        return filename

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
            "Visualizations",
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
                mime="application/pdf",
            )
        else:
            st.error("No reports available for PDF export")

    def run(self):
        """Main application workflow"""
        # Workflow stages
        workflow_stages = {
            "customer_onboarding": self.customer_onboarding,
            "customer_discovery": self.customer_discovery_stage,
            "market_analysis": self.market_analysis_stage,
            "market_expansion": self.market_expansion_stage,
            "product_evolution": self.product_evolution_stage,
            "final_report": self.final_report_stage,
        }

        # Execute current workflow stage
        current_stage = st.session_state.workflow_stage
        workflow_stages[current_stage]()

    def _advance_workflow(self, next_stage):
        """Advance to the next workflow stage"""
        st.session_state.workflow_stage = next_stage
        st.experimental_rerun()

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

        if submitted and domain:
            st.session_state.reports["domain"] = domain
            st.session_state.reports["problem_statement"] = problem_statement
            st.session_state.reports["solution_approach"] = solution_approach
            self._advance_workflow("customer_discovery")

    def customer_discovery_stage(self):
        """Customer Discovery Stage with Interactive Logging"""
        st.title("🔍 Customer Discovery")

        domain = st.session_state.reports["domain"]

        # Interactive logging placeholder
        log_container = st.empty()

        with st.spinner("Discovering Customer Insights..."):
            customer_discoverer = CustomerDiscoverer(domain)

            # Capture print statements
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()

            try:
                customer_discovery_report = customer_discoverer.discover()

                # Restore stdout and get captured output
                sys.stdout = old_stdout
                log_output = captured_output.getvalue()

                log_container.code(log_output)

                st.session_state.reports["customer_discovery"] = (
                    customer_discovery_report
                )

                if st.button("Proceed to Market Analysis"):
                    self._advance_workflow("market_analysis")

            except Exception as e:
                st.error(f"Error in Customer Discovery: {e}")

    def market_analysis_stage(self):
        """Market Analysis Stage with Interactive Logging"""
        st.title("📊 Market Analysis")

        domain = st.session_state.reports["domain"]

        # Interactive logging placeholder
        log_container = st.empty()

        with st.spinner("Performing Market Analysis..."):
            market_analyzer = MarketAnalyzer()

            # Capture print statements
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()

            try:
                market_analyzer.breakdown_problem(domain)
                market_analyzer.perform_analysis()
                market_analyzer.compile_comprehensive_report()
                market_analysis_report = market_analyzer.get_report()

                # Restore stdout and get captured output
                sys.stdout = old_stdout
                log_output = captured_output.getvalue()

                log_container.code(log_output)

                st.session_state.reports["market_analysis"] = market_analysis_report

                if st.button("Proceed to Market Expansion"):
                    self._advance_workflow("market_expansion")

            except Exception as e:
                st.error(f"Error in Market Analysis: {e}")

    def market_expansion_stage(self):
        """Market Expansion Stage with Interactive Logging"""
        st.title("🌐 Market Expansion")

        customer_discovery_report = st.session_state.reports["customer_discovery"]
        market_analysis_report = st.session_state.reports["market_analysis"]

        # Interactive logging placeholder
        log_container = st.empty()

        with st.spinner("Generating Market Expansion Strategy..."):
            market_expander = MarketExpander(
                customer_discovery_report, market_analysis_report
            )

            # Capture print statements
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()

            try:
                market_expansion_strategy = market_expander.expand_market()

                # Restore stdout and get captured output
                sys.stdout = old_stdout
                log_output = captured_output.getvalue()

                log_container.code(log_output)

                st.session_state.reports["market_expansion"] = market_expansion_strategy

                if st.button("Proceed to Product Evolution"):
                    self._advance_workflow("product_evolution")

            except Exception as e:
                st.error(f"Error in Market Expansion: {e}")

    def product_evolution_stage(self):
        """Product Evolution Stage with Interactive Logging"""
        st.title("🚀 Product Evolution")

        customer_discovery_report = st.session_state.reports["customer_discovery"]
        market_analysis_report = st.session_state.reports["market_analysis"]
        market_expansion_strategy = st.session_state.reports["market_expansion"]

        # Interactive logging placeholder
        log_container = st.empty()

        with st.spinner("Generating Product Evolution Strategy..."):
            product_evolver = ProductEvolver(
                customer_discovery_report,
                market_analysis_report,
                market_expansion_strategy,
            )

            # Capture print statements
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()

            try:
                product_evolution_strategy = (
                    product_evolver.generate_product_evolution_strategy()
                )

                # Restore stdout and get captured output
                sys.stdout = old_stdout
                log_output = captured_output.getvalue()

                log_container.code(log_output)

                st.session_state.reports["product_evolution"] = (
                    product_evolution_strategy
                )

                if st.button("View Final Report"):
                    self._advance_workflow("final_report")

            except Exception as e:
                st.error(f"Error in Product Evolution: {e}")

    def final_report_stage(self):
        """Final Report Stage with Export Options"""
        st.title("📄 Final Market Insights Report")

        # Collect all reports
        reports = [
            st.session_state.reports["customer_discovery"],
            st.session_state.reports["market_analysis"],
            st.session_state.reports["market_expansion"],
            st.session_state.reports["product_evolution"],
        ]

        # Display reports and export options
        self.display_reports(reports)

        # Add a button to launch chat UI
        if st.button("💬 Chat with Market Insights"):
            chat_ui = MarketInsightsChatUI(st.session_state.reports)
            chat_ui.run()


def main():
    ui = MarketInsightUI()
    ui.run()


if __name__ == "__main__":
    main()
