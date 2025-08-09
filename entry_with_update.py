import os
import sys
import json

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)


try:
    import pygit2
    pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)

    repo = pygit2.Repository(os.path.abspath(os.path.dirname(__file__)))

    branch_name = repo.head.shorthand

    remote_name = 'origin'
    remote = repo.remotes[remote_name]

    remote.fetch()

    local_branch_ref = f'refs/heads/{branch_name}'
    local_branch = repo.lookup_reference(local_branch_ref)

    remote_reference = f'refs/remotes/{remote_name}/{branch_name}'
    remote_commit = repo.revparse_single(remote_reference)

    merge_result, _ = repo.merge_analysis(remote_commit.id)

    if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
        print("Already up-to-date")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
        local_branch.set_target(remote_commit.id)
        repo.head.set_target(remote_commit.id)
        repo.checkout_tree(repo.get(remote_commit.id))
        repo.reset(local_branch.target, pygit2.GIT_RESET_HARD)
        print("Fast-forward merge")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
        print("Update failed - Did you modify any file?")
except Exception as e:
    print('Update failed.')
    print(str(e))

print('Update succeeded.')
config_file = "config.txt"

# Step 1: Read the existing config
with open(config_file, "r") as file:
    config = json.load(file)

# Step 2: Update / Add new values
config["path_outputs"] = "/content/drive/MyDrive/Fooocus/outputs"

config["available_aspect_ratios"] = [
    "640*480", "1280*720", "1920*1080", "2560*1440", "3840*2160",
    "480*640", "720*1280", "1080*1920", "1440*2560", "2160*3840",
    "480*480", "720*720", "1080*1080", "1440*1440", "2160*2160",
    "1024*1024"
]

config["default_aspect_ratio"] = "720*1280"

config["default_prompt_negative"] = (
    "bindi, tilaka, earrings, nose ring, piercings, heavy makeup, wrinkles, freckles, "
    "blemishes, old woman, blurry, low resolution, face partially visible, shadow on face, "
    "sunglasses, hat, distorted face, artistic filter, exaggerated features"
)

config["default_prompt"] = (
    "A close-up portrait of a 28-year-old Sri Lankan girl with smooth fair-olive skin, "
    "deep shiny black eyes, straight black hair, and soft fair-colored lips. Her full face "
    "is clearly visible from forehead to neck. She is looking directly at the camera. No "
    "makeup, clean natural look, soft natural lighting, a plain background, high resolution, "
    "Instagram influencer style, and professional studio photography."
)

# Step 3: Write updated config back to file
with open(config_file, "w") as file:
    json.dump(config, file, indent=4)

print("Config updated successfully!")
from launch import *
