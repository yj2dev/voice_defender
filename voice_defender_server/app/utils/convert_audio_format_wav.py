from pydub import AudioSegment


def convert_audio_wav(audio_path):
    # input:
    #   audio_path  : 입력된 음성 파일의 저장 경로

    # output:
    #   result_path : wav로 변환된 음성 파일의 경로

    audio_path = audio_path.replace("\\", "/")

    # 입력된 음성 파일의 확장자를 구한다.
    file_format = audio_path[audio_path.rfind(".") + 1 :]

    # 음성 파일을 읽는다.
    audio = AudioSegment.from_file(audio_path, format=file_format)

    # 음성 파일을 wav로 저장한다.
    audio.export(audio_path[: -len(file_format) - 1] + ".wav", format="wav")

    # 저장된 파일 경로를 반환한다.
    result_path = audio_path[: -len(file_format) - 1] + ".wav"
    return result_path
