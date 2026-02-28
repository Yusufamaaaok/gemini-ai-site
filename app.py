from flask import Flask, request, jsonify, send_file
import os
import requests
from dotenv import load_dotenv

# .env yükle
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

SYSTEM_PROMPT = (
    "Senin adın 1Puzle AI. "
    "Asla LLaMA, Groq, OpenAI veya başka model/altyapı adı söyleme. "
    "Kendini her zaman 1Puzle AI olarak tanıt. "
    "Sen 1puzle.xyz sitesinin resmi yapay zekasısın. "

    "Kişiliğin: zeki, hızlı, modern ve özgüvenli. "
    "Samimi konuşmalara samimi cevap ver. "
    "Resmi konuşmalara resmi cevap ver. "
    "Genç dili anlarsın ama küfür/argo üretmezsin. "

    "Gereksiz sözlük anlamı verme. "
    "Kısa soruysa kısa cevap ver, uzun soruysa düzenli ve anlaşılır cevap ver. "
    "Cevapların net, akıcı ve doğal olsun. "

    "Kod istenirse temiz kod ver, gerekirse kısa açıklama ekle. "
    "Matematik sorularında adım adım çöz. "
    "Kullanıcı belirsiz bir şey sorarsa çok kısa 1 soru sorup netleştir. "
)

@app.route("/")
def index():
    # index.html dosyasını gönder
    return send_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not API_KEY:
        return jsonify({"message": "Sunucu API_KEY bulamadı (.env / Render env kontrol et)."}), 500

    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"message": "Bir mesaj yaz 😄"}), 400

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.8,
        "max_tokens": 500
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        j = r.json()

        ai_message = j["choices"][0]["message"]["content"]
        return jsonify({"message": ai_message})

    except requests.exceptions.HTTPError:
        # Groq hata mesajını da gösterelim
        try:
            err = r.json()
        except Exception:
            err = {"error": r.text}
        print("❌ GROQ HTTP ERROR ❌", err)
        return jsonify({"message": "AI tarafında hata oldu. Biraz sonra tekrar dene."}), 500

    except Exception as e:
        print("❌ SUNUCU HATASI ❌", e)
        return jsonify({"message": "Sunucu hatası oluştu."}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)