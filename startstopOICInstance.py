import io
import json
import oci
import base64
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_integrationinstance_client():
    try:
        signer = oci.auth.signers.get_resource_principals_signer()
        return oci.integration.IntegrationInstanceClient(config={}, signer=signer)
    except Exception as e:
        config = oci.config.from_file("~/.oci/config","<region-name>")
        return oci.integration.IntegrationInstanceClient(config)

def get_secrets_client():
    try:
        signer = oci.auth.signers.get_resource_principals_signer()
        return oci.secrets.SecretsClient(config={}, signer=signer)
    except Exception as e:
        config = oci.config.from_file("~/.oci/config","<region-name>")
        return oci.secrets.SecretsClient(config)

def get_secret_value(secret_id):
    try:
        secrets_client = get_secrets_client()
        secret_bundle = secrets_client.get_secret_bundle(secret_id)
        secret_content = base64.b64decode(secret_bundle.data.secret_bundle_content.content)
        return secret_content.decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to retrieve secret value: {e}")
        return None

def get_instance_status(ocid):
    try:
        integration_instance_client = get_integrationinstance_client()
        integration_instance = integration_instance_client.get_integration_instance(ocid)
        return integration_instance.data.lifecycle_state
    except Exception as e:
        logger.error(f"Failed to get instance status: {e}")
        return None

def start_instance(ocid):
    try:
        integration_instance_client = get_integrationinstance_client()
        response = integration_instance_client.start_integration_instance(ocid)
        return response
    except Exception as e:
        logger.error(f"Failed to start instance: {e}")
        return None

def stop_instance(ocid):
    try:
        integration_instance_client = get_integrationinstance_client()
        response = integration_instance_client.stop_integration_instance(ocid)
        return response
    except Exception as e:
        logger.error(f"Failed to stop instance: {e}")
        return None

def startstopOICInstance():
    secret_id ="<secret_ocid>" 
    ocid = get_secret_value(secret_id)

    if not ocid:
        outcome = "Failed to retrieve the OCID from the vault secret."
        logger.error(outcome)
        return outcome

    logger.info("Checking instance status...")
    status = get_instance_status(ocid)

    if status is None:
        outcome = "Failed to get instance status."
        logger.error(outcome)
        return outcome
    
    logger.info(f"Current instance status: {status}")

    if status == "ACTIVE":
        if stop_instance(ocid) is None:
            return "Failed to stop instance."
        
        outcome = "Instance will be stopped in few mins"
        logger.info(outcome)
        return outcome
    elif status == "INACTIVE":
        if start_instance(ocid) is None:
            return "Failed to start instance."
        
        outcome = "Instance will be started in few mins"
        logger.info(outcome)
        return outcome
    else:
        outcome = f"Instance is in {status} state. No action taken."
        logger.info(outcome)
        return outcome

if __name__ == '__main__':
    startstopOICInstance()
