import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import re

class InsuranceRecommendationEngine:
    """
    Goal-based AI agent for insurance product recommendations
    Uses rule-based logic combined with scoring algorithms
    """
    
    def __init__(self, csv_path: str):
        self.products_df = pd.read_csv(csv_path)
        self.user_profile = {}
        
    def parse_user_query(self, query: str) -> Dict:
        """
        Extract key information from user natural language query
        """
        query_lower = query.lower()
        
        # Extract age
        age_match = re.search(r'\b(\d{1,2})\b', query)
        age = int(age_match.group(1)) if age_match else None
        
        # Extract gender/marital status
        gender = None
        marital_status = None
        if any(word in query_lower for word in ['female', 'woman', 'girl']):
            gender = 'female'
        elif any(word in query_lower for word in ['male', 'man', 'boy']):
            gender = 'male'
            
        if any(word in query_lower for word in ['married', 'wife', 'husband']):
            marital_status = 'married'
        elif any(word in query_lower for word in ['unmarried', 'single']):
            marital_status = 'single'
        
        # Extract coverage preferences
        wants_health = any(word in query_lower for word in ['health', 'medical', 'hospital'])
        wants_accident = any(word in query_lower for word in ['accident', 'injury'])
        wants_critical = any(word in query_lower for word in ['critical', 'cancer', 'heart', 'stroke'])
        wants_maternity = any(word in query_lower for word in ['maternity', 'pregnancy', 'childbirth'])
        
        # Extract profession-specific needs
        profession_keywords = {
            'student': ['student', 'college', 'university', 'intern'],
            'tech': ['software', 'developer', 'engineer', 'tech', 'it', 'programmer', 'data scientist'],
            'finance': ['banker', 'financial', 'investment', 'stock broker', 'insurance agent'],
            'medical': ['doctor', 'nurse', 'medical professional', 'healthcare'],
            'transport': ['driver', 'taxi', 'uber', 'ola', 'delivery', 'truck driver'],
            'defense': ['army', 'navy', 'airforce', 'military', 'soldier', 'police'],
            'sports': ['athlete', 'sports', 'player', 'fitness'],
            'senior': ['senior citizen', 'retired', 'elderly', 'old age']
        }
        
        detected_profession = None
        for profession, keywords in profession_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_profession = profession
                break
        
        # Extract specific life situations
        life_situation = None
        if any(word in query_lower for word in ['single mother', 'single father', 'divorced', 'widow']):
            life_situation = 'single_parent'
        elif any(word in query_lower for word in ['family', 'spouse', 'children']):
            life_situation = 'family'
        elif any(word in query_lower for word in ['diabetes', 'hypertension', 'heart disease', 'kidney']):
            life_situation = 'pre_existing'
        
        # Extract premium preferences
        wants_low_premium = any(word in query_lower for word in ['low premium', 'cheap', 'affordable', 'budget'])
        wants_high_coverage = any(word in query_lower for word in ['high coverage', 'maximum coverage', 'comprehensive'])
        
        return {
            'age': age,
            'gender': gender,
            'marital_status': marital_status,
            'wants_health': wants_health,
            'wants_accident': wants_accident,
            'wants_critical': wants_critical,
            'wants_maternity': wants_maternity,
            'wants_low_premium': wants_low_premium,
            'wants_high_coverage': wants_high_coverage,
            'profession': detected_profession,
            'life_situation': life_situation,
            'original_query': query
        }
    
    def filter_by_age(self, age: int) -> pd.DataFrame:
        """Filter products based on age eligibility"""
        if age is None:
            return self.products_df
        return self.products_df[
            (self.products_df['age_min'] <= age) & 
            (self.products_df['age_max'] >= age)
        ]
    
    def calculate_relevance_score(self, product: pd.Series, user_prefs: Dict) -> float:
        """
        Enhanced relevance score calculation with profession and situation matching
        """
        score = 0.0
        product_name_lower = product['name'].lower()
        
        # Coverage type matching (base scoring)
        if user_prefs.get('wants_health') and product['type'] == 'Health':
            score += 3.0
        if user_prefs.get('wants_accident') and product['accident'] == 'Yes':
            score += 2.0
        if user_prefs.get('wants_critical') and product['critical_illness'] == 'Yes':
            score += 2.0
        if user_prefs.get('wants_maternity') and product['maternity'] == 'Yes':
            score += 2.0
        
        # Profession-specific matching (NEW)
        profession = user_prefs.get('profession')
        if profession:
            profession_matches = {
                'student': ['student', 'college', 'teen', 'youth', 'graduate'],
                'tech': ['tech', 'software', 'data', 'cyber', 'cloud', 'devops', 'startup'],
                'finance': ['bank', 'financial', 'investment', 'stock', 'insurance', 'corporate'],
                'medical': ['doctor', 'medical'],
                'transport': ['driver', 'taxi', 'uber', 'delivery', 'truck', 'bike'],
                'defense': ['army', 'navy', 'airforce', 'military', 'soldier', 'police', 'defense'],
                'sports': ['sports', 'athlete'],
                'senior': ['senior', 'retirement', 'elder']
            }
            
            if profession in profession_matches:
                for keyword in profession_matches[profession]:
                    if keyword in product_name_lower:
                        score += 4.0  # High bonus for profession match
                        break
        
        # Life situation matching (NEW)
        life_situation = user_prefs.get('life_situation')
        if life_situation:
            situation_matches = {
                'single_parent': ['single', 'mother', 'father', 'divorcee', 'widow'],
                'family': ['family', 'multi'],
                'pre_existing': ['diabetes', 'hypertension', 'heart', 'kidney', 'cancer']
            }
            
            if life_situation in situation_matches:
                for keyword in situation_matches[life_situation]:
                    if keyword in product_name_lower:
                        score += 3.5  # High bonus for situation match
                        break
        
        # Age-specific product matching (NEW)
        age = user_prefs.get('age')
        if age:
            age_keywords = []
            if age <= 19:
                age_keywords = ['teen', 'youth', 'student']
            elif age <= 30:
                age_keywords = ['young', 'career', 'graduate', 'newjobee']
            elif age <= 50:
                age_keywords = ['professional', 'executive', 'middle']
            elif age >= 60:
                age_keywords = ['senior', 'retirement', 'elder']
            
            for keyword in age_keywords:
                if keyword in product_name_lower:
                    score += 2.5
                    break
        
        # Premium preferences
        if user_prefs.get('wants_low_premium'):
            # Normalize premium score (lower premium = higher score)
            max_premium = self.products_df['monthly_premium'].max()
            premium_score = (max_premium - product['monthly_premium']) / max_premium
            score += premium_score * 2.0
        
        # Coverage amount preferences
        if user_prefs.get('wants_high_coverage'):
            # Normalize coverage score (higher coverage = higher score)
            max_coverage = self.products_df['coverage'].max()
            coverage_score = product['coverage'] / max_coverage
            score += coverage_score * 1.5
        
        # Co-pay penalty (lower co-pay is better)
        max_copay = self.products_df['co_pay'].max()
        copay_score = (max_copay - product['co_pay']) / max_copay
        score += copay_score * 0.5
        
        return score
    
    def get_recommendations(self, query: str, top_n: int = 3) -> List[Dict]:
        """
        Main recommendation function
        """
        # Parse user query
        user_prefs = self.parse_user_query(query)
        
        # Filter by age
        eligible_products = self.filter_by_age(user_prefs.get('age'))
        
        if eligible_products.empty:
            return []
        
        # Calculate scores
        eligible_products = eligible_products.copy()
        eligible_products['relevance_score'] = eligible_products.apply(
            lambda row: self.calculate_relevance_score(row, user_prefs), axis=1
        )
        
        # Sort by score and return top N
        top_products = eligible_products.nlargest(top_n, 'relevance_score')
        
        recommendations = []
        for _, product in top_products.iterrows():
            recommendations.append({
                'id': product['id'],
                'name': product['name'],
                'type': product['type'],
                'coverage': product['coverage'],
                'monthly_premium': product['monthly_premium'],
                'critical_illness': product['critical_illness'],
                'maternity': product['maternity'],
                'accident': product['accident'],
                'co_pay': product['co_pay'],
                'relevance_score': product['relevance_score'],
                'age_range': f"{product['age_min']}-{product['age_max']}"
            })
        
        return recommendations
    
    def explain_recommendation(self, product: Dict, user_prefs: Dict) -> str:
        """
        Generate explanation for why this product was recommended
        """
        reasons = []
        
        # Coverage type matching
        if user_prefs.get('wants_health') and product['type'] == 'Health':
            reasons.append("🏥 Perfectly matches your health insurance requirement")
        
        if user_prefs.get('wants_accident') and product['accident'] == 'Yes':
            reasons.append("🚨 Provides comprehensive accident coverage as requested")
        
        if user_prefs.get('wants_critical') and product['critical_illness'] == 'Yes':
            reasons.append("❤️ Includes critical illness protection for serious conditions")
        
        if user_prefs.get('wants_maternity') and product['maternity'] == 'Yes':
            reasons.append("👶 Offers maternity benefits for family planning")
        
        # Budget considerations
        if user_prefs.get('wants_low_premium'):
            if product['monthly_premium'] <= 1000:
                reasons.append("💰 Very affordable premium that fits your budget")
            elif product['monthly_premium'] <= 1500:
                reasons.append("💵 Reasonably priced with good value for money")
        
        # Coverage amount considerations
        if user_prefs.get('wants_high_coverage'):
            if product['coverage'] >= 2000000:
                reasons.append("🛡️ Excellent high coverage amount for comprehensive protection")
            elif product['coverage'] >= 1000000:
                reasons.append("📈 Good coverage amount for substantial protection")
        
        # Co-pay benefits
        if product['co_pay'] <= 10:
            reasons.append("💳 Very low co-pay means minimal out-of-pocket expenses")
        elif product['co_pay'] <= 20:
            reasons.append("💸 Reasonable co-pay percentage for cost sharing")
        
        # Age-specific benefits
        age = user_prefs.get('age')
        if age:
            if age <= 25 and product['monthly_premium'] <= 700:
                reasons.append("🎓 Great option for young adults with student-friendly pricing")
            elif age >= 50 and product['critical_illness'] == 'Yes':
                reasons.append("👴 Excellent choice for seniors with critical illness coverage")
            elif 25 <= age <= 40 and product['maternity'] == 'Yes':
                reasons.append("👨‍👩‍👧‍👦 Perfect for young families with maternity benefits")
        
        # Special product features
        if product['name'].lower().find('family') != -1:
            reasons.append("👪 Specially designed for family coverage needs")
        elif product['name'].lower().find('senior') != -1:
            reasons.append("👵 Tailored specifically for senior citizen requirements")
        elif product['name'].lower().find('student') != -1:
            reasons.append("📚 Designed specifically for students and young professionals")
        
        # Value proposition
        value_ratio = product['coverage'] / product['monthly_premium']
        if value_ratio > 2500:
            reasons.append("⭐ Outstanding value - maximum coverage for every rupee spent")
        elif value_ratio > 2000:
            reasons.append("👍 Excellent value proposition with great coverage-to-premium ratio")
        elif value_ratio > 1500:
            reasons.append("✅ Good balance between premium cost and coverage benefits")
        
        return ". ".join(reasons) if reasons else "Suitable option based on your profile and requirements"
