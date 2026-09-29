"""FAL vs Higgsfield test round for the new photo direction (owner: current photos read "stocky / outdated").

2 scenes x 3 looks x 5 models = 30 renders, the SAME prompt text per scene+look for every model:
  fal:        Nano Banana Pro (fal-ai/nano-banana-pro, $0.15)   Seedream 4.5 (fal-ai/bytedance/seedream/v4.5/text-to-image, $0.04)
  Higgsfield: Soul (higgsfield-ai/soul/standard, ~$0.19 @1080p)  Soul V2 (higgsfield-ai/soul/v2/standard, ~$0.004)
              Marketing Studio 2.5 Flare direct (marketing-studio/image/flare, token-metered)
Writes compare/fal-jobs.json and compare/hf-jobs.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, "compare"), exist_ok=True)

SCENES = {
    "lowback": ("a patient lies face down on a padded treatment table, the whole body on the table and continuous from "
                "head to feet with the legs under a light blanket, the lower back bare; a white stand-mounted low-level "
                "laser head on an articulated arm is positioned a hand's width above the lower back, projecting three "
                "thin red laser lines across the skin without touching it; the practitioner's hand rests lightly on the "
                "patient's upper back."),
    "mtest": ("a manual muscle test: a patient sits upright on the edge of a treatment table and holds one arm straight "
              "out to the side at shoulder height; the practitioner stands beside them, one flat hand pressing gently "
              "down just above the patient's wrist and the other hand steadying the patient's shoulder."),
}
OVERLAY = {
    "lowback": "the lumbar vertebrae, the sacrum and the pelvis",
    "mtest": "the shoulder joint, the shoulder blade and the muscles of the raised arm",
}
LOOKS = {
    "cinematic": lambda s: ("Premium cinematic editorial photograph. A dark, moody treatment room in deep slate-blue and "
                            "teal tones; a single soft key light from above sculpting the body, a subtle rim light, deep "
                            "shadows that keep their detail" + ("; the red laser light glowing in the dim room" if s == "lowback" else "")
                            + "; matte-white modern equipment; shallow depth of field, 50mm lens, rich color grade, fine "
                            "film grain. It looks like a luxury health-technology brand campaign, not stock photography."),
    "overlay": lambda s: ("Premium editorial photograph in a clean, modern treatment room with soft directional light, "
                          "with a luminous augmented-reality anatomy overlay: " + OVERLAY[s] + " drawn in delicate glowing "
                          "teal engraving lines exactly where they sit under the skin, crisp and precise, like a living "
                          "anatomical plate. It looks like a luxury health-technology brand campaign, not stock photography."),
    "bright": lambda s: ("Bright contemporary editorial photograph in an architect-designed clinic: warm white plaster "
                         "walls, pale oak, sage linen, a large steel-framed window, crisp morning sunlight casting clean "
                         "defined shadows; modern equipment; a natural, unposed moment; confident composition with "
                         "negative space; crisp detail and fresh, true-to-life color. It looks like a high-end magazine "
                         "feature, not stock photography."),
}
PEOPLE = (" The practitioner is a man in a white dress shirt with the sleeves rolled, framed so that his head is out of "
          "the frame (from the chest down, or only his hands and forearms). The patient is a real-looking adult in simple "
          "contemporary clothing; the patient's face may be seen in soft profile, relaxed. Anatomically correct: every "
          "body complete and continuous, the correct number of arms, legs, hands and fingers. No text, logos or labels "
          "anywhere.")


def prompt(scene, look):
    return LOOKS[look](scene) + " Scene: " + SCENES[scene] + PEOPLE


fal_jobs, hf_jobs = [], []
for scene in SCENES:
    for look in LOOKS:
        p = prompt(scene, look)
        fal_jobs.append({"name": f"{scene}-{look}-fal-nbp", "endpoint": "fal-ai/nano-banana-pro", "prompt": p,
                         "params": {"aspect_ratio": "3:2", "resolution": "2K", "output_format": "png"}})
        fal_jobs.append({"name": f"{scene}-{look}-fal-seedream45", "endpoint": "fal-ai/bytedance/seedream/v4.5/text-to-image",
                         "prompt": p, "params": {"image_size": {"width": 2400, "height": 1600}}})
        hf_jobs.append({"name": f"{scene}-{look}-hf-soul", "model": "higgsfield-ai/soul/standard",
                        "input": {"prompt": p, "aspect_ratio": "3:2", "resolution": "1080p"}})
        hf_jobs.append({"name": f"{scene}-{look}-hf-soulv2", "model": "higgsfield-ai/soul/v2/standard",
                        "input": {"prompt": p, "aspect_ratio": "3:2"}})
        hf_jobs.append({"name": f"{scene}-{look}-hf-flare", "model": "marketing-studio/image/flare",
                        "input": {"prompt": p, "quality": "high", "moderation": "auto", "resolution": "2k",
                                  "aspect_ratio": "3:2", "enhance_prompt": False}})
json.dump(fal_jobs, open(os.path.join(HERE, "compare", "fal-jobs.json"), "w"), indent=1)
json.dump(hf_jobs, open(os.path.join(HERE, "compare", "hf-jobs.json"), "w"), indent=1)
print(f"{len(fal_jobs)} fal jobs, {len(hf_jobs)} Higgsfield jobs")
print("sample prompt:", prompt("lowback", "cinematic"))
