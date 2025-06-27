"""
Demo script to test the recommendation engine
Run this to see how the system works
"""

from recommendation_engine import InsuranceRecommendationEngine
from genai_agent import GenAIAgent

def run_demo():
    print("🛡️ Insurance Product Recommendation Agent Demo")
    print("=" * 60)
    
    # Initialize the system
    print("Initializing recommendation engine...")
    engine = InsuranceRecommendationEngine('insurance_products.csv')
    ai_agent = GenAIAgent()
    
    # Test queries showcasing expanded dataset
    test_queries = [
        "I'm 24, software developer, want comprehensive tech professional health plan with critical illness",
        "35-year-old Uber driver needs accident coverage with vehicle-specific benefits and low premium",
        "22-year-old college student looking for affordable health insurance with accident coverage",
        "Senior citizen, 68, with diabetes needs health insurance for pre-existing conditions",
        "New mother, 26, wants maternity support with newborn care and family coverage",
        "Startup founder, 32, needs executive health plan with high coverage and critical illness"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test Query {i}:")
        print(f"Query: {query}")
        print("-" * 40)
        
        # Get recommendations
        recommendations = engine.get_recommendations(query, top_n=3)
        
        if recommendations:
            # Display recommendations
            print(f"Found {len(recommendations)} recommendations:")
            
            for j, product in enumerate(recommendations, 1):
                print(f"\n{j}. {product['name']}")
                print(f"   Type: {product['type']}")
                print(f"   Premium: ₹{product['monthly_premium']}/month")
                print(f"   Coverage: ₹{product['coverage']:,}")
                print(f"   Critical Illness: {product['critical_illness']}")
                print(f"   Maternity: {product['maternity']}")
                print(f"   Accident: {product['accident']}")
                print(f"   Co-pay: {product['co_pay']}%")
                print(f"   Match Score: {product['relevance_score']:.1f}/10")
            
            # Get AI explanation
            print(f"\n🤖 AI Explanation:")
            explanation = ai_agent.generate_personalized_explanation(recommendations, query)
            print(explanation)
            
        else:
            print("No suitable products found for this query.")
        
        print("\n" + "=" * 60)
    
    print("\n✅ Demo completed!")
    print("To run the full interactive application, use: streamlit run app.py")

if __name__ == "__main__":
    run_demo()
