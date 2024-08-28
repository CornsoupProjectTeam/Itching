from flask import Blueprint

# 블루프린트 가져오기
from .payments import payments_bp

__all__ = ["payments_bp"]
