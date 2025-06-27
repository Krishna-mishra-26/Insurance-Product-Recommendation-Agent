"""
Alternative GenAI Agent implementation using free/local models
This file provides alternatives when OpenAI API is not available
"""

import re
from typing import List, Dict

class LocalGenAIAgent:
    """
    Alternative GenAI agent using free APIs or local models
    """
    
    def __init__(self):
        # You can configure different free APIs here
        self.fallback_mode = True
        
    def enhance_query_understanding(self, user_query: str) -> Dict:
        """
        Rule-based query understanding as fallback
        """
        query_lower = user_query.lower()
        
        analysis = []
        
        # Age detection
        age_match = re.search(r'\b(\d{1,2})\b', user_query)
        if age_match:
            analysis.append(f"Detected age: {age_match.group(1)} years")
        
        # Gender detection
        if any(word in query_lower for word in ['female', 'woman', 'girl']):
            analysis.append("Gender: Female")
        elif any(word in query_lower for word in ['male', 'man', 'boy']):
            analysis.append("Gender: Male")
        
        # Marital status
        if any(word in query_lower for word in ['married', 'wife', 'husband']):
            analysis.append("Marital Status: Married")
        elif any(word in query_lower for word in ['unmarried', 'single']):
            analysis.append("Marital Status: Single")
        
        # Insurance needs
        needs = []
        if any(word in query_lower for word in ['health', 'medical']):
            needs.append("Health Insurance")
        if any(word in query_lower for word in ['accident', 'injury']):
            needs.append("Accident Coverage")
        if any(word in query_lower for word in ['critical', 'cancer', 'heart']):
            needs.append("Critical Illness")
        if any(word in query_lower for word in ['maternity', 'pregnancy']):
            needs.append("Maternity Benefits")
        
        if needs:
            analysis.append(f"Insurance Needs: {', '.join(needs)}")
        
        # Budget preferences
        if any(word in query_lower for word in ['low premium', 'cheap', 'affordable']):
            analysis.append("Budget Preference: Low Premium")
        if any(word in query_lower for word in ['high coverage', 'comprehensive']):
            analysis.append("Coverage Preference: High Coverage")
        
        return {
            "ai_analysis": "\n".join(analysis) if analysis else "Basic analysis of insurance requirements"
        }
    
    def generate_personalized_explanation(self, recommendations: List[Dict], user_query: str) -> str:
        """
        Generate explanations using rule-based logic
        """
        if not recommendations:
            return "I couldn't find suitable insurance products for your requirements. Please try adjusting your criteria."
        
        explanation_parts = []
        
        # Opening
        explanation_parts.append(f"Based on your requirements, I've found {len(recommendations)} suitable insurance products for you.")
        
        # Analyze user query for key needs
        query_lower = user_query.lower()
        
        if any(word in query_lower for word in ['low premium', 'affordable', 'cheap']):
            explanation_parts.append("I've prioritized products with competitive premium rates to match your budget preferences.")
        
        if any(word in query_lower for word in ['critical', 'cancer']):
            critical_products = [r for r in recommendations if r['critical_illness'] == 'Yes']
            if critical_products:
                explanation_parts.append(f"{len(critical_products)} of the recommended products include critical illness coverage as requested.")
        
        if any(word in query_lower for word in ['maternity', 'pregnancy']):
            maternity_products = [r for r in recommendations if r['maternity'] == 'Yes']
            if maternity_products:
                explanation_parts.append(f"{len(maternity_products)} products include maternity benefits for your family planning needs.")
        
        # Premium range
        premiums = [r['monthly_premium'] for r in recommendations]
        min_premium, max_premium = min(premiums), max(premiums)
        explanation_parts.append(f"The recommended plans range from ₹{min_premium} to ₹{max_premium} per month.")
        
        # Coverage range
        coverages = [r['coverage'] for r in recommendations]
        min_coverage, max_coverage = min(coverages), max(coverages)
        explanation_parts.append(f"Coverage amounts range from ₹{min_coverage:,} to ₹{max_coverage:,}.")
        
        # Best value recommendation
        if len(recommendations) > 1:
            best_value = min(recommendations, key=lambda x: x['monthly_premium'] / x['coverage'])
            explanation_parts.append(f"'{best_value['name']}' offers the best value for money in terms of coverage per rupee spent.")
        
        return " ".join(explanation_parts)
    
    def generate_comparative_analysis(self, recommendations: List[Dict]) -> str:
        """
        Generate comparison analysis using rule-based logic
        """
        if len(recommendations) < 2:
            return ""
        
        analysis_parts = []
        
        # Premium analysis
        premiums = [(r['name'], r['monthly_premium']) for r in recommendations]
        premiums.sort(key=lambda x: x[1])
        
        cheapest = premiums[0]
        most_expensive = premiums[-1]
        
        analysis_parts.append(f"**Premium Comparison:** '{cheapest[0]}' has the lowest premium at ₹{cheapest[1]}/month, while '{most_expensive[0]}' is the highest at ₹{most_expensive[1]}/month.")
        
        # Coverage analysis
        coverages = [(r['name'], r['coverage']) for r in recommendations]
        coverages.sort(key=lambda x: x[1], reverse=True)
        
        highest_coverage = coverages[0]
        lowest_coverage = coverages[-1]
        
        analysis_parts.append(f"**Coverage Comparison:** '{highest_coverage[0]}' offers the highest coverage at ₹{highest_coverage[1]:,}, while '{lowest_coverage[0]}' provides ₹{lowest_coverage[1]:,}.")
        
        # Value for money
        value_scores = [(r['name'], r['coverage'] / r['monthly_premium']) for r in recommendations]
        value_scores.sort(key=lambda x: x[1], reverse=True)
        
        best_value = value_scores[0]
        analysis_parts.append(f"**Best Value:** '{best_value[0]}' offers the best value with {best_value[1]:.0f} rupees of coverage per rupee of premium.")
        
        # Co-pay analysis
        copays = [(r['name'], r['co_pay']) for r in recommendations]
        copays.sort(key=lambda x: x[1])
        
        lowest_copay = copays[0]
        analysis_parts.append(f"**Co-pay:** '{lowest_copay[0]}' has the lowest co-pay at {lowest_copay[1]}%.")
        
        return "\n\n".join(analysis_parts)

# Function to use when OpenAI is not available
def get_fallback_agent():
    """
    Returns a fallback agent when OpenAI is not available
    """
    return LocalGenAIAgent()
