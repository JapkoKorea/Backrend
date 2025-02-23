from fastapi import HTTPException
from typing import Any
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough 
from utils.llm import anthropic, gpt4o_mini, gpt4o
from utils.prompts import ReservationInfoExtrator


class AgentsService:
    @staticmethod
    def info_extractor(context: str) -> Any:
        try:
            # ReservationInfoExtrator 인스턴스 생성
            tp_cs = ReservationInfoExtrator()
            
            # Prompt 템플릿 생성
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", tp_cs.system),
                    ("user", tp_cs.human),
                ]
            )

            # Chain 구성
            chain = {'context': RunnablePassthrough(),} | prompt | gpt4o | StrOutputParser()

            # Chain 실행
            result = chain.invoke({'context': context})

            return result
        except Exception as e:
            # 예외가 발생하면 HTTPException을 발생시킴
            raise HTTPException(status_code=500, detail=f"Error in extracting information: {str(e)}")
