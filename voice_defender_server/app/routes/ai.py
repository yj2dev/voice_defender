from app.utils.ai_process_pipeline import pipeline
from fastapi import APIRouter, File, UploadFile
from app.utils.tools import generate_dummis
from time import time
import datetime
import os

router = APIRouter(prefix="/api/ai", tags=["AI"])


@router.get("/", include_in_schema=False)
async def root():
    payload = {
        "/": "root",
        "method": "GET",
    }
    return payload


@router.post("/analysis")
async def upload_file(file: UploadFile = File(...)):
    start_time = time()

    file_path = os.path.join("app", "temp", file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    phising_result = None

    try:
        phising_result = pipeline(os.path.join(os.getcwd(), file_path))
    except Exception as e:
        print(f"Failed to analysis the file: {e}")
        phising_result = None

    if phising_result:
        try:
            ext_idx = file.filename.rfind(".")
            # ext = file.filename[ext_idx:]
            filename = file.filename[:ext_idx]

            converted_file_path = os.path.join("app", "temp", f"{filename}.wav")
            vocal_file_path = os.path.join("app", "temp", f"{filename}_vocal.wav")

            # os.remove(file_path)  # 원본 파일 제거
            # os.remove(converted_file_path)  # 확장자 변환 파일(.wav) 제거
            # os.remove(vocal_file_path)  # 목소리 추출 파일(_vocal.wav) 제거

        except Exception as e:
            print(f"Failed to delete the file: {e}")
    else:
        return {"status": False}

    payload = {
        "status": True,
        "filename": file.filename,
        "created_at": datetime.datetime.now().strftime("%y%m%d%H%M%S"),
        "phising_result": {
            "is_phising": phising_result["is_phising"],
            "confidence": phising_result["confidence"],
            "reasons": phising_result["reasons"],
            "text": phising_result["text"],
            "deep_voice_result": {
                "is_deep_voice": phising_result["is_deep_voice"],
                "confidence": phising_result["deep_voice_confidence"],
            },
        },
    }
    print(payload)
    print(f"/ai/analysis API 실행 시간: {int(time() - start_time)}초")  # 실행 시간 출력
    return payload


@router.post("/analysis-test")
async def upload_file_test():
    _ = generate_dummis()

    print('_["reason"] >> ', _["phising_word"])

    payload = {
        "status": True,
        "filename": "통화녹음 01012341234_231103_161127",
        "created_at": datetime.datetime.now().strftime("%y%m%d%H%M%S"),
        "phising_result": {
            "is_phising": _["is_phising"],
            "confidence": _["phising_conf"],
            "reasons": _["phising_word"],
            "text": "집에 언제오니? 으ㅡ르드오느ㅡ르집모오오옷가",
            "deep_voice_result": {
                "is_deep_voice": _["is_deep_voice"],
                "confidence": _["deep_voice_conf"],
            },
        },
    }
    print(payload)
    return payload


# ===========================================================
#           save as random filename and extension
# ===========================================================
#
# @router.post("/analysis")
# async def upload_file(file: UploadFile = File(...)):
#     start_time = time()
#
#     timestamp = datetime.datetime.now().strftime("%y%m%d%H%M%S")
#     ext = file.filename.split(".")[-1]
#
#     with open(f"app/temp/{timestamp}.{ext}", "wb") as f:
#         f.write(await file.read())
#
#     phising_result = pipeline(
#         os.path.join(os.getcwd(), "app", "temp", f"{timestamp}.{ext}")
#     )
#
#     payload = {
#         "phising_result": {
#             "is_phising": phising_result["is_phising"],
#             "confidence": phising_result["confidence"],
#             "reasons": phising_result["reasons"],
#             "text": phising_result["text"],
#             "deep_voice_result": {
#                 "is_deep_voice": phising_result["is_deep_voice"],
#                 "confidence": phising_result["deep_voice_confidence"],
#             },
#         },
#     }
#
#     print(f"/ai/analysis API 실행 시간: {int(time() - start_time)}초")  # 실행 시간 출력
#     return payload

# ===========================================================
