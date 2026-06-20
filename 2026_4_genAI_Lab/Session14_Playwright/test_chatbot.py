from playwright.sync_api import Page, expect

from llm_judge import assert_llm_judge

input_question = "What does this product do?"


def test_chat(page: Page):
    page.goto("https://www.chatbot.com/")
    minimized_frame = page.locator("iframe[name=\"chat-widget-minimized\"]").content_frame
    minimized_frame.get_by_role("textbox", name="Write a message…").click()
    minimized_frame.get_by_role("textbox", name="Write a message…").fill(input_question)
    minimized_frame.get_by_role("textbox", name="Write a message…").press("Enter")
    minimized_frame.get_by_role("button", name="Send a message").click()

    chat_frame = page.locator("iframe[name=\"chat-widget\"]").content_frame
    typing_indicator = chat_frame.get_by_text("is typing")

    expect(typing_indicator).to_be_visible(timeout=10000)
    expect(typing_indicator).to_be_hidden(timeout=60000)

    # Grab the bot's reply from the chat grid (skip the user's message row)
    actual_response = next(
        text
        for text in chat_frame.locator("[role='grid'] [role='row']").all_inner_texts()
        if input_question not in text
    )

    expected_response = "Absolutely! ChatBot is an AI-powered chatbot platform that helps businesses automate customer conversations and support."

    assert_llm_judge(input_question, expected_response, actual_response)
    

