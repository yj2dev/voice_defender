from app.utils.stt_whisper import stt_whisper
from app.detect.find_related_words import find_related_words
from app.detect.context_detection import context_detection
from app.detect.word_detection import word_detection
from app.detect.deep_voice_detect import detect_deep_voice
from app.lib.MDX23.inference import MDX23
from app.utils.convert_audio_format_wav import convert_audio_wav


from datetime import datetime


def pipeline(input_wav_path):
    # input:
    #   input_wav_path                          : wav 파일이 저장된 경로

    # output:
    #   result
    #       test : 음성 파일에서 추출한 텍스트
    #       reasons : 입력된 wav파일에서 검출된 보이스 피싱 연관 단어 리스트
    #       is_phising : 보이스피싱 판단 결과
    #       is_deep_voice : 딥보이스 판단 결과
    #       confidence : 보이스피싱 의심 확률
    #       deep_voice_confidence : 딥보이스 의심 확률

    denoised_wav_path = convert_audio_wav(input_wav_path)

    # 1. wav 파일에서 SST, 딥보이스 분석에 방해되는 소음을 제거한다
    denoised_wav_path = MDX23(denoised_wav_path)
    print(f"[{datetime.now()}][MDX23]음성파일 노이즈 제거 완료:", denoised_wav_path)

    # 2. wav 파일로부터 SST를 진행한다.
    print(f"[{datetime.now()}][Whisper]음성파일 텍스트 추출 시작")
    text = stt_whisper(denoised_wav_path)
    print(f"[{datetime.now()}][Whisper]음성파일 텍스트 추출 완료: {text[:20]}...")

    # 3. wav 파일로 부터 보이스피싱 의심 단어를 추출하고 단어를 통한 보이스피싱 예측 데이터셋, 검출된 연관 단어를 반환받는다.
    infer_data, detected_words = find_related_words(text)

    detected_words = list(set(detected_words))
    print(f"[{datetime.now()}][Infer]보이스피싱 단어 추출 완료: {detected_words[:5]}...")

    # 4. 문맥을 통한 보이스피싱 판단( 딥러닝 Bert 사전 학습모델 사용 )
    (
        voice_phishing_suspicion_probability_sentence,
        voice_phishing_detection_result_sentence,
    ) = context_detection(text)

    # 5. 단어를 통한 보이스피싱 판단 ( 단어의 등장 횟수, 가중치, 전체 단어 수로 판단 )
    voice_phishing_suspicion_probability_word, voice_phishing_detection_result_word = (
        voice_phishing_suspicion_probability_sentence / 2,
        0,
    )
    if (
        detected_words != []
    ):  # infer_data가 None로 오는 경우 : text에서 추출된 단어가 없어 머신러닝 데이터셋 제작 불가
        (
            voice_phishing_suspicion_probability_word,
            voice_phishing_detection_result_word,
        ) = word_detection(infer_data)

    print(voice_phishing_suspicion_probability_word)
    print(voice_phishing_suspicion_probability_sentence)
    # 4번과 5번 과정을 확률값 SoftVoting 5:5, 문맥과 단어 모두 보이스피싱이라고 나오면 보이스피싱 처리,
    voice_phishing_suspicion_probability = (
        voice_phishing_suspicion_probability_word
        + voice_phishing_suspicion_probability_sentence
    ) / 1.3
    voice_phishing_detection_result = (
        1
        if (
            voice_phishing_detection_result_word
            + voice_phishing_detection_result_sentence
        )
        > 1
        else 0
    )

    if ~voice_phishing_detection_result:
        voice_phishing_suspicion_probability /= 2
    voice_phishing_suspicion_probability = round(
        float(voice_phishing_suspicion_probability), 2
    )
    print(
        f"[{datetime.now()}][Model]보이스피싱 확률: {voice_phishing_suspicion_probability}\t 보이스피싱:{voice_phishing_detection_result == 1}"
    )

    # 6. 딥보이스 판단
    deepvoice_suspicion_probability, deepvoice_detection_result = detect_deep_voice(
        denoised_wav_path
    )
    # deepvoice_suspicion_probability = 0.8
    # deepvoice_detection_result = detect_deep_voice(denoised_wav_path)

    print(
        f"[{datetime.now()}][Model]딥보이스 확률: {deepvoice_suspicion_probability}\t 딥보이스:{deepvoice_detection_result == 1}"
    )

    result = {
        "text": text,
        "reasons": detected_words,
        "is_phising": (voice_phishing_detection_result == 1),
        "is_deep_voice": (deepvoice_detection_result == 1),
        "confidence": voice_phishing_suspicion_probability,
        "deep_voice_confidence": round(float(deepvoice_suspicion_probability), 2),
    }

    # 반환
    return result

    # 반환
    # test : 음성 파일에서 추출한 텍스트
    # reasons : 입력된 wav파일에서 검출된 보이스 피싱 연관 단어 리스트
    # is_phising : 보이스피싱 판단 결과
    # is_deep_voice : 딥보이스 판단 결과
    # confidence : 보이스피싱 의심 확률
    # deep_voice_confidence : 딥보이스 의심 확률
