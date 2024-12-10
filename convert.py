import json
import re
import os
import zipfile

# 초기 JSON 데이터 (코드 내 삽입)
json_data = {
    "id": "<id>.music.<songid>",
    "authors": ["<author>"],
    "version": "1.0",
    "objectType": "music",
    "properties": {
        "tracks": [
            {
                "source": "<filename>",
                "name": "<ensongname>"
            }
        ]
    },
    "strings": {
        "name": {
            "en-GB": "<ensongname>",
            "ko-KR": "<kosongname>"
        }
    }
}

def input_and_validate(prompt, pattern, transform=None):
    while True:
        user_input = input(prompt)
        if re.match(pattern, user_input):
            return transform(user_input) if transform else user_input
        print("입력 형식이 올바르지 않습니다. 다시 입력해주세요.")

def save_json(json_data, filename="object.json"):
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

def create_zip(zip_filename, file_name):
    try:
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write("object.json", arcname="object.json")
            zipf.write(file_name, arcname=os.path.basename(file_name))
        print(f"ZIP 파일 생성 완료: {zip_filename}")
    except Exception as e:
        print(f"ZIP 파일 생성 중 오류 발생: {e}")
    finally:
        try:
            os.remove("object.json")
        except FileNotFoundError:
            pass

# 입력받기 및 데이터 변경
json_data["id"] = f"{input_and_validate('작성자 고유 아이디(영어 소문자만): ', r'^[a-z0-9]+$')}.music.{input_and_validate('노래 아이디(영어 소문자만): ', r'^[a-z0-9]+$', lambda x: x.upper())}"
json_data["authors"] = [input_and_validate('저작자 이름 (영어): ', r'^[a-zA-Z0-9\s/|()\.]+$', lambda x: re.sub(r'[^a-zA-Z0-9\s/|()\.]', '', x))]

while True:
    file_name = input("음악 파일을 이 창으로 드래그 앤 드롭(ogg, wav, flac만 지원): ").replace('"', '').strip()
    if not os.path.exists(file_name):
        print("파일이 존재하지 않거나 읽을 수 없습니다. 다시 입력해주세요.")
        continue
    valid_extensions = ('.flac', '.wav', '.ogg')
    if not file_name.lower().endswith(valid_extensions):
        print("지원하지 않는 파일 형식입니다. 다시 입력해주세요.")
        continue
    break

json_data["properties"]["tracks"][0]["source"] = os.path.basename(file_name)
json_data["properties"]["tracks"][0]["name"] = input_and_validate('노래 이름 (영어): ', r'^[a-zA-Z0-9\s/|()\.]+$', lambda x: re.sub(r'[^a-zA-Z0-9\s/|()\.]', '', x))
json_data["strings"]["name"]["en-GB"] = json_data["properties"]["tracks"][0]["name"]
json_data["strings"]["name"]["ko-KR"] = input_and_validate('노래 이름 (한글): ', r'^[가-힣a-zA-Z0-9\s/|()\.]+$', lambda x: re.sub(r'[^가-힣a-zA-Z0-9\s/|()\.]', '', x))

# JSON 파일 저장 및 ZIP 생성
save_json(json_data)
zip_filename = f"{json_data['id']}.parkobj"
create_zip(zip_filename, file_name)
