#-*- coding:utf-8 -*-

FOOD_CATEGORY = [{
    "name": "category",
    "text": "카테고리를 선택하세요!",
    "type": "select",
    "options": [
        {
            "text": "한식",
            "value": "한식",
        },
        {
            "text": "일식",
            "value": "일식",
        },
        {
            "text": "중식",
            "value": "중식",
        },
        {
            "text": "양식",
            "value": "양식",
        },
        {
            "text": "아시아 음식",
            "value": "아시아 음식",
        },
        {
            "text": "랜덤",
            "value": "랜덤",
        },
    ],
}]

KOREAN_FOOD = [
    "삼계탕", "해물탕", "부대찌개", "순대국", "설렁탕",
    "오삼불고기", "제육볶음", "오징어볶음", "순두부찌개",
    "해장국", "떡볶이", "닭고기", "삼겹살", "생선구이",
    "치킨", "뼈해장국", "감자탕", "해물칼국수", "꼼장어",
    "곱창",
]
JAPANESE_FOOD = [
    "라멘", "스시", "돈까스", "회덮밥",
]
CHINESE_FOOD = [
    "짜장면", "짬뽕", "탕수육", "볶음밥", "삼선짜장", "깐풍기",
    "볶음짬뽕",
]
WESTERN_FOOD = [
    "스파게티", "스테이크", "리조또", "피자", "햄버거",
    "샌드위치", "샐러드",
]
ASIA_FOOD = [
    "베트남 쌀국수", "월남쌈", "해물 볶음 쌀국수",
    "파인애플 볶음밥", "타코", "부리또",
]

ALL_FOOD = \
    KOREAN_FOOD + JAPANESE_FOOD + CHINESE_FOOD + WESTERN_FOOD + ASIA_FOOD
