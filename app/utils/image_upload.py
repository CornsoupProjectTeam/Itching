import os
import imghdr
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

# 허용된 파일 확장자 목록
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
VALID_IMAGE_TYPES = {'jpeg', 'png', 'gif'}

# 확장자 검증
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# UUID 기반으로 난수화된 파일명 생성
def generate_random_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    random_filename = f"{uuid.uuid4().hex}.{ext}"
    return random_filename

# 이미지 파일 검증 (서버 측에서 실제 이미지 파일 여부 확인)
def validate_image_file(filepath):
    file_type = imghdr.what(filepath)
    return file_type in VALID_IMAGE_TYPES

# 사용자별 폴더 생성
def create_user_folder(upload_folder):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

# 이미지 업로드 함수
def upload_image(file, user_id):
    try:
        # 파일 확장자 검증
        if not file or not allowed_file(file.filename):
            raise ValueError('허용되지 않는 파일 형식입니다.')

        # 사용자별 업로드 폴더 경로 설정
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
        create_user_folder(upload_folder)  # 폴더 생성

        # 난수화된 파일명 생성
        random_filename = generate_random_filename(file.filename)

        # 파일 경로 설정
        file_path = os.path.join(upload_folder, random_filename)

        # 파일 저장
        file.save(file_path)

        # 서버 측 파일 검증
        if not validate_image_file(file_path):
            os.remove(file_path)  # 검증 실패 시 파일 삭제
            raise ValueError('이미지 파일 형식이 아닙니다.')

        # 파일 권한 설정 (읽기/쓰기 제한)
        # os.chmod(file_path, 0o644)  # 소유자는 읽기/쓰기, 그룹/기타는 읽기만 가능

        return random_filename, None

    except (OSError, IOError) as e:
        # 파일 저장, 폴더 생성 중 오류 처리
        return None, f'파일 처리 중 오류가 발생했습니다: {str(e)}'
    
    except ValueError as ve:
        # 잘못된 파일 형식 등 사용자 오류 처리
        return None, str(ve)
    
    except Exception as e:
        # 기타 예상치 못한 오류 처리
        return None, f'예상치 못한 오류가 발생했습니다: {str(e)}'

# 이미지 삭제 함수
def delete_image(user_id, filename):
    try:
        # 사용자별 폴더 경로 설정
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
        file_path = os.path.join(upload_folder, filename)

        # 파일이 존재하는지 확인
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

        # 파일 삭제
        os.remove(file_path)

        return True, None  # 성공 시 True 리턴

    except FileNotFoundError as fnf_error:
        return False, str(fnf_error)

    except Exception as e:
        return False, f'파일 삭제 중 오류가 발생했습니다: {str(e)}'