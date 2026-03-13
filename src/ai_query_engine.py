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

    def natural_language_to_filter(
        self,
        user_query: str,
        df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Convert natural language query to pandas filter condition

        Args:
            user_query: User's natural language query
            df: DataFrame to filter

        Returns:
            {
                'success': bool,
                'filter_code': str,  # pandas filter code
                'explanation': str,  # AI explanation
                'error': str | None
            }
        """
        if self.query_count >= self.max_queries_per_session:
            return {
                'success': False,
                'filter_code': '',
                'explanation': '',
                'error': f'Session query limit reached ({self.max_queries_per_session} queries). Please refresh the app.'
            }

        schema = self.get_data_schema(df)

        system_prompt = f"""You are a supply chain data analysis expert. Users will query data in natural language, and you need to convert it to Python pandas DataFrame filter code.

Dataset structure:
{schema}

**Core Rules**:
1. Only return valid pandas boolean indexing expressions that return FULL ROWS (DataFrame), not single columns
2. Use df[condition] syntax for filtering, conditions can be combined with & | ~
3. String comparisons use == or .str.contains()
4. Numeric comparisons use > < >= <= ==
5. ALWAYS return complete DataFrame rows, never just single columns like df['SKU']
6. If the query is unclear or cannot be converted, return empty string and explain why in the explanation field

**Examples**:
- User: "Show products with defect rate > 3%"
  → "df['Defect rates'] > 3.0"

- User: "Supplier 2 haircare products"
  → "(df['Supplier name'] == 'Supplier 2') & (df['Product type'] == 'haircare')"

- User: "Top 10 records by shipping cost"
  → "df.nlargest(10, 'Shipping costs')"

- User: "Most expensive item"
  → "df.nlargest(1, 'Manufacturing costs')"

Output format (pure JSON only):
{{
    "filter_code": "pandas code expression",
    "explanation": "brief explanation in English"
}}

**Do NOT** output anything other than JSON!"""

        try:
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",  # Use Haiku (fast and cheap)
                max_tokens=800,
                temperature=0.3,  # Lower randomness, higher consistency
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_query}
                ]
            )

            self.query_count += 1

            # Parse AI response
            response_text = message.content[0].text.strip()

            # Try extracting JSON (AI sometimes includes extra text)
            if not response_text.startswith('{'):
                # Find first { and last }
                start = response_text.find('{')
                end = response_text.rfind('}')
                if start != -1 and end != -1:
                    response_text = response_text[start:end+1]
                else:
                    # No JSON found in response - user likely asked a general question
                    return {
                        'success': False,
                        'filter_code': '',
                        'explanation': '',
                        'error': 'I can help you filter and analyze the supply chain data! Try asking:\n\n• "Show products with defect rate > 3%"\n• "Top 10 most expensive items"\n• "Products with cost over $50"\n• "All skincare products"\n\nOr click one of the suggested prompts below the chat!'
                    }

            result = json.loads(response_text)

            return {
                'success': True,
                'filter_code': result.get('filter_code', ''),
                'explanation': result.get('explanation', ''),
                'error': None
            }

        except json.JSONDecodeError as e:
            return {
                'success': False,
                'filter_code': '',
                'explanation': '',
                'error': 'Let me help you with data filtering! Try asking:\n\n• "Show products with defect rate > 3%"\n• "Top 10 cheapest shipping routes"\n• "Manufacturing cost over $50"\n\nYou can also click the suggested prompts below!'
            }
        except Exception as e:
            return {
                'success': False,
                'filter_code': '',
                'explanation': '',
                'error': f'API call failed: {str(e)}'
            }

    def apply_filter(self, df: pd.DataFrame, filter_code: str) -> pd.DataFrame:
        """
        Safely execute filter code

        Args:
            df: Original data
            filter_code: AI-generated filter code

        Returns:
            Filtered DataFrame
        """
        if not filter_code or filter_code.strip() == '':
            return df

        try:
            # Safe execution: only allow df variable and pandas operations
            namespace = {'df': df.copy(), 'pd': pd}

            # Check for method calls like nlargest
            if 'nlargest' in filter_code or 'nsmallest' in filter_code:
                filtered_df = eval(filter_code, {"__builtins__": {}}, namespace)
            else:
                # Regular boolean indexing
                filtered_df = eval(f"df[{filter_code}]", {"__builtins__": {}}, namespace)

            # Ensure result is always a DataFrame
            if isinstance(filtered_df, pd.Series):
                filtered_df = filtered_df.to_frame()
            elif not isinstance(filtered_df, pd.DataFrame):
                # If it's a scalar or other type, return original df
                print(f"⚠️ Filter returned non-DataFrame type: {type(filtered_df)}")
                return df

            return filtered_df

        except Exception as e:
            print(f"⚠️ Filter execution error: {e}")
            print(f"Attempted code: {filter_code}")
            return df  # Return original data on error

    def reset_session(self):
        """Reset session counter"""
        self.query_count = 0
        self.conversation_history = []
