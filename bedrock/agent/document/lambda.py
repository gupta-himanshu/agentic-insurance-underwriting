import json
import logging
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
        action_group = event['actionGroup']
        function = event['function']
        message_version = event.get('messageVersion',1)
        parameters = event.get('parameters', {})

        # Convert list to dictionary
        params = {
            param["name"]: param["value"]
            for param in parameters
        }
        document_text = str(params["document_text"])

        # If body is a JSON string
        body = json.loads(document_text)
        applicant_name = body.get("applicant_name")
        income = body.get("income")
        credit_score = body.get("credit_score")
        age = body.get("age")
        country = body.get("country")

        response_body = {
            "applicant_name": applicant_name,
            "income": income,
            "credit_score": credit_score,
            "age": age,
            "country": country
        }
        logger.info('Response: %s', response_body)

        return {
            "messageVersion": message_version,
            "response": {
                "actionGroup": action_group,
                "function": function,
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps(response_body)
                        }
                    }
                }
            }
        }

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
