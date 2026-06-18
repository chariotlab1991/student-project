# Running nanoGPT

This document contains the final step-by-step process used to run nanoGPT on a Linux machine.

In this setup:

* The virtual environment was already created.
* `pip` was already updated to the latest version.


---

## Step 1: Install Required Packages

First, install all required dependencies:

```bash
pip install torch numpy transformers datasets tiktoken wandb tqdm
```

---

## Step 2: Prepare the Shakespeare Dataset

Next, prepare the Shakespeare character-level dataset:

```bash
python data/shakespeare_char/prepare.py
```

This command creates the required training files inside:

```bash
data/shakespeare_char/
```

The generated files include:

```bash
train.bin
val.bin
meta.pkl
```

These files are required before training the model.

---

## Step 3: Train the nanoGPT Model

After preparing the dataset, train a small nanoGPT model on CPU:

```bash
python -u train.py config/train_shakespeare_char.py --device=cpu --compile=False --wandb_log=False --max_iters=100 --eval_interval=20 --log_interval=1 --batch_size=2 --block_size=32 --n_layer=2 --n_head=2 --n_embd=32
```

### Explanation of Important Flags

```bash
--device=cpu
```

Runs training on CPU instead of GPU.

```bash
--compile=False
```

Disables PyTorch compile mode, which is useful for simple CPU-based training.

```bash
--wandb_log=False
```

Disables Weights & Biases logging.

```bash
--max_iters=100
```

Runs training for 100 iterations.

```bash
--batch_size=2
```

Uses a small batch size suitable for low-RAM machines.

```bash
--block_size=32
```

Uses a smaller context length to reduce memory usage.

```bash
--n_layer=2 --n_head=2 --n_embd=32
```

Creates a very small GPT-style model that can run on a lightweight Linux machine.

After training, the model checkpoint is saved in:

```bash
out-shakespeare-char
```

---

## Step 4: Test the Trained Model

After training is complete, test the model using `sample.py`:

```bash
python sample.py --out_dir=out-shakespeare-char --device=cpu --compile=False --start="ROMEO:" --max_new_tokens=200
```

This command generates text starting from the prompt:

```text
ROMEO:
```

If this command generates output, the model is working successfully.

---

## Step 5: Replace `chat.py`

After confirming that `sample.py` works, replace the content of `chat.py` with the following code:

```python
import subprocess


def ask_llm(prompt: str) -> str:
    cmd = [
        "python",
        "sample.py",
        "--out_dir=out-shakespeare-char",
        "--device=cpu",
        "--compile=False",
        f"--start={prompt}",
        "--max_new_tokens=100",
        "--temperature=0.6",
        "--top_k=200",
    ]

    p = subprocess.run(cmd, capture_output=True, text=True)

    if p.returncode != 0:
        return "ERROR:\n" + p.stderr

    output = p.stdout.strip()

    lines = output.splitlines()
    clean_lines = []

    skip_prefixes = (
        "Overriding:",
        "number of parameters",
        "Loading meta",
        "No meta",
    )

    for line in lines:
        if line.startswith(skip_prefixes):
            continue
        if line.strip().startswith("----"):
            continue
        clean_lines.append(line)

    clean_output = "\n".join(clean_lines).strip()

    if not clean_output:
        return "(no output generated)"

    return clean_output


while True:
    msg = input("You> ").strip()

    if msg.lower() in ["exit", "quit"]:
        break

    if not msg:
        continue

    reply = ask_llm(msg)
    print("Bot>", reply)
```

---

## Step 6: Run `chat.py`

Finally, run:

```bash
python chat.py
```

Now you can enter prompts such as:

```text
ROMEO:
```

```text
KING:
```

```text
To be or not to be
```

The model will generate Shakespeare-style text based on the prompt.

---

## Important Note

This is not a real ChatGPT-like chatbot.

The model was trained on Shakespeare text, so it works as a text continuation model.

It works like this:

```text
Prompt → Shakespeare-style continuation
```

It does not work like this:

```text
Question → Intelligent answer
```

For example, this is a good prompt:

```text
ROMEO:
```

But this is not a good prompt for this model:

```text
What is AI?
```

To get better output, increase the number of training iterations later, for example:

```bash
--max_iters=500
```

or

```bash
--max_iters=1000
```


