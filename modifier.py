import torch
import subprocess
import argparse
import sys
import io
import time
from PIL import Image
from diffusers import StableDiffusionInpaintPipeline

parser = argparse.ArgumentParser()
 
parser.add_argument("-p", "--prompt", default = "greeb dress, high resolution", help = "text description")
parser.add_argument("-i", "--image", help = "path to original photo")
parser.add_argument("-m", "--mask", help = "path to mask photo")
parser.add_argument("-o", "--outdir", default = './', help = "save path")
parser.add_argument("-a", "--amount", default = 1, help = "amount of generated photos")
parser.add_argument("-s", "--steps", default = 30, help = "amount of changing steps")
 
args = parser.parse_args()
 
original = Image.open(args.image)
mask_image = Image.open(args.mask)

def generate(photo, mask):
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting", 
        revision = "fp16", 
        torch_dtype = torch.float16
    )
    pipe.to("cuda") 
    pipe.safety_checker = None
    pipe.requires_safety_checker = False

    return pipe(
        prompt = args.prompt, 
        image = photo,
        mask_image = mask, 
        num_inference_steps = int(args.steps),
        num_images_per_prompt = int(args.amount)
    ).images

for i, image in enumerate(generate(original, mask_image)):
    image = image.resize(original.size)

    image.save('source.jpg')
    mask_image.convert('RGB').save('mask.jpg')
    original.save('original.jpg')

    try:
        start_time = time.time()
        stdout = subprocess.check_output("java -jar converter/fast-convert.jar", shell = True, stderr = subprocess.STDOUT)
        
        if int(args.amount) == 1:
            sys.stdout.buffer.write(stdout)
        else:
            print(f"Saving photo #{i + 1}: %s" % (time.time() - start_time))
            Image.open(io.BytesIO(stdout)).save(f'{args.outdir}generated-image-{i + 1}.jpg')
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))