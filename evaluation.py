import json
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from agent import run_agent
from tools import get_buy_recommendation

TEST_CASES = [
    {
        "query": "Should I buy product P001 right now?",
        "expected_tool": "buy_recommendation"
    },
    {
        "query": "What is the current price of product P001?",
        "expected_tool": "product_details"
    },
    {
        "query": "How has the price of P001 changed recently?",
        "expected_tool": "price_analysis"
    },
    {
        "query": "Is P001 suitable for programming?",
        "expected_tool": "product_knowledge"
    },
    {
        "query": (
            "Tell me the current price of P001, "
            "analyze its recent price trend, "
            "tell me whether I should buy it now, "
            "and explain whether it is suitable for programming."
        ),
        "expected_tools": [
            "product_details",
            "price_analysis",
            "buy_recommendation",
            "product_knowledge"
        ]
    }
]

def validate_buy_recommendation(product_id):

    result = get_buy_recommendation(product_id)

    required_fields = [
        "product_id",
        "product_name",
        "current_price",
        "buy_score",
        "recommendation"
    ]

    for field in required_fields:
        if field not in result:
            return False

    if not 0 <= result["buy_score"] <= 100:
        return False

    if result["recommendation"] not in [
        "BUY",
        "WAIT",
        "AVOID"
    ]:
        return False

    return True

def evaluate_agent(test_case):

    result = run_agent(
        test_case["query"],
        return_trace=True
    )

    answer = result["answer"]
    trace = result["trace"]

    tools_used = trace["tools_used"]

    answer_valid = (
        isinstance(answer, str)
        and len(answer.strip()) > 0
    )

    tool_correct = True

    if "expected_tool" in test_case:

        expected_tool = test_case["expected_tool"]

        tool_correct = expected_tool in tools_used

    elif "expected_tools" in test_case:

        expected_tools = test_case["expected_tools"]

        tool_correct = all(
            tool in tools_used
            for tool in expected_tools
        )

    passed = (
        answer_valid
        and tool_correct
        and trace["status"] == "completed"
    )

    return {
        "passed": passed,
        "answer_valid": answer_valid,
        "tool_correct": tool_correct,
        "llm_calls": trace["llm_calls"],
        "tool_calls": trace["tool_calls"],
        "tools_used": tools_used,
        "answer": answer
    }

def run_evaluation():

    print("=" * 60)
    print("PRICE INTELLIGENCE AGENT EVALUATION")
    print("=" * 60)

    passed = 0
    failed = 0

    print("\n1. Deterministic Recommendation Test")

    if validate_buy_recommendation("P001"):

        print("PASS")
        passed += 1

    else:

        print("FAIL")
        failed += 1

    print("\n2. Agent Evaluation")

    for index, test_case in enumerate(TEST_CASES, start=1):

        print("\n" + "-" * 60)
        print(f"Test {index}")
        print(f"Query: {test_case['query']}")

        try:
            result = evaluate_agent(test_case)

            if result["passed"]:

                print("PASS")
                passed += 1

            else:

                print("FAIL")
                failed += 1

            print("Tools used :", result["tools_used"])
            print("LLM calls  :", result["llm_calls"])
            print("Tool calls :", result["tool_calls"])

            print("\nFinal answer:")
            print(result["answer"])

        except Exception as error:

            print("FAIL")
            print(f"Error: {error}")

            failed += 1

    total = passed + failed

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    print(f"Total tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")

    if total > 0:

        pass_rate = (passed / total) * 100

        print(f"Pass rate   : {pass_rate:.2f}%")

load_dotenv()

evaluator_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)



if __name__ == "__main__":
    run_evaluation()