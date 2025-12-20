from typing import Dict, Any, Union
import cloudinary.uploader
import logging


class Utils:

    logger = logging.getLogger(__name__)

    @staticmethod
    def upload_image(file_path_or_url: str, folder="restaurant") -> Union[str, None]:
        if not file_path_or_url:
            return None
        try:
            upload_result = cloudinary.uploader.upload(file_path_or_url, folder=folder)
            return upload_result.get("secure_url")
        except Exception as e:
            Utils.logger.error(f"Utils Cloudinary Error: {e}")
            return None
