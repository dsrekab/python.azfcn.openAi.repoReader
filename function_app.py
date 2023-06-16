import azure.functions as func
import logging
import json
from services import LocalRepoReader

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="QueryRepo", auth_level=func.AuthLevel.ANONYMOUS, methods=['POST'])
def QueryRepo(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try: 
        req_body = req.get_json() 
    except ValueError: 
        raise RuntimeError("rootFolder and prompt data must be set in POST.") 
    else: 
        prompt = req_body.get('prompt')
        rootFolder = req_body.get('rootFolder') 
        if not prompt:
            raise RuntimeError("prompt data must be set in POST.")
        if not rootFolder:
            raise RuntimeError("rootFolder must be set in POST.")

    svc = LocalRepoReader()

    result = svc.queryForPrompt(rootFolder, prompt)

    return func.HttpResponse(result)