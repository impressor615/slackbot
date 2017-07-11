# -*- coding: utf-8 -*-

import bot
import json
import os

from flask import Flask, request, make_response, render_template, jsonify

pyBot = bot.Bot()
slack = pyBot.client

app = Flask(__name__)


def _event_handler(event_type, slack_event):
    """

    A helper function that routes events from Slack to our Bot
    by event type and subtype.

    """
    event = slack_event['event']
    bot_id = slack_event['event'].get('bot_id')
    hidden = slack_event.get('hidden')

    if (event_type == "message" and (not bot_id or bot_id == 'B01')
            and not hidden):

        user_id = event["user"]
        user_data = pyBot.get_user_info(user_id)
        username = user_data['user']['profile']['first_name']

        text = slack_event['event']['text'].encode('utf-8')
        channel = slack_event['event']['channel']
        if text == '가위바위보':
            pyBot.do_rcp(channel)
        if  '날씨' in text:
            pyBot.weather_forecast(channel)

    return make_response("task is completed", 200,)


def _command_handler(slack_event):
    """hear the slash commands"""
    channel = slack_event['channel_id']
    text = slack_event['text'].encode('utf-8')
    username = slack_event['user_name']

    if text == '뭐먹지':
        pyBot.choose_category(username, channel)
        return make_response("Answer machine is activated", 200,)

    return make_response("Answer machine is activated", 200,)


@app.route("/get_message", methods=["GET", "POST"])
def communicate_with_slash_commands():
    """respond to the interactive action with slash command"""
    data = json.loads(request.form['payload'])
    token = data["token"]

    if pyBot.verification != token:
        message = "Invalid Slack verification token: %s \npyBot has: \
            %s\n\n" % (slack_event["token"], pyBot.verification)
        return make_response(message, 403, {"X-Slack-No-Retry": 1})

    if 'actions' in data:
        category = data["actions"][0]["selected_options"][0]["value"]
        username = data["user"]["name"]
        message_ts = data["message_ts"]
        channel = data["channel"]["id"]
        result = pyBot.choose_food(channel, message_ts, username, category)

    return jsonify({
        "response_type": "in_channel",
        "text": result[0],
        "attachments": result[1],
    })


@app.route("/listening", methods=["GET", "POST"])
def hears():
    """
    This route listens for incoming events from Slack and uses the event
    handler helper function to route events to our Bot.
    """
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(
            slack_event["challenge"], 200,
            {"content_type": "application/json"}
        )

    if pyBot.verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s \npyBot has: \
                   %s\n\n" % (slack_event["token"], pyBot.verification)
        return make_response(message, 403, {"X-Slack-No-Retry": 1})

    if request.headers.get('X-Slack-Retry-Reason'):
        return make_response("Not real event", 403, {"X-Slack-No-Retry": 1})

    attachments = slack_event['event'].get('attachments')
    previous_event = slack_event['event'].get('previous_message')
    if previous_event:
        return make_response("Not event", 403, {"X-Slack-No-Retry": 1})
    if attachments:
        actions = attachments[0].get('actions')
        if actions:
            return make_response("Not event", 403, {"X-Slack-No-Retry": 1})
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        # Then handle the event by event_type and have your bot respond
        return _event_handler(event_type, slack_event)
    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/command", methods=["GET", "POST"])
def slash_command():

    data = request.form
    token = request.form['token']

    if pyBot.verification != token:
        message = "Invalid Slack verification token: %s \npyBot has: \
                   %s\n\n" % (token, pyBot.verification)
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    else:
        slack_event = request.form
        return _command_handler(slack_event)

    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
