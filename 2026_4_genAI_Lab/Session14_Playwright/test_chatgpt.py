from playwright.sync_api import Page, expect

def test_chat(page: Page):
    page.goto("https://www.chatbot.com/")
    minimized_frame = page.locator("iframe[name=\"chat-widget-minimized\"]").content_frame
    minimized_frame.get_by_role("textbox", name="Write a message…").click()
    minimized_frame.get_by_role("textbox", name="Write a message…").fill("What does this product do?")
    minimized_frame.get_by_role("textbox", name="Write a message…").press("Enter")
    minimized_frame.get_by_role("button", name="Send a message").click()

    chat_frame = page.locator("iframe[name=\"chat-widget\"]").content_frame
    typing_indicator = chat_frame.get_by_text("is typing")

    # Wait for the bot to start and finish responding (to_be_hidden passes immediately
    # if "is typing" isn't in the DOM yet, so confirm it appears first)
    expect(typing_indicator).to_be_visible(timeout=10000)
    expect(typing_indicator).to_be_hidden(timeout=60000)
    expect(chat_frame.get_by_text("Absolutely! ChatBot is an AI-")).to_be_visible(timeout=10000)