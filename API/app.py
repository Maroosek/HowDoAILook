from flask import Flask, request, jsonify
from ai_handler import get_clothing_description, choose_best_outfit, generate_outfit_image, generate_outfit_video
from flask_cors import CORS
from photo_handler import ImageMerger
import os

app = Flask(__name__)
CORS(app)


@app.route('/api/generate-outfit', methods=['POST'])
def generate_outfit():
    data = request.get_json()

    apiToken = data.get("apiKey")
    os.environ["REPLICATE_API_TOKEN"] = apiToken
    print(apiToken)

    sex = data.get("sex")
    selected_style = data.get("selectedStyle")
    print(sex, selected_style)
    shirts = data.get("shirts", [])
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


@app.route('/api/generate-outfit-video', methods=['POST'])
def generate_outfit_video_route():
    data = request.get_json()
    picture = data.get("picture")

    if not picture:
        return jsonify({"error": "Brak obrazu stroju"}), 400

    video = generate_outfit_video(picture)
    print(video)
    if hasattr(video, "url"):
        video_url = video.url
    elif hasattr(video, "path"):
        video_url = video.path
    elif isinstance(video, str):
        video_url = video
    else:
        video_url = str(video)

    return jsonify({"video_url": video_url})


@app.route('/api/test', methods=['GET'])
def test_connection():

    return jsonify({"message": "You are conneceted"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
