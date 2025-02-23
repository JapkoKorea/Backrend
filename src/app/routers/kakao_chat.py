from fastapi import APIRouter, Request
from services.agents import AgentsService
router = APIRouter()

@router.post("/chatbot")
async def kakao_chatbot(request: Request):
    data = await request.json()
    user_message = data.get("userRequest", {}).get("utterance", "")

    # # 간단한 자동 응답 로직
    # if "안녕" in user_message:
    #     response_text = "안녕하세요! 무엇을 도와드릴까요?"
    # elif "운영 시간" in user_message:
    #     response_text = "저희 운영 시간은 9:00 AM ~ 6:00 PM 입니다."
    # else:
    #     response_text = "죄송해요, 이해하지 못했어요. 다시 한번 말씀해주세요."
    result = AgentsService.info_extractor(user_message)
    print('결과', result)
    return {
        "version": "2.0",
        "data": {"text": result}
        # "template": {
        #     "outputs": [
        #         {
        #             "simpleText": {
        #                 "text": response_text
        #             }
        #         }
            # ]
        # }
    }
