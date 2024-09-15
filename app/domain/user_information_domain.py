import re

class UserInformationDomain:
    
    @staticmethod
    def check_nickname(nickname):
        # 닉네임이 영어 소문자와 숫자로만 이루어졌는지 확인하는 정규 표현식
        pattern = r'^[a-z0-9]+$'

        # 닉네임 길이가 20자를 초과하면 False 반환
        if len(nickname) > 20:
            return False

        # 정규 표현식에 맞으면 True, 아니면 False 반환
        return bool(re.match(pattern, nickname))
