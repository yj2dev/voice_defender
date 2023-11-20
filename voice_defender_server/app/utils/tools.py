import random


def generate_dummis():
    phishing_words = [
        "계좌번호",
        "비밀번호",
        "카드번호",
        "인증번호",
        "보안카드",
        "전화번호",
        "개인정보",
        "주민번호",
        "이름",
        "생년월일",
        "은행",
        "금융기관",
        "거래내역",
        "송금",
        "입금",
        "출금",
        "핸드폰",
        "예금",
        "투자",
        "대출",
    ]

    phising_word = random.sample(phishing_words, random.randint(0, 6))
    phising_conf = round(random.uniform(0, 1), 2)
    deep_voice_conf = round(random.uniform(0, 1), 2)
    is_phising = phising_conf > 0.5
    is_deep_voice = deep_voice_conf > 0.5

    result = {
        "phising_word": phising_word,
        "phising_conf": phising_conf,
        "deep_voice_conf": deep_voice_conf,
        "is_phising": is_phising,
        "is_deep_voice": is_deep_voice,
    }

    return result
