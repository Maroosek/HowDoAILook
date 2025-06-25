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
    best_outfit = choose_best_outfit(desc)
    img_url     = generate_outfit_image(best_outfit, merged_uri)

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
            "img_url": img_url,        # wygenerowana stylizacja (jak wcześniej)
            "img_merged": merged_uri,  # płótno z wgranymi zdjęciami
        })


    # image_base64 = data['image_base64']
    # mime_type = data.get('mime_type', 'image/png')
    # data_uri = f"data:{mime_type};base64,{image_base64}"
    #
    # desc = get_clothing_description(data_uri)
    # best_outfit = choose_best_outfit(desc)
    # img_url = generate_outfit_image(best_outfit, data_uri)
    #
    # if hasattr(img_url, "url"):
    #     img_url = img_url.url
    # elif hasattr(img_url, "path"):
    #     img_url = img_url.path
    # elif not isinstance(img_url, str):
    #     img_url = str(img_url)
    #
    # return jsonify({
    #     "desc": desc,
    #     "best_outfit": best_outfit,
    #     "img_url": img_url
    # })


if __name__ == "__main__":
    app.run(port=5000, debug=True)
