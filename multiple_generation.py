import argparse
import os
import json
import time
import subprocess

OUTPUT_ROOT = "output"
BASE_COMMAND = 'python demo.py --output "{output_path}" --prompt "{prompt}"'


def main(setting):
    with open(setting) as f:
        json_obj = json.load(f)

    os.makedirs(OUTPUT_ROOT, exist_ok=True)

    products = json_obj["products"]

    for product in products:
        title = product["title"]
        prompt = product["prompt"]
        num_output = product["num_output"]

        curr_time = time.strftime("%Y%m%d-%H-%M-%S")
        product_dir = os.path.join(OUTPUT_ROOT, f"{curr_time}_{title}")
        os.makedirs(product_dir, exist_ok=True)

        setting_backup = os.path.join(product_dir, setting)
        with open(setting_backup, 'w') as f:
            json.dump(product, f)

        for i in range(num_output):
            image_name = f"{i:03d}.png"
            output_path = os.path.join(product_dir, image_name)
            command = BASE_COMMAND.format(output_path=output_path, prompt=prompt)
            print(command)
            subprocess.run(command, shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--setting", default="setting.json")
    args = parser.parse_args()
    main(args.setting)