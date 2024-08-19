import boto3
import json

def load_lambda_config(json_file_path):
    """
    Load the Lambda function name and payload from a JSON file.

    :param json_file_path: Path to the JSON file containing the Lambda configuration.
    :return: Tuple containing (function_name, payload) or (None, None) if there's an error.
    """
    try:
        with open(json_file_path, 'r') as file:
            config = json.load(file)
        
        function_name = config.get('function_name')
        payload = config.get('payload')
        
        if not function_name or payload is None:
            print("Error: 'function_name' or 'payload' key missing in JSON file.")
            return None, None
        
        return function_name, payload

    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None, None

def invoke_lambda(function_name, payload, environment='default'):
    """
    Invoke an AWS Lambda function with the given name and payload.

    :param function_name: Name of the Lambda function.
    :param payload: Payload to pass to the Lambda function.
    :param environment: AWS environment (profile) to use.
    :return: Response from the Lambda function.
    """
    # Initialize a session using the specified environment's profile
    session = boto3.Session(profile_name=environment)
    
    # Initialize Lambda client
    lambda_client = session.client('lambda')
    
    # Convert payload dictionary to JSON
    payload_json = json.dumps(payload)
    
    try:
        # Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',  # Synchronous invocation
            Payload=payload_json,
        )

        # Read and return the response
        response_payload = response['Payload'].read()
        return json.loads(response_payload)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    json_file_path = 'path/to/your/config.json'
    environment = 'your-aws-environment'  # E.g., 'dev', 'prod'
    
    # Load function name and payload from the JSON file
    function_name, payload = load_lambda_config(json_file_path)
    
    if function_name and payload:
        response = invoke_lambda(function_name, payload, environment)
        print("Response from Lambda:", response)
