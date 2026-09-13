import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent import run_agent
from database import get_product
from logging_config import configure_logging


# --------------------------------
# Configure logging
# --------------------------------

configure_logging()

logger = logging.getLogger("price-intelligence-api")


# --------------------------------
# Create FastAPI application
# --------------------------------

app = FastAPI(
    title="Price Intelligence API",
    description=(
        "Backend API for the AI-powered Price Intelligence "
        "and Recommendation Platform."
    ),
    version="1.0.0"
)


# --------------------------------
# Request model
# --------------------------------

class QueryRequest(BaseModel):

    product_id: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Unique product ID, for example P001"
    )

    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="User's question about the selected product"
    )


# --------------------------------
# Response model
# --------------------------------

class QueryResponse(BaseModel):

    answer: str
    tools_used: list[str]
    llm_calls: int
    tool_calls: int
    status: str


# --------------------------------
# Root endpoint
# --------------------------------

@app.get("/")
def root():

    logger.info("Root endpoint accessed")

    return {
        "message": "Price Intelligence API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# --------------------------------
# Health check
# --------------------------------

@app.get("/health")
def health_check():

    logger.info("Health check requested")

    return {
        "status": "healthy"
    }


# --------------------------------
# Product query
# --------------------------------

@app.post(
    "/api/v1/query",
    response_model=QueryResponse
)
def query_product(request: QueryRequest):

    logger.info(
        "Received query for product_id=%s",
        request.product_id
    )

    # --------------------------------
    # Validate product
    # --------------------------------

    product = get_product(request.product_id)

    if product is None:

        logger.warning(
            "Product not found: product_id=%s",
            request.product_id
        )

        raise HTTPException(
            status_code=404,
            detail=(
                f"Product '{request.product_id}' "
                "was not found."
            )
        )

    logger.info(
        "Product validated: product_id=%s product_name=%s",
        request.product_id,
        product["product_name"]
    )

    # --------------------------------
    # Build agent query
    # --------------------------------

    agent_query = (
        f"The user is asking about product "
        f"{request.product_id} "
        f"({product['product_name']}).\n\n"
        f"User question: {request.question}"
    )

    logger.info(
        "Sending request to agent for product_id=%s",
        request.product_id
    )

    # --------------------------------
    # Execute agent
    # --------------------------------

    try:

        result = run_agent(
            agent_query,
            return_trace=True
        )

    except Exception:

        logger.exception(
            "Agent execution failed for product_id=%s",
            request.product_id
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "The AI agent failed while processing "
                "the request."
            )
        )

    # --------------------------------
    # Extract trace
    # --------------------------------

    trace = result["trace"]

    logger.info(
        "Agent completed successfully | "
        "product_id=%s | llm_calls=%s | tool_calls=%s | tools=%s",
        request.product_id,
        trace["llm_calls"],
        trace["tool_calls"],
        trace["tools_used"]
    )

    # --------------------------------
    # Return API response
    # --------------------------------

    return QueryResponse(
        answer=result["answer"],
        tools_used=trace["tools_used"],
        llm_calls=trace["llm_calls"],
        tool_calls=trace["tool_calls"],
        status=trace["status"]
    )