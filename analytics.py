import pandas as pd
from database import get_product,get_price_history

def calculate_price_statistics(product_id):
    product = get_product(product_id)
    if product is None:
        return None
    history = get_price_history(product_id)
    if not history:
        return None
    df = pd.DataFrame(history)
    df["date"] = pd.to_datetime(df["date"])
    current_price = product["current_price"]

    historical_min = df["price"].min()
    historical_max = df["price"].max()
    historical_avg = df["price"].mean()

    last_7_days = df.tail(7)
    last_30_days = df.tail(30)
    last_90_days = df.tail(90)

    avg_7_days = last_7_days["price"].mean()
    avg_30_days = last_30_days["price"].mean()
    avg_90_days = last_90_days["price"].mean()

    price_change_7_days = (current_price - last_7_days.iloc[0]["price"])/last_7_days.iloc[0]["price"]*100

    price_change_30_days = (current_price - last_30_days.iloc[0]["price"])/last_30_days.iloc[0]["price"]*100

    price_change_90_days = (current_price - last_90_days.iloc[0]["price"])/last_90_days.iloc[0]["price"]*100

    discount_from_90_days_average = (avg_90_days - current_price) / avg_90_days * 100

    distance_from_historical_min = (current_price - historical_min) / historical_min * 100

    return {
        "product_id": product_id,
        "product_name":product["product_name"],
        "current_price":current_price,

        "historical_min": historical_min,
        "historical_max": historical_max,
        "historical_avg": historical_avg,

        "avg_7_days": avg_7_days,
        "avg_30_days": avg_30_days,
        "avg_90_days": avg_90_days,

        "price_change_7_days": price_change_7_days,
        "price_change_30_days": price_change_30_days,
        "price_change_90_days": price_change_90_days,

        "discount_from_90_days_average": discount_from_90_days_average,
        "distance_from_historical_min": distance_from_historical_min
    } 

def calculate_price_trend(product_id):
    history = get_price_history(product_id)
    if not history:
        return None

    df = pd.DataFrame(history)

    df["date"] = pd.to_datetime(df["date"])
    recent_prices = df.tail(30)

    first_price = recent_prices.iloc[0]["price"]
    last_price = recent_prices.iloc[-1]["price"]

    percentage_change = (last_price - first_price)/first_price*100

    if percentage_change <=-3:
        trend = "Decreasing"

    elif percentage_change>=3:
        trend = "Increasing"

    else:
        trend = "Stable"

    return {
        "trend":trend,
        "percentage_change":percentage_change,
    }

def analyze_product(product_id):
    statistics = calculate_price_statistics(product_id)
    if statistics is None:
        return None
    trend = calculate_price_trend(product_id)
    statistics["trend"] = trend["trend"]
    statistics["trend_percentage"] = trend["percentage_change"]

    return statistics

def calculate_buy_score(product_id):
    analysis = analyze_product(product_id)
    if analysis is None:
        return None
    score = 50
    discount = analysis["discount_from_90_days_average"]

    if discount >= 10:
        score += 25

    elif discount >= 5:
        score+=15

    elif discount>=2:
        score+=8

    elif discount<0:
        score-=15

    distance_from_min = analysis["distance_from_historical_min"]

    if distance_from_min <= 3:
        score+=15

    elif distance_from_min<=7:
        score+=8
    elif distance_from_min>=15:
        score-=10

    trend = analysis["trend"]

    if trend == "Decreasing":
        score+=10

    elif trend == "Increasing":
        score-=10

    score = max(0, min(100, score))

    if score >=75:
        recommendation = "BUY"

    elif score>=50:
        recommendation = "WAIT"

    else:
        recommendation = "AVOID"

    analysis["buy_score"] = score
    analysis["recommendation"] = recommendation

    return analysis
