import openai
import os
import logging

class GPTHandler:
    def __init__(self, api_key=None):
        self.api_key ='#OPENAI API KEY' or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required for GPT operations")
        
        openai.api_key = self.api_key

    def generate_response(self, prompt, model="gpt-3.5-turbo", max_tokens=1000):
        """Generates a GPT response for the given prompt"""
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return {
                'status': 'success',
                'message': 'Response generated successfully',
                'data': response.choices[0].message['content'].strip()
            }
        
        except openai.error.AuthenticationError:
            error_msg = "Invalid API key or authentication error"
            logging.error(error_msg)
            return {'status': 'error', 'message': error_msg, 'data': None}
        
        except openai.error.RateLimitError:
            error_msg = "API rate limit exceeded"
            logging.error(error_msg)
            return {'status': 'error', 'message': error_msg, 'data': None}
        
        except Exception as e:
            error_msg = f"GPT API error: {str(e)}"
            logging.error(error_msg)
            return {'status': 'error', 'message': error_msg, 'data': None}

    @staticmethod
    def format_prompt(base_prompt, user_input, file_content=None):
        """Formats a complete prompt with optional file content"""
        if file_content:
            return f"{base_prompt}\n\nFile Content:\n{file_content}\n\nUser Input: {user_input}"
        return f"{base_prompt}\n\nUser Input: {user_input}"
