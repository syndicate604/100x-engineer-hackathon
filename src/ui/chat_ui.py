import streamlit as st
from app.llm import LiteLLMKit
from app.schemas.llm import ChatRequest, Message


class MarketInsightsChatUI:
    """Chat interface for exploring market insights reports"""

    def __init__(self, reports):
        """Initialize chat UI with generated market reports"""
        self.reports = reports
        self.llm = LiteLLMKit(model_name="gpt-4o", temperature=0.7)
        self.chat_history = []

    def _generate_system_context(self):
        """Create a comprehensive system context from reports"""
        context = """
        You are an expert market strategy consultant analyzing the following comprehensive market insights:

        Domain: {domain}
        Problem Statement: {problem_statement}
        Solution Approach: {solution_approach}

        Customer Discovery Report:
        {customer_discovery}

        Market Analysis Report:
        {market_analysis}

        Market Expansion Strategy:
        {market_expansion}

        Product Evolution Strategy:
        {product_evolution}

        Provide insightful, strategic, and actionable responses to user queries.
        """.format(
            domain=self.reports.get("domain", "Unknown"),
            problem_statement=self.reports.get("problem_statement", ""),
            solution_approach=self.reports.get("solution_approach", ""),
            customer_discovery=str(self.reports.get("customer_discovery", "")),
            market_analysis=str(self.reports.get("market_analysis", "")),
            market_expansion=str(self.reports.get("market_expansion", "")),
            product_evolution=str(self.reports.get("product_evolution", "")),
        )
        return context

    def run(self):
        """Launch interactive chat interface"""
        st.title("💬 Market Insights Chat")
        st.markdown("Ask questions about your market insights!")

        # Initialize chat history in session state if not exists
        if "market_insights_chat_history" not in st.session_state:
            st.session_state.market_insights_chat_history = []

        # Chat input
        user_query = st.chat_input("What would you like to know about your market insights?")

        # Display chat history
        for message in st.session_state.market_insights_chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Process new user query
        if user_query:
            # Add user message to chat history
            st.session_state.market_insights_chat_history.append(
                {"role": "user", "content": user_query}
            )

            # Display user message
            with st.chat_message("user"):
                st.markdown(user_query)

            # Generate AI response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                
                # Prepare messages for LLM
                messages = [
                    Message(role="system", content=self._generate_system_context()),
                    Message(role="user", content=user_query)
                ]

                # Generate response
                full_response = self.llm.generate(
                    ChatRequest(messages=messages)
                )

                # Stream the response
                message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.market_insights_chat_history.append(
                {"role": "assistant", "content": full_response}
            )
