import os
import boto3
from botocore.exceptions import ClientError

# 환경 변수에서 DynamoDB 설정 로드
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "click_records")
AWS_REGION = os.getenv("AWS_REGION", "us-northeast-2")
DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", None)  # DynamoDB Local 용

# DynamoDB 리소스 생성
dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    endpoint_url=DYNAMODB_ENDPOINT  # DynamoDB Local 실행 시 필요
)

# 테이블 객체 가져오기
table = dynamodb.Table(DYNAMODB_TABLE)

def save_record(pk: str, sk: str, data: dict):
    """
    데이터를 DynamoDB 테이블에 저장
    :param record_id: 레코드의 고유 ID
    :param data: 저장할 데이터 (dict 형태)
    :return: DynamoDB 응답
    """
    try:
        response = table.put_item(
            Item={
                "PK": pk,
                "SK": sk,
                **data
            }
        )
        return response
    except ClientError as e:
        print(f"Error saving record to DynamoDB: {e.response['Error']['Message']}")
        raise

# def get_record(record_id: str):
#     """
#     DynamoDB에서 특정 ID의 데이터를 조회
#     :param record_id: 조회할 레코드의 ID
#     :return: 조회된 데이터 또는 None
#     """
#     try:
#         response = table.get_item(Key={"id": record_id})
#         return response.get("Item", None)
#     except ClientError as e:
#         print(f"Error getting record from DynamoDB: {e.response['Error']['Message']}")
#         raise

# def delete_record(record_id: str):
#     """
#     DynamoDB에서 특정 ID의 데이터를 삭제
#     :param record_id: 삭제할 레코드의 ID
#     :return: DynamoDB 응답
#     """
#     try:
#         response = table.delete_item(Key={"id": record_id})
#         return response
#     except ClientError as e:
#         print(f"Error deleting record from DynamoDB: {e.response['Error']['Message']}")
#         raise

