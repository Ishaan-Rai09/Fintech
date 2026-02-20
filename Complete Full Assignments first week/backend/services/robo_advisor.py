"""
Robo-Advisory service
"""
from typing import Dict, Any, List
import numpy as np


class RoboAdvisor:
    """Robo-advisory service for investment recommendations"""
    
    # Risk profile questions
    RISK_QUESTIONNAIRE = [
        {
            "id": 1,
            "question": "What is your age?",
            "options": [
                {"value": "18-30", "score": 5},
                {"value": "31-45", "score": 4},
                {"value": "46-60", "score": 3},
                {"value": "60+", "score": 2}
            ]
        },
        {
            "id": 2,
            "question": "What is your investment time horizon?",
            "options": [
                {"value": "Less than 3 years", "score": 2},
                {"value": "3-5 years", "score": 3},
                {"value": "5-10 years", "score": 4},
                {"value": "More than 10 years", "score": 5}
            ]
        },
        {
            "id": 3,
            "question": "How would you react to a 20% drop in your portfolio?",
            "options": [
                {"value": "Panic and sell everything", "score": 1},
                {"value": "Feel uncomfortable but hold", "score": 2},
                {"value": "Stay calm and wait for recovery", "score": 3},
                {"value": "See it as a buying opportunity", "score": 5}
            ]
        },
        {
            "id": 4,
            "question": "What is your primary investment goal?",
            "options": [
                {"value": "Capital preservation", "score": 1},
                {"value": "Income generation", "score": 2},
                {"value": "Balanced growth", "score": 3},
                {"value": "Aggressive growth", "score": 5}
            ]
        },
        {
            "id": 5,
            "question": "What percentage of your income can you invest?",
            "options": [
                {"value": "Less than 10%", "score": 2},
                {"value": "10-20%", "score": 3},
                {"value": "20-30%", "score": 4},
                {"value": "More than 30%", "score": 5}
            ]
        }
    ]
    
    @staticmethod
    def calculate_risk_score(answers: List[int]) -> Dict[str, Any]:
        """
        Calculate risk score from questionnaire answers
        
        Args:
            answers: List of scores from questionnaire
        """
        total_score = sum(answers)
        max_score = 25  # 5 questions * 5 max score
        
        risk_score = int((total_score / max_score) * 10)  # Scale to 1-10
        
        # Categorize risk
        if risk_score <= 3:
            category = "Conservative"
            description = "Low risk tolerance, focus on capital preservation"
        elif risk_score <= 5:
            category = "Moderately Conservative"
            description = "Below average risk tolerance, prefer stability"
        elif risk_score <= 7:
            category = "Moderate"
            description = "Balanced approach between risk and return"
        elif risk_score <= 8:
            category = "Moderately Aggressive"
            description = "Above average risk tolerance, growth-oriented"
        else:
            category = "Aggressive"
            description = "High risk tolerance, maximize growth potential"
        
        return {
            "risk_score": risk_score,
            "category": category,
            "description": description
        }
    
    @staticmethod
    def recommend_asset_allocation(risk_score: int) -> Dict[str, float]:
        """
        Recommend asset allocation based on risk score (1-10)
        """
        # Asset classes: Stocks, Bonds, Cash, Alternative
        if risk_score <= 2:
            # Very Conservative
            allocation = {
                "stocks": 20,
                "bonds": 60,
                "cash": 15,
                "alternative": 5
            }
        elif risk_score <= 4:
            # Conservative
            allocation = {
                "stocks": 35,
                "bonds": 50,
                "cash": 10,
                "alternative": 5
            }
        elif risk_score <= 6:
            # Moderate
            allocation = {
                "stocks": 60,
                "bonds": 30,
                "cash": 5,
                "alternative": 5
            }
        elif risk_score <= 8:
            # Aggressive
            allocation = {
                "stocks": 75,
                "bonds": 15,
                "cash": 5,
                "alternative": 5
            }
        else:
            # Very Aggressive
            allocation = {
                "stocks": 90,
                "bonds": 5,
                "cash": 0,
                "alternative": 5
            }
        
        return allocation
    
    @staticmethod
    def recommend_securities(risk_score: int, investment_amount: float = 10000) -> Dict[str, Any]:
        """
        Recommend specific securities based on risk profile
        """
        allocation = RoboAdvisor.recommend_asset_allocation(risk_score)
        
        # Example recommendations (in production, use real-time data)
        recommendations = {
            "stocks": [],
            "bonds": [],
            "etfs": []
        }
        
        if allocation["stocks"] > 0:
            if risk_score <= 4:
                recommendations["stocks"] = [
                    {"ticker": "JNJ", "name": "Johnson & Johnson", "allocation_pct": 30},
                    {"ticker": "PG", "name": "Procter & Gamble", "allocation_pct": 35},
                    {"ticker": "KO", "name": "Coca-Cola", "allocation_pct": 35}
                ]
                recommendations["etfs"].append(
                    {"ticker": "VOO", "name": "Vanguard S&P 500 ETF", "allocation_pct": allocation["stocks"]}
                )
            elif risk_score <= 7:
                recommendations["stocks"] = [
                    {"ticker": "AAPL", "name": "Apple Inc.", "allocation_pct": 25},
                    {"ticker": "MSFT", "name": "Microsoft", "allocation_pct": 25},
                    {"ticker": "GOOGL", "name": "Alphabet", "allocation_pct": 25},
                    {"ticker": "AMZN", "name": "Amazon", "allocation_pct": 25}
                ]
                recommendations["etfs"].append(
                    {"ticker": "QQQ", "name": "Invesco QQQ Trust", "allocation_pct": allocation["stocks"]}
                )
            else:
                recommendations["stocks"] = [
                    {"ticker": "TSLA", "name": "Tesla", "allocation_pct": 20},
                    {"ticker": "NVDA", "name": "NVIDIA", "allocation_pct": 20},
                    {"ticker": "AMD", "name": "AMD", "allocation_pct": 20},
                    {"ticker": "ARKK", "name": "ARK Innovation ETF", "allocation_pct": 40}
                ]
        
        if allocation["bonds"] > 0:
            recommendations["bonds"] = [
                {"ticker": "AGG", "name": "iShares Core US Aggregate Bond ETF", "allocation_pct": 60},
                {"ticker": "BND", "name": "Vanguard Total Bond Market ETF", "allocation_pct": 40}
            ]
        
        # Calculate dollar amounts
        for category in recommendations:
            for security in recommendations[category]:
                allocation_pct = security["allocation_pct"]
                category_allocation = allocation.get(category, allocation.get("stocks", 0))
                
                dollar_amount = investment_amount * (category_allocation / 100) * (allocation_pct / 100)
                security["recommended_amount"] = round(dollar_amount, 2)
        
        return {
            "asset_allocation": allocation,
            "securities": recommendations,
            "total_investment": investment_amount
        }
    
    @staticmethod
    def rebalancing_strategy(current_allocation: Dict[str, float],
                            target_allocation: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate rebalancing strategy
        """
        rebalancing_needed = {}
        
        for asset_class in target_allocation:
            current = current_allocation.get(asset_class, 0)
            target = target_allocation[asset_class]
            difference = target - current
            
            if abs(difference) > 5:  # Only rebalance if difference > 5%
                action = "increase" if difference > 0 else "decrease"
                rebalancing_needed[asset_class] = {
                    "current_pct": current,
                    "target_pct": target,
                    "difference_pct": difference,
                    "action": action
                }
        
        return {
            "rebalancing_needed": len(rebalancing_needed) > 0,
            "adjustments": rebalancing_needed,
            "strategy": "Sell overweight positions and buy underweight positions"
        }
