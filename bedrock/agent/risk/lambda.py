import logging
import json
from typing import Dict, Any
from http import HTTPStatus

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for processing Bedrock agent requests.

    Args:
        event (Dict[str, Any]): The Lambda event containing action details
        context (Any): The Lambda context object

    Returns:
        Dict[str, Any]: Response containing the action execution results

    Raises:
        KeyError: If required fields are missing from the event
    """
    try:
        parameters = event.get("parameters", [])
        print(json.dumps(event))

        # Convert list to dictionary
        params = {
            param["name"]: param["value"]
            for param in parameters
        }

        income = float(params["income"])
        credit_score = float(params["credit_score"])

        risk_score = (income * 0.3) + (credit_score * 0.7)
        risk_level = "HIGH" if risk_score < 30450 else "LOW"
        body = {
            "risk_score": risk_score,
            "risk_level": risk_level
        }

        resp = {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": "action_group_quick_start_nf3yc",
                "function": event.get("function"),
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps(body)
                        }
                    }
                }
            }
        }

        print(json.dumps(resp))

        return resp

    except KeyError as e:
        logger.error('Missing required field: %s', str(e))
        return {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body': f'Error: {str(e)}'
        }
    except Exception as e:
        logger.error('Unexpected error: %s', str(e))
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': 'Internal server error'
        }
