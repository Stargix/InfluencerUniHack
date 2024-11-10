# INFLUSEND
This web application helps influencers automatically categorize their Instagram messages. By integrating with the Instagram API, the application fetches all incoming messages and, with the help of an OpenAI API, classifies each message into two categories: **Business** or **Personal**. This allows influencers to easily spot collaboration or business opportunities without manually reviewing every message.

## Features

- **Instagram Message Access:** Connects to the user's Instagram API to retrieve direct messages.
- **AI-based Message Classification:** Uses the OpenAI API to analyze and classify each message as **Business** or **Non-Relevant**.
- **Dashboard View:** At the end of the day, influencers can see an organized list of messages categorized as **Business** to make sure no opportunity is missed.

## Installation
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/username/project-name.git
   
2. API keys: you need to have an .env document with the API credentials




## AI agent 
The core functionality of this application relies on an AI agent designed to interpret and classify the direct messages (DMs) received on Instagram. The AI agent is specifically trained to identify and differentiate **business offers** from other types of messages, allowing influencers to focus on relevant opportunities without sorting through each message manually.

### How the AI Agent Works

1. **Message Analysis:** Each DM is sent to the AI agent, which leverages OpenAI’s natural language processing (NLP) capabilities. The agent analyzes the message text, searching for phrases, patterns, and context that might indicate whether the message is related to **business** or is **non-relevant** (e.g., personal or casual).

2. **Classification Criteria:** The AI agent is trained to distinguish business-related messages from personal ones based on specific cues, including:
   - **Business Messages**: Messages that mention collaborations, sponsorships, product placements, or business inquiries.
   - **Non-Relevant Messages**: Messages that are casual, personal, or unrelated to business matters.
   
3. **High Accuracy:** Thanks to targeted training, the AI agent achieves a high classification accuracy, simplifying the influencer's inbox. Only messages likely to be business-relevant are displayed in the dashboard, ensuring no potential opportunity is missed.

### Benefits of AI-Powered Classification

- **Efficient Sorting:** Automates the sorting of messages, significantly reducing the time spent managing incoming DMs.
- **Prioritized Inbox:** Ensures that important business-related messages are highlighted and easily accessible for review at the end of the day.
- **Continuous Improvement:** As the AI agent processes more data, it continues to improve its classification accuracy over time.

This AI-driven classification system is central to the application, streamlining message management and enabling influencers to stay focused on valuable business connections.


## Instructions
   - npm run dev
   - ngrok http 0808
   - uvicorn main:app --reload

## WEB - Fronted Interface

The web interface is designed to help influencers manage and respond to business messages on Instagram more efficiently. Below is an overview of its main components:

1. **User Cards:** Each card on the interface represents a user who has sent a message. For influencers, this will typically include brands or businesses reaching out with work or collaboration proposals. Each card shows:
   - **User’s Name:** The name of the Instagram user- company.
   - **Message Preview:** A preview of the message content.
   - **Timestamp:** The time when the message was received.

2. **Action Buttons:**
   - **Open Instagram:** This button redirects the influencer to the specific conversation on Instagram, allowing them to respond directly within the app.
   - **Answer with AI:** This button (currently in development) is intended to generate a suggested response using AI, making it faster and easier to reply to business offers.
     ⚠️ This feature is still under construction and is listed under future improvements.

3. **Search Bar:** A search feature at the bottom of the interface allows users to quickly locate specific offers or messages by typing keywords, making it easier to manage a high volume of incoming messages.

#### Future Improvements ⚠️ 🔜
- **AI-Generated Responses:** The “Answer with AI” button will soon allow influencers to generate an AI-powered response draft. This feature is intended to save time by automatically creating personalized replies based on the message content and context.

This interface provides a centralized and streamlined way for influencers to focus on potential business collaborations, reducing the need to manually sift through each Instagram message.

