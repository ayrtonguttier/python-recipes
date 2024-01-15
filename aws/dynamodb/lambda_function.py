import json
import boto3
from boto3.dynamodb.conditions import Attr

dynamodb_resource = boto3.resource("dynamodb")

pessoa_table = dynamodb_resource.Table("pessoa")


def mostrar_resultado(result):
    for item in result["Items"]:
        print(item["cpf"])
        print(item["nome"])
        print(item["status_registro"])


def primeiro_item(result):
    return result["Items"][0]


def atualizar_status(item):
    item_key = {"cpf": item["cpf"]}
    update_expression = "SET status_registro = :novo_status"
    update_parameters = {":novo_status": 1}
    response = pessoa_table.update_item(
        Key=item_key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=update_parameters,
    )
    print(response)


def lambda_handler(event, context):
    # Consulta com filtros
    query_result = pessoa_table.scan(
        TableName="pessoa", FilterExpression=Attr("status_registro").eq(0)
    )

    if query_result["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return {
            "statusCode": 200,
            "body": json.dumps(query_result["Items"], default=str),
        }

    return {"statusCode": 500, "body": "Erro"}