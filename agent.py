import logging
from config import settings

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage
from langchain_core.tools import StructuredTool

from tools import get_product_details,get_price_analysis,get_buy_recommendation,get_product_knowledge


logger = logging.getLogger("price-intelligence-agent")

product_details = StructuredTool.from_function(
    func=get_product_details,
    name="product_details",
    description=(
        "Get basic information about a product using its product ID. "
        "Returns product name, brand, category and current price."
    )
)

price_analysis = StructuredTool.from_function(
    func=get_price_analysis,
    name="price_analysis",
    description=(
        "Analyze historical price information for a product. "
        "Returns historical minimum, maximum, averages, price changes "
        "and recent price trend."
    )
)

buy_recommendation = StructuredTool.from_function(
    func=get_buy_recommendation,
    name="buy_recommendation",
    description=(
        "Calculate the deterministic buy score and recommendation "
        "for a product. Use this when the user asks whether they "
        "should buy the product now, wait, or avoid buying."
    )
)

product_knowledge = StructuredTool.from_function(
    func=get_product_knowledge,
    name="product_knowledge",
    description=(
        "Retrieve product information from the product knowledge base. "
        "Returns product description, ideal use cases, pros and cons."
    )
)


tools = [
    product_details,
    price_analysis,
    buy_recommendation,
    product_knowledge
]

tool_map = {
    tool.name: tool
    for tool in tools
}

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key = settings.groq_api_key
)

llm_with_tools = llm.bind_tools(tools)

def run_agent(
    user_query: str,
    return_trace: bool = False
):

    messages = [
        SystemMessage(
            content="""
You are a price intelligence assistant.

Your job is to answer product and price-related questions.

You have access to several tools:

1. product_details
   Use this to retrieve basic product information.

2. price_analysis
   Use this to analyze historical pricing and price trends.

3. buy_recommendation
   Use this when deciding whether the user should buy now,
   wait, or avoid buying.

4. product_knowledge
   Use this to retrieve product description, ideal use cases,
   pros and cons.

Rules:

- Use tools whenever they can provide factual information.
- Do not invent prices or product information.
- Do not perform numerical calculations yourself when a
  tool can do them.
- You may call multiple tools when necessary.
- Continue using tools until you have enough information.
- Use tool results as the source of truth.
- The final answer must be plain natural language.
- Never expose tool calls, JSON, internal reasoning, or
  implementation details to the user.
"""
        ),
        HumanMessage(content=user_query)
    ]

    trace = {
        "query": user_query,
        "llm_calls": 0,
        "tool_calls": 0,
        "tools_used": [],
        "status": "started"
    }

    while True:

       
        trace["llm_calls"] += 1

        logger.info(
            "Calling LLM | call_number=%s",
            trace["llm_calls"]
        )

        response = llm_with_tools.invoke(
            messages
        )

        # Add model response
        messages.append(response)

        if not response.tool_calls:

            trace["status"] = "completed"

            logger.info(
                "Agent completed | llm_calls=%s | "
                "tool_calls=%s | tools=%s",
                trace["llm_calls"],
                trace["tool_calls"],
                trace["tools_used"]
            )

            if return_trace:

                return {
                    "answer": response.content,
                    "trace": trace
                }

            return response.content

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]

            trace["tool_calls"] += 1
            trace["tools_used"].append(
                tool_name
            )

            logger.info(
                "Executing tool | name=%s | args=%s",
                tool_name,
                tool_args
            )

            tool = tool_map.get(tool_name)


            if tool is None:

                logger.error(
                    "Unknown tool requested: %s",
                    tool_name
                )

                tool_result = {
                    "error": (
                        f"Tool '{tool_name}' "
                        "does not exist."
                    )
                }


            else:

                try:

                    tool_result = tool.invoke(
                        tool_args
                    )

                    logger.info(
                        "Tool completed successfully | name=%s",
                        tool_name
                    )

                except Exception as error:

                    logger.exception(
                        "Tool execution failed | name=%s",
                        tool_name
                    )

                    tool_result = {
                        "error": (
                            f"Tool '{tool_name}' failed: "
                            f"{str(error)}"
                        )
                    }

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call_id
                )
            )