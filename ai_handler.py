import replicate

def get_clothing_description(data_uri):
    print(f"inside get_clothing_desc {data_uri}")
    output = replicate.run(
        "lucataco/qwen-vl-chat:50881b153b4d5f72b3db697e2bbad23bb1277ab741c5b52d80cd6ee17ea660e9",
        input={
            "image": data_uri,
            "prompt": (
                "List all the clothing items visible in this photo. For each item, specify if it is a 'top' or a 'bottom', and describe its color with a lot of details, pattern, and any visible logos or details. List each item on a separate line."
            )
        }
    )
    print("5.2")
    return output

def choose_best_outfit(clothing_list):
    prompt_for_next = (
        f"{clothing_list}\nSelect the best outfit from the listed items. Return only one combination (one top and one bottom) and explain your choice. Do not explain, use this format, example: 'Top: white shirt, bottom: jeans'"
    )

    input2 = {
        "prompt": prompt_for_next,
        "max_new_tokens": 512,
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    }

    ansToSend = ""
    for event in replicate.stream(
        "meta/meta-llama-3-8b-instruct",
        input=input2,
    ):
        ansToSend += str(event)
    return ansToSend

def generate_outfit_image(ansToSend, data_uri):
    prompt_flux = (
        f"A photorealistic, full-body photo of a male model wearing this clothes: {ansToSend} from the input_image. No other clothes or accessories. White background."
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
    return output_img
