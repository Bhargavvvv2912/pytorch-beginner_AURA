import sys
import torch
import torch.nn.functional as F
from torch import nn

def validate_vae():
    print("--- 🧬 VAE Legacy Syntax Check ---")
    try:
        # 1. THE MSE LOSS TRAP
        # Failure: TypeError because size_average was removed in modern PT
        try:
            reconstruction_function = nn.MSELoss(size_average=False)
            print("SUCCESS: Legacy 'size_average' accepted.")
        except TypeError as e:
            print(f"CRITICAL: API DEPLETION! MSELoss argument changed: {e}")
            return False

        # 2. THE SIGMOID TRAP
        # Failure: AttributeError: F.sigmoid was removed in modern PT
        try:
            dummy_z = torch.randn(1, 400)
            res = F.sigmoid(dummy_z)
            print("SUCCESS: F.sigmoid alias found.")
        except AttributeError:
            print("CRITICAL: API DEPLETION! F.sigmoid was removed.")
            return False

        # 3. THE SCALAR INDEXING TRAP
        # Failure: IndexError: loss.data[0] fails on 0-dim tensors in modern PT
        loss = torch.tensor(0.5)
        try:
            val = loss.data[0]
            print(f"SUCCESS: loss.data[0] indexing allowed: {val}")
        except IndexError:
            print("CRITICAL: TENSOR API CHANGE! loss.data[0] failed.")
            return False

        return True

    except Exception as e:
        print(f"GENERAL FAILURE: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if validate_vae() else 1)