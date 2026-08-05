<h1>
<p align="center">
RND1: Scaling Diffusion Language Models
</p>
</h1>

![???](https://github.com/user-attachments/assets/c2c54f94-a7f5-4b76-987d-f15de4efaef6)


This repository contains an inference harness for Radical Numerics Diffusion 1 (RND1), an experimental diffusion language model. RND1-Base-0910 is a 30B‑parameter sparse Mixture‑of‑Experts model with 3B active parameters per token, converted from an autoregressive base (Qwen3-30B-A3B) via continual pretraining on 500B tokens.

We release RND1 models to catalyze further research on inference and post-training of DLMs.

For more details, see:

**Blog:** https://www.radicalnumerics.ai/blog/rnd1

**Report:** https://www.radicalnumerics.ai/assets/rnd1_report.pdf

**🤗:** https://huggingface.co/radicalnumerics/RND1-Base-0910

**Models:**
 * **RND1-Base-0910**: first base model in the RND1 family. It has not been post-trained for specific usage.


## Installation

Using a Python 3.12 environment:
```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install -e .
```


## Quick Start



```bash
# Task mode (default) - for instructions, questions, or requests
python demo_rnd_generation.py --prompt "Write a Python function that finds the longest common subsequence of two strings. Include comments explaining the algorithm."

# Completion mode - for text continuation
python demo_rnd_generation.py --mode completion --prompt "The key to understanding quantum computing lies in"

# Sampling parameters
python demo_rnd_generation.py --top-k 50 --temperature 0.7 --prompt "Explain how neural networks learn in simple terms"
```



### Demo Parameters

- `--mode`: Generation mode - 'task' or 'completion' (default: task)
  - `task`: For instructions, questions, or requests (adds "Question:" prefix)
  - `completion`: For text continuation (no prefix added)
- `--max-new-tokens`: Number of new tokens to generate (default: 256)
- `--num-steps`: Diffusion denoising steps (default: 256)
- `--temperature`: Sampling temperature, 0.0 for greedy (default: 0.01)
- `--top-k`: Top-k filtering - keeps only k most likely tokens (works with greedy and sampling)
- `--top-p`: Nucleus filtering - keeps tokens with cumulative probability ≤ p (works with greedy and sampling)
- `--no-viz`: Disable visualization
- `--add-eos-at-end` / `--no-add-eos-at-end`: Add EOS token at the end of the sequence to force coherent endings (default: True)

## Python API

```python
from transformers import AutoTokenizer
from rnd import RND1LM

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("radicalnumerics/RND1-Base-0910", trust_remote_code=True)

# Load model
model = RND1LM.from_pretrained(
    "radicalnumerics/RND1-Base-0910",
    dtype="bfloat16",
    device_map="auto",
    trust_remote_code=True,
)

# Generate - Task mode (for instructions and questions)
prompt = "Write a Python function that finds the longest common subsequence of two strings. Include comments explaining the algorithm."
inputs = tokenizer(f"Question: {prompt}\nAnswer:", return_tensors="pt")
input_ids = inputs.input_ids.to(model.device)

# Generate
output = model.generate(
    inputs=input_ids,
    max_new_tokens=256,
    num_diffusion_steps=256,
    temperature=0.01,
)

# Decode only the generated part
text = tokenizer.decode(output[0], skip_special_tokens=True)
print(text)
```

## Citation

```bibtex
@article{rnd1_2025,
   title        = {RND1: Simple, Scalable AR-to-Diffusion Conversion},
   author       = {Chandrasegaran, Keshigeyan and Thomas, Armin W. and Ku, Jerome and Berto, Federico and Kim, Jae Myung and Brixi, Garyk and Nguyen, Eric and Massaroli, Stefano and Poli, Michael},
   year         = {2025},
   month        = {Oct},
   url          = {https://www.radicalnumerics.ai/blog/rnd1},
   organization = {Radical Numerics}
}
```


## Project Structure

```
RND1/
├── README.md                    # This file
├── demo_rnd_generation.py       # Demo script with command-line interface
└── rnd/                         # Core RND1 pa
…
