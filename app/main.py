import uvicorn
from fastapi import FastAPI

from app.internal.db import initialize_db

from app.domain.lawyers import LawyersDomain
from app.repository.lawyers import LawyersRepository
from app.routers.lawyers import LawyersRouter


app = FastAPI()

db = initialize_db()
lawyers_repository = LawyersRepository(db)
lawyers_domain = LawyersDomain(lawyers_repository)
lawyers_router = LawyersRouter(lawyers_domain)

app.include_router(lawyers_router.router)


@app.get('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=5001, log_level="info", reload=True)



# lambda_handler = Mangum(app = app, lifespan="off")
# if __name__ == '__main__':
#     uvicorn.run("app.main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)

# def lambda_handler(event, context):
#     """Sample pure Lambda function

#     Parameters
#     ----------
#     event: dict, required
#         API Gateway Lambda Proxy Input Format

#         Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

#     context: object, required
#         Lambda Context runtime methods and attributes

#         Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

#     Returns
#     ------
#     API Gateway Lambda Proxy Output Format: dict

#         Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
#     """

#     # try:
#     #     ip = requests.get("http://checkip.amazonaws.com/")
#     # except requests.RequestException as e:
#     #     # Send some context about this error to Lambda Logs
#     #     print(e)

#     #     raise e

#     return {
#         "statusCode": 200,
#         "body": json.dumps({
#             "message": "hello world",
#             # "location": ip.text.replace("\n", "")
#         }),
#     }
