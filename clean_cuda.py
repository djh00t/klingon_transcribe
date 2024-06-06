import torch
import gc

# Define your variables
x = torch.randn(10000, 10000).to('cuda')
y = torch.randn(10000, 10000).to('cuda')

# Use the variables
z = x * y

# Delete the variables
del x
del y
del z

# Perform garbage collection
gc.collect()

# Clear the CUDA cache
torch.cuda.empty_cache()

# Check GPU memory status
print(torch.cuda.memory_allocated())
print(torch.cuda.memory_reserved())
