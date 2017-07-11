# -*- coding: utf-8 -*-
"""
슬랙봇에 필요한 utils handler들을 모아 둡니다.
"""

import os

from requests import get

def forecast_result():
    """SK PLANET API를 사용합니다."""
    params = {'version': '1', 'lat': 37.543512, 'lon': 127.044696}
    headers = {'appKey': os.environ.get('SK_PLANET_KEY')}

    weather_response = get(
        "http://apis.skplanetx.com/weather/current/hourly",
        params=params, headers=headers,
    )
    weather_data = weather_response.json()

    summary = (
        weather_data['weather']['hourly'][0]['sky']['name'].encode('utf-8')
    )
    min_tem = int(
        float(weather_data['weather']['hourly'][0]['temperature']['tmin'])
    )
    max_tem = int(
        float(weather_data['weather']['hourly'][0]['temperature']['tmax'])
    )
    humidity = int(
        float(weather_data['weather']['hourly'][0]['humidity'])
    )
    wind_speed = weather_data['weather']['hourly'][0]['wind']['wspd']

    result = (
        "*하루를 시작하기 전에 오늘의 날씨를 참고하세요!*\n\n"
        "오늘의 날씨: *{summary}*\n"
        "> 최저 온도: {min_tem}도\n"
        "> 최고 온도: {max_tem}도\n"
        "> 습도: {humidity}%\n"
        "> 풍속: {wind_speed} m/s"
        .format(
            summary=summary, min_tem=min_tem, max_tem=max_tem,
            humidity=humidity, wind_speed=wind_speed,
        )
    )

    if '뇌우' in summary or '비' in summary or '눈' in summary:
        result = (
            '{result}\n'
            '*오늘은 우산을 챙기세요!*'
            .format(result=result)
        )

    return result
