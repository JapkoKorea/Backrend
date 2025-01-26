import boto3
from models.user_model import UserModel
from boto3.dynamodb.conditions import Key
# DynamoDB 초기화
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("test")  # DynamoDB 테이블 이름

def save_user(user: UserModel):
    """사용자 정보를 DynamoDB에 저장"""
    table.put_item(Item=user.dict())

def get_user_by_pk(pk: str):
    """사용자 정보를 pk로 조회"""
    response = table.get_item(Key={"pk": pk, "sk": "info"})
    return response.get("Item")

def update_user(user: UserModel):
    """사용자 정보를 업데이트"""
    table.put_item(Item=user.dict())

def delete_session(pk: str):
    table.delete_item(Key={"pk": pk, "sk": "session"})

def query_info(kakao_id: str):
    try:
        variable = table.query(
            IndexName="info-index",
            KeyConditionExpression=Key('sk').eq('info'),
            FilterExpression=Key('OAuth').eq(f'kakao#{kakao_id}')
        )
        data = variable['Items']
        
        return data[0]
    except Exception as e:
        
        return None
# import boto3
# from models.session_model import SessionModel

# dynamodb = boto3.resource("dynamodb")
# table = dynamodb.Table("test")  # DynamoDB 테이블 이름

# def save_session(session: SessionModel):
#     table.put_item(Item=session.dict())

# def get_session(pk: str):
#     response = table.get_item(Key={"pk": pk, "sk": "session"})
#     return response.get("Item")

# def delete_session(pk: str):
#     table.delete_item(Key={"pk": pk, "sk": "session"})