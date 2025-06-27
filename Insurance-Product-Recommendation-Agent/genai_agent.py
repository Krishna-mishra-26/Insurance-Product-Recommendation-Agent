try:
    import openai
    from dotenv import load_dotenv
    OPENAI_AVAILABLE = True
    load_dotenv()
except ImportError:
    OPENAI_AVAILABLE = False

import os
from typing import List, Dict
from fallback_agent import LocalGenAIAgent

class GenAIAgent:
    """
    GenAI-powered agent for insurance recommendations
    Uses OpenAI GPT for natural language understanding and response generation
    Falls back to rule-based logic if OpenAI is not available
    """
    
    def __init__(self):
        self.use_openai = False
        self.fallback_agent = LocalGenAIAgent()
        
        if OPENAI_AVAILABLE:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key and api_key != 'your_openai_api_key_here' and api_key.strip():
                try:
                    # Use classic OpenAI API approach (stable and reliable)
                    openai.api_key = api_key.strip()
                    self.use_openai = True
                    print("✅ OpenAI API key configured successfully")
                except Exception as e:
                    print(f"❌ OpenAI API configuration failed: {e}")
                    print("🔄 Falling back to rule-based recommendations")
                    self.use_openai = False
            else:
                print("⚠️ No valid OpenAI API key found, using fallback agent")
                self.use_openai = False
        else:
            print("⚠️ OpenAI package not available, using fallback agent")
            self.use_openai = False
        
    def enhance_query_understanding(self, user_query: str) -> Dict:
        """
        Use GenAI to better understand user intent and extract structured information
        """
        if not self.use_openai:
            return self.fallback_agent.enhance_query_understanding(user_query)
        
        system_prompt = """
        You are an expert insurance advisor. Analyze the user's query and extract structured information.
        
        Extract the following information from the user query:
        - Age (if mentioned)
        - Gender (if mentioned or implied)
        - Marital status (if mentioned)
        - Specific insurance needs (health, accident, critical illness, maternity)
        - Budget preferences (low premium, high coverage)
        - Any specific conditions or requirements
        
        Return the analysis in a structured format.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this insurance query: {user_query}"}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            return {"ai_analysis": response.choices[0].message.content}
        except Exception as e:
            print(f"⚠️ OpenAI API call failed: {e}")
            print("🔄 Using fallback analysis")
            self.use_openai = False  # Disable for future calls
            return self.fallback_agent.enhance_query_understanding(user_query)
    
    def generate_personalized_explanation(self, recommendations: List[Dict], user_query: str) -> str:
        """
        Generate a personalized explanation using GenAI or fallback logic
        """
        if not self.use_openai:
            return self.fallback_agent.generate_personalized_explanation(recommendations, user_query)
        
        if not recommendations:
            return "I couldn't find suitable insurance products for your requirements. Please try adjusting your criteria."
        
        products_summary = "\n".join([
            f"- {rec['name']}: ₹{rec['monthly_premium']}/month, Coverage: ₹{rec['coverage']:,}, "
            f"Critical Illness: {rec['critical_illness']}, Maternity: {rec['maternity']}, "
            f"Accident: {rec['accident']}, Co-pay: {rec['co_pay']}%"
            for rec in recommendations
        ])
        
        system_prompt = """
        You are a friendly and knowledgeable insurance advisor. Based on the user's query and the recommended products, 
        provide a personalized explanation in a conversational tone. 
        
        - Explain why these products were selected
        - Highlight key benefits relevant to the user
        - Provide practical advice
        - Keep it concise but informative
        - Use Indian Rupees (₹) for currency
        """
        
        user_prompt = f"""
        User Query: {user_query}
        
        Recommended Products:
        {products_summary}
        
        Please provide a personalized explanation for these recommendations.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ OpenAI API call failed: {e}")
            print("🔄 Using fallback explanation")
            self.use_openai = False  # Disable for future calls
            return self.fallback_agent.generate_personalized_explanation(recommendations, user_query)
    
    def generate_comparative_analysis(self, recommendations: List[Dict]) -> str:
        """
        Generate a comparative analysis of recommended products
        """
        if not self.use_openai:
            return self.fallback_agent.generate_comparative_analysis(recommendations)
        
        if len(recommendations) < 2:
            return ""
        
        products_data = "\n".join([
            f"{i+1}. {rec['name']}: Premium ₹{rec['monthly_premium']}, Coverage ₹{rec['coverage']:,}, Co-pay {rec['co_pay']}%"
            for i, rec in enumerate(recommendations)
        ])
        
        system_prompt = """
        You are an insurance expert. Compare the given insurance products and provide insights on:
        - Which product offers best value for money
        - Trade-offs between premium and coverage
        - Suitable scenarios for each product
        Keep it concise and practical.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Compare these insurance products:\n{products_data}"}
                ],
                temperature=0.5,
                max_tokens=300
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ OpenAI API call failed: {e}")
            print("🔄 Using fallback comparison")
            self.use_openai = False  # Disable for future calls
            return self.fallback_agent.generate_comparative_analysis(recommendations)
    
    def test_openai_connection(self) -> bool:
        """
        Test OpenAI connection when actually needed
        """
        if not self.use_openai:
            return False
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=1,
                temperature=0
            )
            return True
        except Exception as e:
            print(f"❌ OpenAI connection test failed: {e}")
            self.use_openai = False
            return False
