from flask import Flask, request, jsonify
import os
import asyncio
from sydney import SydneyClient

app = Flask(__name__)

# Set your Bing Chat cookie
bing_cookie = "1mukvn9IqY1X-AJ2RFW9Vy5vTd5eArDV4Z6WGPIVeEjQqZA-wrMFk5N-33ke3DmROcy1wTMd29Kf9f5yeCGDlQ0g1CY-Oeuf6X9ANLfDEhjqmTirTTwTrE7wDuZGB2EZ9cEyvXVlLbJ90SSjwiKbK8h2w9FFdLUWYj4Pq1ZWvYXPp87BouwSeyrnvX38pjSAbnlCXcn2ylFjZcmWUcQciqxgE4mB9E0j0Y53tgYMorZA"

# Set the BING_U_COOKIE environment variable
os.environ["BING_U_COOKIE"] = bing_cookie


@app.route('/api/chat', methods=['POST'])
def chat_with_sydney():
    try:
        user_input = request.json.get('input', '')

        # Initialize responses list
        responses = []

        # Initialize Sydney client
        async def chat():
            async with SydneyClient() as sydney:
                async for response in sydney.ask_stream(user_input):
                    responses.append(response)

        asyncio.run(chat())

       # Join the responses into a single string
        joined_responses = ' '.join(responses)

        # Return the joined response as a JSON object
        return jsonify({"response": joined_responses})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
