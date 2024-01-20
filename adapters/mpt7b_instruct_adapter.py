import transformers
import torch

def mpt7b_configuraton():
    name = 'mosaicml/mpt-7b-instruct'

    config = transformers.AutoConfig.from_pretrained(name, trust_remote_code=True)
    config.attn_config['attn_impl'] = 'triton'
    config.init_device = 'cuda:0' # For fast initialization directly on GPU!
    config.max_seq_len = 4096 # For long sequences, ALiBi enables us to increase maximum sequence length, though the model was trained with a sequence length of 2048

    model = transformers.AutoModelForCausalLM.from_pretrained(
    name,
    config=config,
    torch_dtype=torch.bfloat16, # Load model weights in bfloat16
    trust_remote_code=True
    )

    tokenizer = transformers.AutoTokenizer.from_pretrained(name)

    return model, tokenizer
