import whisper


def stt_whisper(wav_file_path):
    # input:
    #   wav_file_path   : wav 파일 경로

    # output:
    #   text            : wav파일의 Speech를 Text로 변환한 str

    # model = whisper.load_model("small")  # 사용 가능 모델 크기: tiny, base, small, medium, lagre, large-v2
    model = whisper.load_model(
        "small"
    )  # 사용 가능 모델 크기: tiny, base, small, medium, lagre, large-v2
    result = model.transcribe(wav_file_path)

    return result["text"]
