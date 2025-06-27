import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from recommendation_engine import InsuranceRecommendationEngine
from genai_agent import GenAIAgent
import os
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Insurance Product Recommendation Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Dark Theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Dark Theme Variables */
    :root {
        --bg-primary: #0a0a0a;
        --bg-secondary: #1a1a1a;
        --bg-tertiary: #2a2a2a;
        --accent-primary: #3b82f6;
        --accent-secondary: #8b5cf6;
        --text-primary: #ffffff;
        --text-secondary: #a1a1aa;
        --border-color: #374151;
        --shadow-primary: rgba(0, 0, 0, 0.5);
        --glow-blue: rgba(59, 130, 246, 0.5);
        --glow-purple: rgba(139, 92, 246, 0.5);
    }
    
    /* Main App Styling */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
        color: var(--text-primary);
    }
    
    /* Animated Cyber Grid Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            linear-gradient(90deg, transparent 98%, rgba(59, 130, 246, 0.03) 100%),
            linear-gradient(0deg, transparent 98%, rgba(139, 92, 246, 0.03) 100%);
        background-size: 100px 100px;
        animation: gridMove 20s linear infinite;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(100px, 100px); }
    }
    
    /* Glowing Particles */
    .particle {
        position: absolute;
        width: 2px;
        height: 2px;
        background: var(--accent-primary);
        border-radius: 50%;
        box-shadow: 0 0 10px var(--glow-blue);
        animation: particleFloat 25s infinite linear;
        opacity: 0.6;
    }
    
    @keyframes particleFloat {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% { opacity: 0.6; }
        90% { opacity: 0.6; }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    .main-header {
        font-size: 4.5rem;
        text-align: center;
        margin: 4rem 0;
        font-weight: 900;
        letter-spacing: 3px;
        animation: neonGlow 3s ease-in-out infinite;
        font-family: 'JetBrains Mono', monospace;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        text-transform: uppercase;
        position: relative;
        z-index: 10;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -20px;
        left: -20px;
        right: -20px;
        bottom: -20px;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
        border-radius: 30px;
        z-index: -1;
        animation: pulseGlow 4s ease-in-out infinite;
    }
    
    @keyframes pulseGlow {
        0%, 100% { 
            transform: scale(1);
            opacity: 0.5;
        }
        50% { 
            transform: scale(1.05);
            opacity: 0.8;
        }
    }
    
    @keyframes neonGlow {
        0%, 100% { 
            filter: drop-shadow(0 0 15px var(--glow-blue)) drop-shadow(0 0 30px var(--glow-blue));
            transform: scale(1);
        }
        50% { 
            filter: drop-shadow(0 0 25px var(--glow-purple)) drop-shadow(0 0 50px var(--glow-purple));
            transform: scale(1.02);
        }
    }
    
    @keyframes gradientShift {
        0% { 
            background-position: 0% 50%;
            transform: scale(1);
        }
        25% { 
            background-position: 100% 50%;
            transform: scale(1.01);
        }
        50% { 
            background-position: 200% 50%;
            transform: scale(1.02);
        }
        75% { 
            background-position: 300% 50%;
            transform: scale(1.01);
        }
        100% { 
            background-position: 400% 50%;
            transform: scale(1);
        }
    }
    
    .sub-header {
        font-size: 2rem;
        color: var(--text-primary);
        margin-bottom: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        padding: 25px 30px;
        border-radius: 15px;
        border: 1px solid var(--border-color);
        box-shadow: 
            0 8px 32px var(--shadow-primary),
            inset 0 1px 0 rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .sub-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
        animation: scanLine 3s infinite;
    }
    
    @keyframes scanLine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Special styling for Find Your Perfect Insurance Match header */
    .perfect-match-header {
        background-size: 200%;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Dark Product Cards */
    .product-card {
        background: linear-gradient(145deg, var(--bg-secondary), var(--bg-tertiary));
        border-radius: 20px;
        border: 1px solid var(--border-color);
        margin-bottom: 3rem;
        box-shadow: 
            0 20px 40px var(--shadow-primary),
            inset 0 1px 0 rgba(255,255,255,0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        overflow: hidden;
    }
    
    .product-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary), #06b6d4);
        background-size: 200% 100%;
        animation: borderGlow 4s ease-in-out infinite;
    }
    
    @keyframes borderGlow {
        0%, 100% { background-position: 0% 0%; }
        50% { background-position: 200% 0%; }
    }
    
    .product-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 30px 60px var(--shadow-primary),
            0 0 30px var(--glow-blue);
        border-color: var(--accent-primary);
    }
    
    .product-title {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(45deg, var(--text-primary), var(--accent-primary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.8rem;
        letter-spacing: 1px;
    }
    
    .product-type {
        font-size: 1rem;
        color: var(--text-secondary);
        margin-bottom: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
        position: relative;
    }
    
    .product-separator {
        height: 2px;
        background: linear-gradient(90deg, var(--accent-primary), transparent);
        margin: 2rem 0;
        border-radius: 1px;
        animation: separatorGlow 2s ease-in-out infinite;
    }
    
    @keyframes separatorGlow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .why-recommended {
        background: linear-gradient(135deg, var(--bg-tertiary), #1f2937);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid var(--accent-primary);
        margin: 20px 0;
        font-weight: 600;
        color: var(--text-primary);
        box-shadow: 0 8px 25px var(--shadow-primary);
        position: relative;
    }
    
    /* Dark Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, var(--bg-tertiary), #1f2937);
        color: var(--text-primary);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 15px 0;
        border: 1px solid var(--border-color);
        box-shadow: 
            0 10px 30px var(--shadow-primary),
            inset 0 1px 0 rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 20px 40px var(--shadow-primary),
            0 0 20px var(--glow-blue);
        border-color: var(--accent-primary);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-bottom: 8px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 1.4rem;
        font-weight: 800;
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Dark Score Badge */
    .recommendation-score {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 25px;
        font-weight: 800;
        font-size: 1rem;
        display: inline-block;
        box-shadow: 0 8px 25px var(--glow-blue);
        text-transform: uppercase;
        letter-spacing: 1px;
        animation: scoreGlow 3s ease-in-out infinite;
        font-family: 'JetBrains Mono', monospace;
    }
    
    @keyframes scoreGlow {
        0%, 100% { box-shadow: 0 8px 25px var(--glow-blue); }
        50% { box-shadow: 0 8px 25px var(--glow-purple); }
    }
    
    /* Dark Coverage Badges */
    .coverage-badge {
        display: inline-block;
        padding: 10px 16px;
        margin: 6px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .coverage-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px var(--shadow-primary);
    }
    
    .badge-critical {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white;
        border-color: #dc2626;
    }
    
    .badge-maternity {
        background: linear-gradient(135deg, #ec4899, #be185d);
        color: white;
        border-color: #ec4899;
    }
    
    .badge-accident {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        border-color: #f59e0b;
    }
    
    /* Sample Queries Box */
    .sample-queries-box {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 8px 25px var(--shadow-primary);
    }
    
    /* COMPREHENSIVE SAMPLE QUERY BUTTON FIXES */
    /* Target all possible button selectors for sample queries */
    .sample-queries-box button,
    .sample-queries-box .stButton button,
    .sample-queries-box .stButton > button,
    .sample-queries-box div[data-testid="column"] button,
    .sample-queries-box div[data-testid="column"] .stButton button,
    .sample-queries-box div[data-testid="column"] .stButton > button,
    div[data-testid="column"] .stButton > button {
        /* Force complete override of Streamlit styles */
        all: unset !important;
        
        /* Rebuild button styling from scratch */
        background: linear-gradient(135deg, var(--bg-tertiary), #1f2937) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        
        /* Container properties */
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        
        /* Text handling - CRITICAL */
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        word-break: break-word !important;
        hyphens: auto !important;
        text-overflow: clip !important;
        overflow: visible !important;
        text-align: left !important;
        
        /* Spacing and sizing */
        padding: 12px 15px !important;
        margin: 8px 0 !important;
        line-height: 1.4 !important;
        min-height: auto !important;
        height: auto !important;
        max-height: none !important;
        
        /* Visual effects */
        box-shadow: 0 4px 15px var(--shadow-primary) !important;
        
        /* Force text to wrap */
        -webkit-line-clamp: unset !important;
        -webkit-box-orient: unset !important;
        text-decoration: none !important;
        outline: none !important;
    }
    
    /* Hover states for all sample query buttons */
    .sample-queries-box button:hover,
    .sample-queries-box .stButton button:hover,
    .sample-queries-box .stButton > button:hover,
    .sample-queries-box div[data-testid="column"] button:hover,
    .sample-queries-box div[data-testid="column"] .stButton button:hover,
    .sample-queries-box div[data-testid="column"] .stButton > button:hover,
    div[data-testid="column"] .stButton > button:hover {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
        border-color: var(--accent-primary) !important;
        transform: translateX(3px) !important;
        color: white !important;
        box-shadow: 0 6px 20px var(--glow-blue) !important;
    }
    
    /* Additional specific targeting for stubborn buttons */
    .sample-queries-box * button {
        white-space: normal !important;
        word-break: break-word !important;
        overflow-wrap: break-word !important;
        text-overflow: clip !important;
        overflow: visible !important;
        height: auto !important;
        max-height: none !important;
        min-height: auto !important;
    }
    
    /* Dark Theme Input Styling */
    .stTextArea textarea {
        background: var(--bg-secondary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        font-size: 1.1rem !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px var(--shadow-primary) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 
            0 0 0 2px var(--glow-blue),
            0 12px 30px var(--shadow-primary) !important;
        outline: none !important;
    }
    
    .stTextArea textarea::placeholder {
        color: var(--text-secondary) !important;
    }
    
    /* Dark Theme Button Styling */
    .stButton button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px var(--glow-blue) !important;
        font-family: 'JetBrains Mono', monospace !important;
        white-space: wrap !important;
        min-height: 48px !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px var(--glow-purple) !important;
        background: linear-gradient(135deg, var(--accent-secondary), var(--accent-primary)) !important;
    }
    
    /* Override for sample query buttons - make them wrap text properly */
    div[data-testid="column"]:nth-child(1) .stButton button,
    div[data-testid="column"]:nth-child(2) .stButton button {
        background: linear-gradient(135deg, var(--bg-tertiary), #1f2937) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        padding: 15px 18px !important;
        border-radius: 10px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        text-transform: none !important;
        letter-spacing: 0px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        line-height: 1.4 !important;
        min-height: 55px !important;
        height: auto !important;
        display: flex !important;
        align-items: flex-start !important;
        justify-content: flex-start !important;
        text-align: left !important;
        word-break: break-word !important;
        hyphens: auto !important;
        box-shadow: 0 4px 15px var(--shadow-primary) !important;
        font-family: 'Inter', sans-serif !important;
        padding-top: 12px !important;
    }
    
    div[data-testid="column"]:nth-child(1) .stButton button:hover,
    div[data-testid="column"]:nth-child(2) .stButton button:hover {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
        border-color: var(--accent-primary) !important;
        transform: translateX(5px) !important;
        color: white !important;
        box-shadow: 0 6px 20px var(--glow-blue) !important;
    }
    
    /* Dark Sidebar Styling */
    .css-1d391kg {
        background: var(--bg-secondary) !important;
        border-right: 2px solid var(--border-color) !important;
    }
    
    /* Dark Analysis Boxes */
    .ai-analysis {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        padding: 25px;
        border-radius: 15px;
        border-left: 4px solid var(--accent-primary);
        margin: 25px 0;
        color: var(--text-primary);
        box-shadow: 0 10px 30px var(--shadow-primary);
    }
    
    .explanation-box {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        padding: 25px;
        border-radius: 15px;
        border-left: 4px solid var(--accent-secondary);
        margin: 25px 0;
        font-size: 1.1rem;
        line-height: 1.6;
        color: var(--text-primary);
        box-shadow: 0 10px 30px var(--shadow-primary);
    }
    
    /* Success/Error Messages - Dark Theme */
    .success-message {
        background: linear-gradient(135deg, #059669, #047857);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(5, 150, 105, 0.3);
        font-weight: 600;
        border-left: 4px solid #10b981;
    }
    
    .error-message {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(220, 38, 38, 0.3);
        font-weight: 600;
        border-left: 4px solid #ef4444;
    }
    
    /* Dark Loading Animation */
    .magic-loader {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 10px 30px var(--shadow-primary);
    }
    
    .magic-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        animation: magicDots 1.4s infinite ease-in-out;
    }
    
    .magic-dot:nth-child(1) { 
        background: var(--accent-primary); 
        animation-delay: -0.32s; 
    }
    .magic-dot:nth-child(2) { 
        background: var(--accent-secondary); 
        animation-delay: -0.16s; 
    }
    .magic-dot:nth-child(3) { 
        background: #06b6d4; 
        animation-delay: 0s; 
    }
    
    @keyframes magicDots {
        0%, 80%, 100% { 
            transform: scale(0.8);
            opacity: 0.5;
        }
        40% { 
            transform: scale(1.2);
            opacity: 1;
        }
    }
    
    /* Dark Chart Container */
    .chart-container {
        background: var(--bg-secondary);
        border-radius: 15px;
        margin: 2rem 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 10px 30px var(--shadow-primary);
    }
    
    /* Dark Footer */
    .footer {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        color: var(--text-primary);
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-top: 50px;
        border: 1px solid var(--border-color);
        box-shadow: 0 10px 30px var(--shadow-primary);
    }
    
    /* Sidebar Info Box */
    .sidebar-info-box {
        background: linear-gradient(135deg, var(--bg-tertiary), #1f2937);
        padding: 25px 20px 20px 20px;
        border-radius: 15px;
        margin: 25px 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 8px 25px var(--shadow-primary);
        position: relative;
        overflow: hidden;
    }
    
    .sidebar-info-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
        background-size: 200% 100%;
        animation: borderGlow 3s ease-in-out infinite;
    }
    
    .info-item {
        display: flex;
        align-items: center;
        margin: 12px 0;
        padding: 10px;
        background: rgba(59, 130, 246, 0.1);
        border-radius: 8px;
        border-left: 3px solid var(--accent-primary);
    }
    
    .info-icon {
        margin-right: 12px;
        font-size: 1.2rem;
    }
    
    .info-text {
        color: var(--text-primary);
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* Responsive Design for Dark Theme */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.8rem;
            letter-spacing: 1px;
            gap: 0.5rem;
            margin: 2rem 0;
        }
        
        .main-header span:first-child {
            font-size: 3.5rem !important;
        }
        
        .main-header span:last-child {
            font-size: 2.8rem !important;
            letter-spacing: 2px !important;
        }
        
        .product-card {
            padding: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
    }
    
    /* Scrollbar Styling for Dark Theme */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent-primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-secondary);
    }
    
    /* Advanced Micro-interactions */
    .stButton button:active {
        transform: translateY(-1px) scale(0.98) !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Enhanced Focus States for Accessibility */
    .stTextArea textarea:focus,
    .stSelectbox > div > div:focus,
    .stButton button:focus {
        outline: 3px solid rgba(102, 126, 234, 0.5) !important;
        outline-offset: 2px !important;
    }
    
    /* Improved Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        line-height: 1.3 !important;
    }
    
    /* Enhanced Tooltips */
    [title]:hover::after {
        content: attr(title);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0,0,0,0.9);
        color: white;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 0.9rem;
        white-space: nowrap;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Accessibility improvements */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* High contrast mode support */
    @media (prefers-contrast: high) {
        .product-card {
            border: 3px solid #000 !important;
        }
        
        .coverage-badge {
            border: 2px solid #000 !important;
        }
    }
    
    /* Print styles */
    @media print {
        .floating-element,
        .particle,
        .stButton,
        .sidebar {
            display: none !important;
        }
        
        .product-card {
            break-inside: avoid;
            background: white !important;
            border: 2px solid #000 !important;
        }
    }
</style>""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load insurance products data"""
    return pd.read_csv('insurance_products.csv')

@st.cache_resource
def initialize_engines():
    """Initialize recommendation engine and GenAI agent"""
    engine = InsuranceRecommendationEngine('insurance_products.csv')
    ai_agent = GenAIAgent()
    return engine, ai_agent

def format_currency(amount):
    """Format currency in Indian style"""
    if amount >= 10000000:  # 1 crore
        return f"₹{amount/10000000:.1f} Cr"
    elif amount >= 100000:  # 1 lakh
        return f"₹{amount/100000:.1f} L"
    else:
        return f"₹{amount:,}"

def display_product_card(product, explanation="", ai_analysis=""):
    """Display a product recommendation card with enhanced styling"""
    with st.container():
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        
        # Product Header
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f'<div class="product-title">{product["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="product-type">{product["type"]} Insurance</div>', unsafe_allow_html=True)
        
        with col2:
            score = product.get('relevance_score', 0)
            score_percentage = min(100, int((score / 10) * 100))
            st.markdown(f'''
                <div class="recommendation-score">
                    🎯 {score_percentage}% Match
                </div>
            ''', unsafe_allow_html=True)
        
        # Why Recommended Section
        if explanation:
            st.markdown(f'''
                <div class="why-recommended">
                    <strong>💡 Why Recommended:</strong><br>
                    {explanation}
                </div>
            ''', unsafe_allow_html=True)
        
        # Main Details
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">💰 Monthly Premium</div>
                    <div class="metric-value">₹{product['monthly_premium']:,}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">🛡️ Coverage Amount</div>
                    <div class="metric-value">{format_currency(product['coverage'])}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">💳 Co-pay</div>
                    <div class="metric-value">{product['co_pay']}%</div>
                </div>
            ''', unsafe_allow_html=True)
        
        # Coverage Badges
        st.markdown("#### 🏷️ Coverage Benefits")
        badges_html = ""
        
        if product['critical_illness'] == 'Yes':
            badges_html += '<span class="coverage-badge badge-critical">🔴 Critical Illness</span>'
        
        if product['maternity'] == 'Yes':
            badges_html += '<span class="coverage-badge badge-maternity">👶 Maternity Care</span>'
        
        if product['accident'] == 'Yes':
            badges_html += '<span class="coverage-badge badge-accident">🚨 Accident Coverage</span>'
        
        if not badges_html:
            badges_html = '<span class="coverage-badge" style="background: #ddd; color: #666;">Basic Coverage Only</span>'
        
        st.markdown(badges_html, unsafe_allow_html=True)
        
        # Additional Info
        st.markdown(f"**📅 Age Eligibility:** {product.get('age_range', 'N/A')}")
        
        # Value Indicator
        value_ratio = product['coverage'] / product['monthly_premium']
        if value_ratio > 2000:
            value_text = "🌟 Excellent Value"
            value_color = "#00b894"
        elif value_ratio > 1500:
            value_text = "👍 Good Value"
            value_color = "#fdcb6e"
        else:
            value_text = "⚠️ Premium Option"
            value_color = "#e17055"
        
        st.markdown(f'''
            <div style="background: {value_color}; color: white; padding: 10px; border-radius: 10px; text-align: center; margin-top: 15px; font-weight: bold;">
                {value_text} - ₹{value_ratio:.0f} coverage per rupee premium
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def create_comparison_chart(recommendations):
    """Create a comparison chart for recommendations"""
    if not recommendations:
        return None
    
    df = pd.DataFrame(recommendations)
    
    fig = go.Figure()
    
    # Add premium bars
    fig.add_trace(go.Bar(
        name='Monthly Premium (₹)',
        x=df['name'],
        y=df['monthly_premium'],
        yaxis='y',
        offsetgroup=1,
        marker_color='lightblue'
    ))
    
    # Add coverage bars (scaled down)
    fig.add_trace(go.Bar(
        name='Coverage (₹ Lakhs)',
        x=df['name'],
        y=df['coverage'] / 100000,  # Convert to lakhs
        yaxis='y2',
        offsetgroup=2,
        marker_color='lightgreen'
    ))
    
    fig.update_layout(
        title='Premium vs Coverage Comparison',
        xaxis_title='Insurance Products',
        yaxis=dict(
            title='Monthly Premium (₹)',
            side='left'
        ),
        yaxis2=dict(
            title='Coverage (₹ Lakhs)',
            side='right',
            overlaying='y'
        ),
        barmode='group',
        height=400
    )
    
    return fig

def main():
    # Add cyber particles for dark theme
    st.markdown('''
        <div id="particles-container">
            <div class="particle" style="left: 5%; animation-delay: 0s;"></div>
            <div class="particle" style="left: 15%; animation-delay: 3s;"></div>
            <div class="particle" style="left: 25%; animation-delay: 6s;"></div>
            <div class="particle" style="left: 35%; animation-delay: 9s;"></div>
            <div class="particle" style="left: 45%; animation-delay: 12s;"></div>
            <div class="particle" style="left: 55%; animation-delay: 15s;"></div>
            <div class="particle" style="left: 65%; animation-delay: 18s;"></div>
            <div class="particle" style="left: 75%; animation-delay: 21s;"></div>
            <div class="particle" style="left: 85%; animation-delay: 24s;"></div>
            <div class="particle" style="left: 95%; animation-delay: 27s;"></div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Header with dark theme styling - CENTER OF ATTRACTION
    st.markdown('''
        <div style="text-align: center; margin: 3rem 0 4rem 0; position: relative;">
            <div style="background: radial-gradient(circle, rgba(59, 130, 246, 0.05) 0%, transparent 70%); 
                        padding: 2rem; border-radius: 50px; margin-bottom: 1rem;">
                <h1 class="main-header">
                    <span style="font-size: 5rem; color: #FFD700; text-shadow: 0 0 20px #FFD700, 0 0 40px #FFD700, 0 0 60px #FFD700; 
                               filter: drop-shadow(0 0 15px #FFD700); animation: shieldGlow 3s ease-in-out infinite; display: inline-block;">🛡️</span> 
                    <span style="background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary), #06b6d4, #10b981); 
                                 background-size: 300% 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                                 background-clip: text; animation: gradientShift 4s ease-in-out infinite; 
                                 font-size: 4.5rem; font-weight: 900; letter-spacing: 4px; 
                                 text-shadow: 0 0 30px rgba(59, 130, 246, 0.5);">INSURANCE AI AGENT</span>
                </h1>
                <div style="background: linear-gradient(90deg, transparent, var(--accent-primary), var(--accent-secondary), transparent); 
                           height: 3px; width: 60%; margin: 1.5rem auto; border-radius: 2px; 
                           animation: lineGlow 2s ease-in-out infinite;"></div>
                <p style="color: var(--text-secondary); font-size: 1.3rem; font-weight: 600; 
                          margin-top: 1rem; letter-spacing: 2px; text-transform: uppercase; 
                          animation: fadeInOut 3s ease-in-out infinite;">
                    🤖 Powered by Advanced GenAI Technology
                </p>
            </div>
        </div>
        
        <style>
        @keyframes shieldGlow {
            0%, 100% { 
                transform: rotate(0deg) scale(1);
                text-shadow: 0 0 20px #FFD700, 0 0 40px #FFD700, 0 0 60px #FFD700;
            }
            50% { 
                transform: rotate(5deg) scale(1.1);
                text-shadow: 0 0 30px #FFD700, 0 0 60px #FFD700, 0 0 90px #FFD700;
            }
        }
        
        @keyframes lineGlow {
            0%, 100% { 
                opacity: 0.6;
                transform: scaleX(1);
            }
            50% { 
                opacity: 1;
                transform: scaleX(1.1);
            }
        }
        
        @keyframes fadeInOut {
            0%, 100% { 
                opacity: 0.7;
                transform: translateY(0px);
            }
            50% { 
                opacity: 1;
                transform: translateY(-2px);
            }
        }
        </style>
    ''', unsafe_allow_html=True)
    
    # Initialize engines
    try:
        engine, ai_agent = initialize_engines()
        data = load_data()
    except Exception as e:
        st.error(f"⚠️ Error initializing application: {str(e)}")
        st.info("Please ensure all required files are present and API keys are configured.")
        return
    
    # Enhanced Dark Sidebar with useful info
    with st.sidebar:
        st.markdown("""
        <div class='sidebar-info-box'>
            <h2 style='color: white; font-weight: 900; text-align: center; margin: 0 0 15px 0; 
                       font-size: 1.4rem; letter-spacing: 1px; text-transform: uppercase;
                       font-family: "JetBrains Mono", monospace;'>
                <span style='color: #FFB000; filter: none; -webkit-text-fill-color: #FFB000;'>🎯</span> 
                <span style='background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary)); 
                             -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>How to Use</span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        steps = [
            ("📝", "Describe Needs", "Tell us your insurance requirements"),
            ("🤖", "AI Analysis", "Get intelligent recommendations"),
            ("📊", "Compare", "Review detailed comparisons"),
            ("✅", "Decide", "Make informed choices")
        ]
        
        for emoji, title, desc in steps:
            st.markdown(f"""
            <div class='info-item'>
                <div class='info-icon'>{emoji}</div>
                <div>
                    <strong style='color: white;'>{title}</strong><br>
                    <span class='info-text'>{desc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Useful Information Section
        st.markdown("""
        <div class='sidebar-info-box'>
            <h2 style='color: white; font-weight: 900; text-align: center; margin: 0 0 15px 0; 
                       font-size: 1.4rem; letter-spacing: 1px; text-transform: uppercase;
                       background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary)); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       font-family: "JetBrains Mono", monospace;'>
            📘 Useful Information
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        useful_info = [
            ("🏥", "Health Insurance", "Covers medical expenses, hospitalization"),
            ("⚠️", "Critical Illness", "Lump sum for serious diseases"),
            ("🚨", "Accident Coverage", "Protection against accidents"),
            ("👶", "Maternity", "Pregnancy and childbirth coverage"),
            ("💰", "Premium", "Monthly payment amount"),
            ("💳", "Co-pay", "Your share of medical bills"),
            ("🛡️", "Coverage", "Maximum insurance amount"),
            ("📅", "Age Limit", "Eligible age range for policy")
        ]
        
        for icon, term, description in useful_info:
            st.markdown(f"""
            <div class='info-item'>
                <div class='info-icon'>{icon}</div>
                <div>
                    <strong style='color: white; font-size: 0.9rem;'>{term}</strong><br>
                    <span class='info-text' style='font-size: 0.8rem;'>{description}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick Tips
        st.markdown("""
        <div class='sidebar-info-box'>
            <h2 style='color: white; font-weight: 900; text-align: center; margin: 0 0 15px 0; 
                       font-size: 1.4rem; letter-spacing: 1px; text-transform: uppercase;
                       background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary)); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       font-family: "JetBrains Mono", monospace;'>
                💡 Quick Tips
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        tips = [
            "💡 Mention your age for better matches",
            "👨‍👩‍👧‍👦 Include family size if applicable", 
            "💰 Specify budget range",
            "🏥 Mention health conditions",
            "✍️ Be specific about coverage needs"
        ]
        
        for tip in tips:
            st.markdown(f"""
            <div style='background: rgba(59, 130, 246, 0.1); padding: 8px 12px; margin: 8px 0; 
                        border-radius: 8px; border-left: 3px solid var(--accent-primary);'>
                <span style='color: var(--text-primary); font-size: 0.85rem;'>{tip}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Main interface with dark styling
    st.markdown('<h2 class="perfect-match-header">🎯 Find Your Perfect Insurance Match</h2>', 
                unsafe_allow_html=True)
    
    # Custom styling for textarea with floating controls
    st.markdown('''
        <style>
        .textarea-wrapper {
            position: relative;
            margin-bottom: 40px;
        }
        
        /* Style the controls to appear floating inside textarea */
        .floating-controls {
            position: absolute;
            bottom: 15px;
            left: 15px;
            right: 15px;
            background: rgba(26, 26, 26, 0.95);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 10px 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 25px var(--shadow-primary);
            z-index: 10;
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .floating-controls .stButton button {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            font-family: 'JetBrains Mono', monospace !important;
            white-space: nowrap !important;
            min-height: 36px !important;
            height: 36px !important;
            margin: 0 !important;
        }
        
        .floating-controls .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px var(--glow-blue) !important;
        }
        
        .floating-controls .stSelectbox > div > div {
            background: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 6px !important;
            font-size: 0.85rem !important;
            min-height: 36px !important;
            height: 36px !important;
            padding: 0 10px !important;
            margin: 0 !important;
        }
        
        .floating-controls label {
            color: var(--text-secondary) !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            margin: 0 5px 0 0 !important;
        }
        
        /* Ensure textarea has enough padding for floating controls */
        .stTextArea textarea {
            padding-bottom: 70px !important;
            min-height: 160px !important;
        }
        
        /* Make controls responsive */
        @media (max-width: 768px) {
            .floating-controls {
                flex-direction: column;
                gap: 8px;
                padding: 8px 12px;
            }
            
            .floating-controls .stButton button {
                width: 100% !important;
                font-size: 0.8rem !important;
            }
            
            .stTextArea textarea {
                padding-bottom: 120px !important;
            }
        }
        </style>
    ''', unsafe_allow_html=True)
    
    # Create wrapper for textarea and floating controls
    st.markdown('<div class="textarea-wrapper">', unsafe_allow_html=True)
    
    # Main textarea
    user_query = st.text_area(
        "�️ Share your insurance goals and preferences:",
        value=st.session_state.get('sample_query', ''),
        height=160,
        placeholder="Example: I'm a 28-year-old software developer looking for comprehensive health coverage with critical illness protection. My budget is around ₹1500/month...",
        help="Include details about your age, profession, family status, health conditions, budget, and desired coverage",
        key="main_query_input"
    )
    
   
    
    col1, col2, col3 = st.columns([2.5, 1.5, 1])
    
    with col1:
        search_button = st.button(
            "🚀 Get AI Recommendations", 
            type="primary",
            help="Click to get AI-powered insurance recommendations",
            key="integrated_search_btn"
        )
    
    with col2:
        num_recommendations = st.selectbox(
            "📊 Count:", 
            [3, 5, 7, 10], 
            index=0,
            key="num_recs_select",
            help="Number of recommendations"
        )
    
    with col3:
        clear_button = st.button(
            "🔄 Clear", 
            help="Clear all inputs and start fresh",
            key="clear_btn"
        )
        if clear_button:
            st.session_state.clear()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
   
    
    sample_queries = [
        ("👨🏻‍🎓", "College student, 20, needs affordable health insurance with accident coverage"),
        ("💻", "Software developer, 28, wants comprehensive tech professional health plan"),
        ("🚗", "Uber driver, 35, looking for accident coverage with vehicle-specific benefits"),
        ("👶", "New mother, 26, needs maternity support with newborn care coverage"),
        ("👴", "Senior citizen, 68, wants health insurance for pre-existing conditions"),
        ("💼", "Startup founder, 32, needs executive health plan with critical illness"),
        ("🏥", "Doctor, 40, looking for medical professional insurance with high coverage"),
        ("🎯", "Single mother, 29, wants family health plan with maternity benefits")
    ]
    
    col1, col2 = st.columns(2)
    for i, (emoji, query) in enumerate(sample_queries):
        if i % 2 == 0:
            with col1:
                if st.button(f"{emoji} {query}", key=f"sample_main_{i}", 
                           help="Click to use this sample query", use_container_width=True):
                    st.session_state['sample_query'] = query.split(' ', 1)[1]  # Remove emoji
                    st.rerun()
        else:
            with col2:
                if st.button(f"{emoji} {query}", key=f"sample_main_{i}", 
                           help="Click to use this sample query", use_container_width=True):
                    st.session_state['sample_query'] = query.split(' ', 1)[1]  # Remove emoji
                    st.rerun()
    
    
    if search_button and user_query:
        # Enhanced loading animation
        progress_placeholder = st.empty()
        
        with progress_placeholder.container():
            st.markdown('''
                <div class="magic-loader">
                    <div style="text-align: center; color: white; font-weight: 600; margin-bottom: 20px;">
                        <h3 style="margin: 0; font-size: 1.5rem;">🧠 AI is analyzing your needs...</h3>
                        <p style="margin: 10px 0; opacity: 0.8;">Finding the perfect insurance matches for you</p>
                    </div>
                    <div class="magic-dots">
                        <div class="magic-dot"></div>
                        <div class="magic-dot"></div>
                        <div class="magic-dot"></div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
        
        try:
            import time
            start_time = time.time()
            
            # Get AI analysis
            ai_analysis = ai_agent.enhance_query_understanding(user_query)
            
            # Get recommendations
            recommendations = engine.get_recommendations(user_query, top_n=num_recommendations)
            
            processing_time = time.time() - start_time
            
            # Clear loading animation
            progress_placeholder.empty()
            
            # Success message
            st.markdown(f'''
                <div class="success-message">
                    ✅ Perfect! Found {len(recommendations)} personalized recommendations in {processing_time:.2f} seconds
                </div>
            ''', unsafe_allow_html=True)
            
            if recommendations:
                # Display AI analysis with enhanced styling
                with st.expander("🧠 AI Analysis of Your Query", expanded=True):
                    st.markdown(f'''
                        <div class="ai-analysis">
                            <h4>🤖 What Our AI Understood:</h4>
                            {ai_analysis.get('ai_analysis', 'Analysis not available')}
                        </div>
                    ''', unsafe_allow_html=True)
                
                # Generate personalized explanation
                personalized_explanation = ai_agent.generate_personalized_explanation(
                    recommendations, user_query
                )
                
                # Display explanation with enhanced styling
                
                st.markdown(f'''
                    <div class="explanation-box">
                        <h4>📋 Recommendation Summary:</h4>
                        {personalized_explanation}
                    </div>
                ''', unsafe_allow_html=True)
                
                # Display recommendations with better separation
                st.markdown('<h3 class="sub-header">🏆 Your Personalized Recommendations</h3>', 
                           unsafe_allow_html=True)
                
                user_prefs = engine.parse_user_query(user_query)
                
                for i, product in enumerate(recommendations, 1):
                    # Create clear separation between recommendations
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)); 
                               padding: 15px; border-radius: 15px; margin: 30px 0 20px 0; text-align: center;'>
                        <h2 style='color: white; margin: 0; font-weight: 800; font-family: "JetBrains Mono", monospace;'>
                            🏅 RECOMMENDATION #{i}
                        </h2>
                    </div>
                    """, unsafe_allow_html=True)
                    explanation = engine.explain_recommendation(product, user_prefs)
                    display_product_card(product, explanation)
                    
                    # Add visual separator between recommendations
                    if i < len(recommendations):
                        st.markdown('<div class="product-separator"></div>', unsafe_allow_html=True)
                
                # Enhanced Comparison Chart
                if len(recommendations) > 1:
                    st.markdown('<h3 class="sub-header">📊 Interactive Product Comparison</h3>', 
                               unsafe_allow_html=True)
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    chart = create_comparison_chart(recommendations)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    # AI comparison analysis with enhanced styling
                    comparison_analysis = ai_agent.generate_comparative_analysis(recommendations)
                    if comparison_analysis:
                        st.markdown("### 🤔 AI-Powered Comparison Analysis")
                        st.markdown(f'''
                            <div class="ai-analysis">
                                <h4>🔍 Detailed Product Comparison:</h4>
                                {comparison_analysis}
                            </div>
                        ''', unsafe_allow_html=True)
                
                # Enhanced Additional insights
                with st.expander("📈 Advanced Insights & Analytics", expanded=True):
                    st.markdown('<div class="insights-container">', unsafe_allow_html=True)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        avg_premium = sum(r['monthly_premium'] for r in recommendations) / len(recommendations)
                        st.metric("💰 Avg. Premium", f"₹{avg_premium:.0f}/month", 
                                 delta=f"Range: ₹{min(r['monthly_premium'] for r in recommendations)}-{max(r['monthly_premium'] for r in recommendations)}")
                    
                    with col2:
                        avg_coverage = sum(r['coverage'] for r in recommendations) / len(recommendations)
                        st.metric("🛡️ Avg. Coverage", format_currency(avg_coverage))
                    
                    with col3:
                        products_with_critical = sum(1 for r in recommendations if r['critical_illness'] == 'Yes')
                        st.metric("❤️ Critical Illness", f"{products_with_critical}/{len(recommendations)}", 
                                 delta="Products with coverage")
                    
                    with col4:
                        avg_copay = sum(r['co_pay'] for r in recommendations) / len(recommendations)
                        st.metric("💳 Avg. Co-pay", f"{avg_copay:.1f}%")
                    
                    # Value analysis
                    st.markdown("#### 💎 Value Analysis")
                    for product in recommendations:
                        value_ratio = product['coverage'] / product['monthly_premium']
                        st.write(f"{product['name']}: ₹{value_ratio:.0f} coverage per rupee premium")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        
            # Check if no recommendations found
            if not recommendations:
                st.warning("🤷‍♂️ No suitable products found for your requirements. Please try adjusting your criteria or being more specific about your needs.")
                st.info("💡 **Tip:** Try mentioning your age, budget range, specific coverage needs, or family situation for better results.")
        
        except Exception as e:
            # Clear loading animation
            progress_placeholder.empty()
            
            # Error message
            st.markdown(f'''
                <div class="error-message">
                    ❌ Oops! Something went wrong: {str(e)}
                    <br><small>Please try again or contact support if the issue persists.</small>
                </div>
            ''', unsafe_allow_html=True)
    
    elif search_button:
        st.warning("📝 Please enter your insurance requirements to get personalized recommendations.")
        st.info("💡 **Need help?** Try one of our sample queries from the sidebar!")
    
    # Dark Theme Footer
    st.markdown("---")
    st.markdown('''
        <div class="footer">
            <h3>🛡️ INSURANCE AI AGENT</h3>
            <p><strong>Advanced GenAI-Powered Recommendations</strong></p>
            <p>🤖 Intelligent system using cutting-edge AI for personalized insurance recommendations</p>
            <p><small>⚠️ Demo application for educational purposes. 
            Consult certified insurance professionals for actual policy decisions.</small></p>
            <p><small>💡 Built for BFSI Innovation Hackathon | 🏆 AI in Financial Services</small></p>
        </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
