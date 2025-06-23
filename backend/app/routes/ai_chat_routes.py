from flask import Blueprint, request, jsonify, current_app
import requests
import json

ai_chat_bp = Blueprint('ai_chat', __name__, url_prefix='/ai-chat')

@ai_chat_bp.route('/chat', methods=['POST'])
def chat():
    """
    AI Chat endpoint using Ollama with configurable model
    Expects JSON with 'message' field
    Returns AI response from Ollama
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        user_message = data['message']
        model_name = current_app.config.get("OLLAMA_MODEL", "llama3.1:8b")
        
        # Ollama API endpoint - using Docker service name
        ollama_url = "http://ollama:11434/api/generate"
        
        # Prepare the request payload for Ollama
        payload = {
            "model": model_name,
            "prompt": user_message,
            "stream": False
        }
        
        # Make request to Ollama
        response = requests.post(ollama_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            ai_response = response.json()
            return jsonify({
                "response": ai_response.get('response', ''),
                "model": model_name
            }), 200
        else:
            return jsonify({
                "error": f"Ollama API error: {response.status_code}",
                "details": response.text
            }), 500
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Cannot connect to Ollama. Make sure Ollama is running on ollama:11434"
        }), 503
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Request to Ollama timed out"
        }), 504
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500

@ai_chat_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify Ollama connection
    """
    try:
        response = requests.get("http://ollama:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [model.get('name', '') for model in models]
            current_model = current_app.config.get("OLLAMA_MODEL", "llama3:8b")
            
            return jsonify({
                "status": "healthy",
                "ollama_connected": True,
                "current_model": current_model,
                "model_loaded": current_model in model_names,
                "available_models": model_names
            }), 200
        else:
            return jsonify({
                "status": "unhealthy",
                "ollama_connected": False,
                "error": f"Ollama returned status {response.status_code}"
            }), 503
    except requests.exceptions.ConnectionError:
        return jsonify({
            "status": "unhealthy",
            "ollama_connected": False,
            "error": "Cannot connect to Ollama"
        }), 503
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "ollama_connected": False,
            "error": str(e)
        }), 500 