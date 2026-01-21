import importlib.util

packages = [
    "unsloth",
    "torch",
    "datasets",
    "trl",
    "transformers",
    "peft",
    "bitsandbytes",
    "accelerate",
    "xformers",
    "sentencepiece",
    "protobuf",
    "huggingface_hub",
]

installed = []
missing = []

for pkg in packages:
    if importlib.util.find_spec(pkg) is not None:
        installed.append(pkg)
    else:
        missing.append(pkg)

print("✅ Installed packages:")
for p in installed:
    print(f"  - {p}")

print("\n❌ Missing packages:")
for p in missing:
    print(f"  - {p}")
