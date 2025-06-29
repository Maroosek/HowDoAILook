import replicate

def get_clothing_description(data_uri):
    print(f"inside get_clothing_desc")
    output = replicate.run(
        "lucataco/qwen-vl-chat:50881b153b4d5f72b3db697e2bbad23bb1277ab741c5b52d80cd6ee17ea660e9",
        input={
            "image": data_uri,
            "prompt": (
                "List all the clothing items visible in this photo. For each item, specify if it is a 'top' or a 'bottom', "
                "and describe its color with a lot of details, pattern, and any visible logos or details. List each item on a separate line. "
                "If it's t-shirt use 'T-Shirt', if jeans are baggie use 'Baggie jeans'."
            )
        }
    )
    print("qwen-vl-chat passed")
    return output

def choose_best_outfit(clothing_list, sex_param, style_param):
    print(f"inside choose_best_outfit")
    prompt_for_next = (
        f"{clothing_list}\nSelect the best outfit from the listed items using this style: Use style this style: {style_param} and this genred: {sex_param}. Return only one combination (one top and one bottom) and explain your choice. "
        f"Do not explain, use this format, example: 'Top: white shirt, bottom: jeans'. "
    )

    input2 = {
        "prompt": prompt_for_next,
        "max_new_tokens": 512,
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n"
                           "\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    }

    ansToSend = ""
    for event in replicate.stream(
        "meta/meta-llama-3-8b-instruct",
        input=input2,
    ):
        ansToSend += str(event)
    return ansToSend

def generate_outfit_image(ansToSend, data_uri, sex_param, style_param):
    print(f"inside generate_outfit_image")
    prompt_flux = (
        f"A photorealistic, full-body photo of a {sex_param} model wearing this clothes: {ansToSend} from the input_image. S"
        f"tyle of the photo is {style_param}. No other clothes or accessories. White background."
    )

    input3 = {
        "prompt": prompt_flux,
        "input_image": data_uri,
        "output_format": "jpg"
    }

    output_img = replicate.run(
        "black-forest-labs/flux-kontext-pro",
        input=input3
    )
    print("image generated")
    return output_img

def generate_outfit_video(output_img):
    print(f"inside generate_outif_video")
    prompt_flux = (
        "Create a highly photorealistic image of the person from the input photo posing confidently on a fashion runway, "
        "like a top model during a fashion show finale. Show a stylish, dynamic fashion pose, with one hand on the hip or a creative pose, "
        "head held high, strong posture. Use dramatic runway lighting, professional fashion show background, and elegant atmosphere. "
        "Make it look like a real high-fashion catwalk photo, with the person's face and style from the input photo. Vogue magazine style."
    )

    input4 = {
        "prompt": prompt_flux,
        "image": output_img,
        "resolution": "480p",
        "duration": 5,
        "aspect_ratio": "16:9",
        "fps": 24,
    }

    output = replicate.run(
        "bytedance/seedance-1-pro",
        input=input4,
    )

    with open("output.mp4", "wb") as file:
        file.write(output.read())

    return output


