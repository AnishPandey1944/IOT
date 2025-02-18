import os
import logging

class FileProcessor:
    @staticmethod
    def read_file(file_path):
        """Reads content from a file with error handling"""
        try:
            if not os.path.exists(file_path):
                return {'status': 'error', 'message': 'File does not exist', 'data': None}
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return {'status': 'success', 'message': 'File read successfully', 'data': content}
        
        except PermissionError:
            error_msg = "Permission denied to read file"
            logging.error(error_msg)
            return {'status': 'error', 'message': error_msg, 'data': None}
        
        except Exception as e:
            error_msg = f"Error reading file: {str(e)}"
            logging.error(error_msg)
            return {'status': 'error', 'message': error_msg, 'data': None}

    @staticmethod
    def write_file(file_path, content):
        """Writes content to a file with error handling"""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
                return {'status': 'success', 'message': 'File written successfully', 'data': None}
        
        except PermissionError:
            error_msg = "Permission denied to write file"
            logging.error(error_msg)
            return {'status': 'error', 'message': error_msg, 'data': None}
        
        except Exception as e:
            error_msg = f"Error writing file: {str(e)}"
            logging.error(error_msg)
            return {'status': 'error', 'message': error_msg, 'data': None}

    @staticmethod
    def validate_file_type(file_path, valid_extensions):
        """Validates if file has an allowed extension"""
        _, ext = os.path.splitext(file_path)
        if ext.lower() in valid_extensions:
            return True
        return False