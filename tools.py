from analytics import analyze_product, calculate_buy_score
from database import get_product
from rag import retrieve_product_by_id

def get_product_details(product_id:str):
    product = get_product(product_id)
    if product is None:
        return {
            "error":f"Product {product_id} not found."
        }

    return product

def get_price_analysis(product_id:str):
    analysis = analyze_product(product_id)
    if analysis is None:
        return {
            "error":f"Price analysis for product {product_id} not found."
        }
    return analysis

def get_buy_recommendation(product_id:str):
    analysis = calculate_buy_score(product_id)
    if analysis is None:
        return {
            "error":f"Buy recommendation for product {product_id} not found."
        }
    return {
        "product_id":analysis["product_id"],
        "product_name":analysis["product_name"],
        "current_price":analysis["current_price"],
        "buy_score":analysis["buy_score"],
        "recommendation":analysis["recommendation"],
        "trend":analysis["trend"],
        "discount_from_90_days_average":analysis["discount_from_90_days_average"],
        "distance_from_historical_min":analysis["distance_from_historical_min"],
    }

def get_product_knowledge(product_id:str):
    document = retrieve_product_by_id(product_id)
    if document is None:
        return {
            "error":f"Product knowledge for product {product_id} not found."
        }
    return {
        "product_id":product_id,
        "product_name":document.metadata["product_name"],
        "information":document.page_content
    }