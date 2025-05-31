import io
import pypdf
import logging
import json
from json import JSONDecodeError
from openai import OpenAI
from bot import settings


class InvalidJSONError(Exception):
    content: str


def generate_questions(file: io.BytesIO) -> dict:
    context = settings.Context().text
    prompt = settings.Prompt().text
    reader = pypdf.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    logging.info("Generating questions for \nContext:\n" + context + "\nPrompt:\n" + prompt + "\nContent:\n" + text)
    client = OpenAI(api_key=settings.Settings().OPENAI_API_KEY.get_secret_value())
    response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            temperature=0.4,
            top_p=0.8,
            messages=[
                {"role": "system", "content": context},
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]
    )
    try:
        response = json.loads(response.choices[0].message.content)
    except JSONDecodeError:
        raise InvalidJSONError(response.choices[0].message.content)

    return response




