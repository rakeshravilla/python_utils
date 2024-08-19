import boto3
import argparse
from pipeline_parameters import parameters_dict

def list_pipeline_parameters(pipeline_id):
    """
    Lists the parameters of an AWS Data Pipeline and writes them to a file named after the pipeline.

    :param pipeline_id: The ID of the pipeline.
    :return: A list of parameter objects, each containing parameter ID and attributes.
    """
    client = boto3.client('datapipeline')
    
    # Get the pipeline description to retrieve the pipeline name
    pipeline_description = client.describe_pipelines(pipelineIds=[pipeline_id])
    pipeline_name = pipeline_description['pipelineDescriptionList'][0]['name']
    
    # Define the output file name based on the pipeline name
    output_file = f"{pipeline_name.replace(' ', '_')}_parameters.txt"
    
    # Get the pipeline definition
    response = client.get_pipeline_definition(
        pipelineId=pipeline_id
    )
    
    parameter_objects = response.get('parameterObjects', [])
    
    with open(output_file, 'w') as file:
        file.write(f"Pipeline Name: {pipeline_name}\n")
        file.write(f"Pipeline ID: {pipeline_id}\n\n")
        for param in parameter_objects:
            file.write(f"Parameter ID: {param['id']}\n")
            for attribute in param.get('attributes', []):
                file.write(f"  - {attribute['key']}: {attribute['stringValue']}\n")
            file.write("\n")  # Add a newline for better readability
    
    return parameter_objects

def activate_pipeline_with_parameters(pipeline_id, parameters_list):
    """
    Activates an AWS Data Pipeline with parameters passed as a list of dictionaries.

    :param pipeline_id: The ID of the pipeline.
    :param parameters_list: A list of dictionaries containing the parameters and their values.
                            Example: [{'id': 'myStartDateTime', 'stringValue': '2024-08-19T00:00:00'}]
    :return: The response from the activate-pipeline API call.
    """
    client = boto3.client('datapipeline')
    
    # Activate the pipeline with the parameters
    response = client.activate_pipeline(
        pipelineId=pipeline_id,
        parameterValues=parameters_list
    )
    
    return response

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Activate an AWS Data Pipeline with parameters from a dictionary.")
    parser.add_argument("pipeline_id", type=str, help="The ID of the pipeline to activate.")
    
    args = parser.parse_args()
    pipeline_id = args.pipeline_id
    
    # Check if the pipeline ID exists in the parameters dictionary
    if pipeline_id in parameters_dict:
        parameters_list = parameters_dict[pipeline_id]
        
        # List pipeline parameters
        list_pipeline_parameters(pipeline_id)
        
        # Activate pipeline with parameters from the dictionary
        response = activate_pipeline_with_parameters(pipeline_id, parameters_list)
        print(f"Pipeline {pipeline_id} activated successfully. Response: {response}")
    else:
        print(f"No parameters found for pipeline ID: {pipeline_id}")

if __name__ == "__main__":
    main()
