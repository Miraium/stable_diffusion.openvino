import os
import glob
import json
import time
import datetime
from multiple_generation import OUTPUT_ROOT

md_template = """
## {title}

Date: {date}

> {prompt}

{table}
"""

NUM_COLUMN = 5

def main():
    title_list = glob.glob(os.path.join(OUTPUT_ROOT,"*"))
    title_list.sort(reverse=True)
    # print(title_list)

    output_text = ""
    for title in title_list:
        image_list = glob.glob(os.path.join(title,"*.png"))
        image_list.sort()
        setting_json = glob.glob(os.path.join(title,"*.json"))

        date_str= os.path.basename(title.split('_')[0])
        dt = datetime.datetime.strptime(date_str, "%Y%m%d-%H-%M-%S")
        date_str = dt.strftime("%Y-%m-%d %H:%M:%S")

        with open(setting_json[0]) as f:
            obj = json.load(f)
            title = obj["title"]
            prompt = obj["prompt"]
            num_image = obj["num_output"]
            # print(title, prompt, num_image)

        table = "|" * NUM_COLUMN + "|\n"
        table += "|-" * NUM_COLUMN + "|\n"

        for i, image_path in enumerate(image_list):
            table += "|" + f"![]({image_path})"
            if i % NUM_COLUMN == NUM_COLUMN - 1:
                table += "|\n"
        
        output_text += md_template.format(title=title, date=date_str, prompt=prompt, table=table)

    with open("Gallery.md", 'w') as f:
        f.write(output_text)



if __name__ == "__main__":
    main()