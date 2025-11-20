from .config import REPORT_DIR, openai_client

def generate_report(dev_prompt, user_prompt, ticker: str):
    response = openai_client.responses.create(
        model="o4-mini",
        input=[
            {"role": "developer", "content": dev_prompt},
            {"role": "user", "content": user_prompt},
        ],
        tools=[
            {
                "type": "web_search_preview",
                "user_location": {"type": "approximate", "country": "KR"},
            }
        ],
    )

    text = response.output_text
    out = REPORT_DIR / f"{ticker}.md"
    out.write_text(text, encoding="utf-8")
    return out