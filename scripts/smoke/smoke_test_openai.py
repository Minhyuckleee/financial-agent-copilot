"""OpenAI API 키 최소 호출 검증. 실행: python scripts/smoke_test_openai.py"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def main() -> None:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.environ.get("OPENAI_MODEL", "gpt-4.1")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "한 단어로만 답해: 성공"}],
        max_tokens=10,
    )
    print(f"[OK] model={model} response={response.choices[0].message.content!r}")


if __name__ == "__main__":
    main()
