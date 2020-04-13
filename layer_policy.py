import click
import boto3

from botocore.exceptions import ClientError, EndpointConnectionError, ProfileNotFound
from termcolor import colored

@click.option('-a', '--account-id', required=True, help='AWS Account Id to add to layer permission.')
@click.option('-r', '--region', required=True, default='ca-central-1', help='The region to use.')
@click.option('-p', '--profile', required=True, help='Use a specific profile from your credential file.')
@click.command()
def cli(account_id, region, profile):
  try:
    session = boto3.Session(profile_name=profile, region_name=region)
  except ProfileNotFound as e:
    error(e)
    exit(1)
  client = session.client('lambda')
  paginator = client.get_paginator('list_layers')
  page_iterator = paginator.paginate()

  try:
    for response in page_iterator:
      layers = response['Layers']
      for layer in layers:
        layer_name = layer['LayerName']
        latest_version = layer['LatestMatchingVersion']['Version']
        try:
          client.add_layer_version_permission(
            LayerName=layer_name,
            VersionNumber=latest_version,
            StatementId=account_id,
            Action='lambda:GetLayerVersion',
            Principal=account_id,
          )
          success_msg = "Successfully added AccountId '{}' to '{}:{}' permissions.".format(
            account_id,
            layer_name,
            latest_version
          ) 
          success(success_msg)
        except client.exceptions.InvalidParameterValueException as e:
          error(e)
          exit(1)
        except client.exceptions.ResourceConflictException:
          msg = "AccountId '{}' is already authorized to access layer '{}:{}'. Skipping.".format(
            account_id,
            layer_name,
            latest_version
          )
          warning(msg)
  except EndpointConnectionError as e:
    error("{}. Maybe you entered an incorrect region?".format(e))

def error(msg):
  print_colored(msg, 'red')
def warning(msg):
  print_colored(msg, 'yellow')
def success(msg):
  print_colored(msg, 'green')
def print_colored(msg, color):
  click.echo(colored(msg, color))