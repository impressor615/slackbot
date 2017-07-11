# -*- coding: utf-8 -*-
"""
Python Slack Bot class for use with the pythOnBoarding app
"""
import os
import random

from answers import *
from slackclient import SlackClient
from utils import forecast_result


class Bot(object):
    """Instanciates a Bot object to handle interactions with Slack"""
    def __init__(self):
        super(Bot, self).__init__()
        self.name = "정답머신"
        self.emoji = ":robot_face:"
        self.oauth = {
            "client_id": os.environ.get("CLIENT_ID"),
            "client_secret": os.environ.get("CLIENT_SECRET"),
            "scope": "bot"
        }
        self.verification = os.environ.get("VERIFICATION_TOKEN")
        self.client = SlackClient(os.environ.get("BOT_TOKEN"))


    def do_rcp(self, channel):
        """play rock. scissor, paper game with friends"""
        self.name = '게임봇'
        self.emoji = ':video_game:'
        result = random.choice([':v:', ':hand:', ':fist:'])
        self.client.api_call(
            'chat.postMessage', channel=channel,
            username=self.name, icon_emoji=self.emoji,
            text=result
        )

    def not_developed(self, username, channel):
        """when bot can't answer properly, this function will be executed"""
        self.client.api_call(
            "chat.postMessage", channel=channel,
            username=self.name, icon_emoji=self.emoji,
            text=(
                "*{username}님*, 죄송해요. 그건 제가 아직 하지 못하는 일이에요.\n "
                "이번에 요청하신 것도 곧 빨리 배워볼게요!:thumbsup:"
                .format(username=username)
            ),
        )

    def weather_forecast(self, channel):
        """return the current weather forecast hourly"""
        self.name = '날씨봇'
        self.emoji = ':beach_with_umbrella:'
        self.client.api_call(
            'chat.postMessage', channel=channel,
            username=self.name, icon_emoji=self.emoji,
            text=forecast_result(),
        )

    def get_user_info(self, user_id):
        """get slack user information"""
        data = self.client.api_call(
            'users.info',
            user=user_id,
        )
        return data

    def choose_category(self, username, channel):
        """choose what to eat instead of users"""
        text = (
            "*{username}님*, 무엇을 먹을지 고민이시군요?\n"
            .format(username=username)
        )
        attachments = [{
            "fallback": "오류가 발생했습니다.",
            "callback_id": "food_recommendation",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": FOOD_CATEGORY,
        }]

        self.client.api_call(
            'chat.postMessage', channel=channel,
            username=self.name, icon_emoji=self.emoji,
            text=text, attachments=attachments,
        )
        return text, attachments

    def choose_food(self, channel, message_ts, username, category):
        """Based on the category user chose, recommend what food to eat"""
        category = category.encode('utf-8')
        if category == '한식':
            candidate = KOREAN_FOOD
        if category == '일식':
            candidate = JAPANESE_FOOD
        if category == '중식':
            candidate = CHINESE_FOOD
        if category == '양식':
            candidate = WESTERN_FOOD
        if category == '아시아 음식':
            candidate = ASIA_FOOD
        if category == '랜덤':
            candidate = ALL_FOOD
        suggestion = random.choice(candidate)
        text = "*{username}님*, 저의 추천이 마음에 드셨으면 좋겠네요!" \
            .format(username=username)
        attachments = [{
            "title": '{suggestion}를 드시면 어떨까요?!' \
                .format(suggestion=suggestion),
            "callback_id": "food_decision",
            "color": "#3AA3E3",
        }]
        self.client.api_call(
            'chat.update', channel=channel, ts=message_ts
        )
        return text, attachments
