import json
import logging
from typing import Dict, Any
from http import HTTPStatus

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def approve(event: Dict[str, Any]):
    body = {
        "status": "approved"
    }
    return {
        "messageVersion": event.get('messageVersion', 1),
        "response": {
            "actionGroup": event.get('actionGroup'),
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

def reject(event: Dict[str, Any], reason: str):
    body = {
        "status": "rejected",
        "reason": reason
    }
    return {
        "messageVersion": event.get('messageVersion', 1),
        "response": {
            "actionGroup": event.get('actionGroup'),
            "function": event.get("function"),
            "functionResponse": {
                "responseBody": {
                    "TEXT": {
                        "body": json.dumps(body)
                    }
                }
            },
            "sessionAttributes": event.get("sessionAttributes"),
            "promptSessionAttributes": event.get("promptSessionAttributes")
        }
    }

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
        action_group = event['actionGroup']
        function = event['function']
        message_version = event.get('messageVersion',1)
        parameters = event.get('parameters', [])

        params = {
            param["name"]: param["value"]
            for param in parameters
        }
        age = int(params["age"])
        country = str(params["country"])

        if age < 18:
            return reject(event, "Applicant below legal age")

        if country not in ["US", "CA", "UK", "canada", "Canada", "USA", "usa", "England", "england"]:
            return reject(event, "Unsupported geography")

        return approve(event)

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
