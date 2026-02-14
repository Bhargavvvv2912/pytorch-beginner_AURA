import sys
import torch
import torch.nn.functional as F
from torch import nn

def validate_vae():
    print("--- 🧬 VAE Legacy Syntax Check ---")
    try:
        # 1. THE SCALAR INDEXING TRAP (Removed in PT 2.x)
        # This works in PT 1.7.1 but crashes in PT 2.6
        loss = torch.tensor(0.5)
        try:
            val = loss.data[0]
            print(f"SUCCESS: loss.data[0] indexing allowed.")
        except IndexError:
            print("CRITICAL: TENSOR API CHANGE! loss.data[0] failed.")
            return False

        # 2. THE SIGMOID TRAP (Removed in PT 2.x)
        try:
            dummy_z = torch.randn(1, 10)
            res = F.sigmoid(dummy_z)
            print("SUCCESS: F.sigmoid alias found.")
        except AttributeError:
            print("CRITICAL: API DEPLETION! F.sigmoid was removed.")
            return False

        # 3. THE PILLOW ANTIALIAS TRAP
        # Author code often uses Image.ANTIALIAS (Removed in Pillow 10.0)
        from PIL import Image
        try:
            alias = Image.ANTIALIAS
            print("SUCCESS: Pillow legacy constants found.")
        except AttributeError:
            print("CRITICAL: PILLOW ROT! Image.ANTIALIAS was removed.")
            return False

        return True

    except Exception as e:
        print(f"GENERAL FAILURE: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if validate_vae() else 1)