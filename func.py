import io
import json
import logging
import oci
import traceback
from fdk import response
import startstopOICInstance

# Setup logging
logging.basicConfig(level=logging.INFO)

def handler(ctx, data: io.BytesIO = None):
    try:
        logging.getLogger().info("Invoking startstopOICInstance function")
        
        
        # Call the startstopOICInstance function
        status = startstopOICInstance.startstopOICInstance()

        # Return a successful response
        return response.Response(
            ctx,
            response_data=json.dumps({"message": status}),
            headers={"Content-Type": "application/json"}
        )
    except Exception as ex:
        logging.getLogger().error('Error in handler: ' + str(ex))
        error_msg = f"An error occurred: {str(ex)}\n{traceback.format_exc()}"
        
        # Return an error response
        return response.Response(
            ctx,
            response_data=json.dumps({"error": error_msg}),
            headers={"Content-Type": "application/json"},
            status_code=500
        )
