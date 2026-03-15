"""
AI Query Engine for Supply Chain Data Analysis
Convert natural language queries to data filters using Claude API
"""

import os
from anthropic import Anthropic
import pandas as pd
import json
from typing import Dict, Any, Optional


class SupplyChainAIEngine:
    """Claude API-powered supply chain data query engine"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI engine

        Args:
            api_key: Claude API Key (if not provided, read from environment)
        """
        self.client = Anthropic(
            api_key=api_key or os.getenv('ANTHROPIC_API_KEY')
        )
        self.model = os.getenv('ANTHROPIC_MODEL', 'claude-3-haiku-20240307')
        self.conversation_history = []
        self.query_count = 0
        self.max_queries_per_session = 100  # Prevent abuse

    def get_data_schema(self, df: pd.DataFrame) -> str:
        """Generate dataset schema description for AI understanding"""
        schema_info = {
            "total_rows": len(df),
            "columns": {},
        }

        for col in df.columns:
            col_info = {
                "type": str(df[col].dtype),
            }

            # Numeric columns
            if pd.api.types.is_numeric_dtype(df[col]):
                col_info["min"] = float(df[col].min())
                col_info["max"] = float(df[col].max())
                col_info["mean"] = float(df[col].mean())
            # Categorical columns
            else:
                unique_vals = df[col].dropna().unique()
                col_info["unique_count"] = len(unique_vals)
                col_info["sample_values"] = unique_vals[:5].tolist()

            schema_info["columns"][col] = col_info

        return json.dumps(schema_info, ensure_ascii=False, indent=2)

    def natural_language_to_sql(
        self,
        user_query: str,
        df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Convert natural language query to SQL statement

        Args:
            user_query: User's natural language query
            df: DataFrame for schema reference

        Returns:
            {
                'success': bool,
                'sql_query': str,
                'explanation': str,
                'error': str | None
            }
        """
        if self.query_count >= self.max_queries_per_session:
            return {
                'success': False,
                'sql_query': '',
                'explanation': '',
                'error': f'Session query limit reached ({self.max_queries_per_session} queries). Please refresh the app.'
            }

        schema = self.get_data_schema(df)

        system_prompt = f"""You are a supply chain data analysis expert. Convert natural language to DuckDB SQL queries.

Dataset structure:
{schema}

Table name: supply_chain

**Core Rules**:
1. Generate valid DuckDB SQL SELECT statements
2. Use double quotes for column names with spaces: "Defect rates"
3. In JSON output, ESCAPE double quotes in SQL: \"Defect rates\"
4. Use single quotes for string values: 'Supplier 1'
5. Use WHERE clauses for filtering
6. Use ORDER BY with LIMIT for top N queries
7. Always use SELECT * unless specific columns requested

**Examples with ESCAPED quotes in JSON**:

Example 1:
User: "Show products with defect rate > 3%"
Response:
{{
    "sql_query": "SELECT * FROM supply_chain WHERE \\"Defect rates\\" > 3.0",
    "explanation": "Query filters products with defect rate greater than 3%"
}}

Example 2:
User: "Top 10 most expensive items"
Response:
{{
    "sql_query": "SELECT * FROM supply_chain ORDER BY \\"Manufacturing costs\\" DESC LIMIT 10",
    "explanation": "Query returns top 10 items ordered by manufacturing cost descending"
}}

Example 3:
User: "Skincare products with cost over $50"
Response:
{{
    "sql_query": "SELECT * FROM supply_chain WHERE \\"Product type\\" = 'skincare' AND \\"Manufacturing costs\\" > 50",
    "explanation": "Query filters skincare products with manufacturing cost over $50"
}}

**CRITICAL**: Your response MUST be ONLY valid JSON in this exact format:
{{
    "sql_query": "SQL with \\"escaped quotes\\" for column names",
    "explanation": "brief explanation in English"
}}

REMEMBER: Escape double quotes in SQL column names with backslash!
No markdown, no code blocks, no explanations - ONLY the JSON object above!"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_query}
                ]
            )

            self.query_count += 1

            response_text = message.content[0].text.strip()

            # Extract JSON object
            if not response_text.startswith('{'):
                start = response_text.find('{')
                end = response_text.rfind('}')
                if start != -1 and end != -1:
                    response_text = response_text[start:end+1]
                else:
                    return {
                        'success': False,
                        'sql_query': '',
                        'explanation': '',
                        'error': 'I can help you filter and analyze the supply chain data! Try asking:\n\n• "Show products with defect rate > 3%"\n• "Top 10 most expensive items"\n• "Products with cost over $50"\n• "All skincare products"\n\nOr click one of the suggested prompts below the chat!'
                    }

            # Fix: AI sometimes doesn't escape quotes in SQL properly
            # Strategy: Extract values with regex and build result dict manually
            import re

            try:
                # First attempt: try parsing as-is
                result = json.loads(response_text)
            except json.JSONDecodeError as first_error:
                # If parsing fails, extract values manually with regex

                # Extract sql_query - match from "sql_query": " to the next ",
                # but handle quotes in between
                sql_match = re.search(r'"sql_query":\s*"(.+?)",?\s*$', response_text, re.MULTILINE | re.DOTALL)

                # More robust: find sql_query line and extract until next line with "explanation"
                lines = response_text.split('\n')
                sql_query = None
                explanation = None

                for i, line in enumerate(lines):
                    if '"sql_query"' in line:
                        # Extract everything after "sql_query": "
                        sql_start = line.find('"sql_query"')
                        after_key = line[sql_start + len('"sql_query"'):]
                        # Find the opening quote
                        quote_start = after_key.find('"', after_key.find(':'))
                        if quote_start != -1:
                            sql_part = after_key[quote_start + 1:]
                            # Find the closing quote (but not escaped ones)
                            # Simple approach: find last quote before comma or end
                            if sql_part.rstrip().endswith('",'):
                                sql_query = sql_part.rstrip()[:-2]
                            elif sql_part.rstrip().endswith('"'):
                                sql_query = sql_part.rstrip()[:-1]
                            else:
                                sql_query = sql_part

                    if '"explanation"' in line:
                        # Same process for explanation
                        exp_start = line.find('"explanation"')
                        after_key = line[exp_start + len('"explanation"'):]
                        quote_start = after_key.find('"', after_key.find(':'))
                        if quote_start != -1:
                            exp_part = after_key[quote_start + 1:]
                            if exp_part.rstrip().endswith('"'):
                                explanation = exp_part.rstrip()[:-1]
                            else:
                                explanation = exp_part

                if sql_query and explanation:
                    result = {
                        'sql_query': sql_query,
                        'explanation': explanation
                    }
                else:
                    raise first_error

            return {
                'success': True,
                'sql_query': result.get('sql_query', ''),
                'explanation': result.get('explanation', ''),
                'error': None
            }

        except json.JSONDecodeError as e:
            return {
                'success': False,
                'sql_query': '',
                'explanation': '',
                'error': 'Let me help you with data filtering! Try asking:\n\n• "Show products with defect rate > 3%"\n• "Top 10 cheapest shipping routes"\n• "Manufacturing cost over $50"\n\nYou can also click the suggested prompts below!'
            }
        except Exception as e:
            return {
                'success': False,
                'sql_query': '',
                'explanation': '',
                'error': f'API call failed: {str(e)}'
            }

    def execute_sql(self, con, sql_query: str) -> pd.DataFrame:
        """
        Execute SQL query using DuckDB connection

        Args:
            con: DuckDB/ibis connection
            sql_query: SQL query string

        Returns:
            Filtered DataFrame
        """
        if not sql_query or sql_query.strip() == '':
            return con.table('supply_chain').to_pandas()

        try:
            result = con.sql(sql_query).to_pandas()
            return result
        except Exception as e:
            # Return full table if query fails
            return con.table('supply_chain').to_pandas()

    def reset_session(self):
        """Reset session counter"""
        self.query_count = 0
        self.conversation_history = []
