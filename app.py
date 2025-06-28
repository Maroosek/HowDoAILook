import base64
from flask import Flask, request, jsonify
from ai_handler import get_clothing_description, choose_best_outfit, generate_outfit_image
from flask_cors import CORS
from photo_handler import ImageMerger
app = Flask(__name__)
CORS(app)

@app.route('/api/generate-outfit', methods=['POST'])
def generate_outfit():
    data = request.get_json()

    sex = data.get("sex")
    selected_style = data.get("selectedStyle")
    print(sex, selected_style)
    shirts = data.get("shirt", [])
    pants  = data.get("pants", [])
    shoes  = data.get("shoes", [])

    if not any([shirts, pants, shoes]) and "image_base64" in data:
        mime = data.get("mime_type", "image/png")
        shirts = [f"data:{mime};base64,{data['image_base64']}"]

    if not shirts and not pants:
        return jsonify({"error": "Brak obrazów top/bottom"}), 400

    merged_uri = ImageMerger.merge_rows(shirts, pants, shoes)

    desc        = get_clothing_description(merged_uri)
    best_outfit = choose_best_outfit(desc, sex, selected_style)
    img_url     = generate_outfit_image(best_outfit, merged_uri, sex, selected_style)

    if hasattr(img_url, "url"):
        img_url = img_url.url
    elif hasattr(img_url, "path"):
        img_url = img_url.path
    elif not isinstance(img_url, str):
        img_url = str(img_url)

    return jsonify(
        {
            "desc": desc,
            "best_outfit": best_outfit,
            "img_url": img_url,
            "img_merged": merged_uri,
        })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
