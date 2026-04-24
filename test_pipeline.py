import os
from dotenv import load_dotenv
load_dotenv(override=True)

from utils.helpers import run_pipeline

output, evaluation, steps_log = run_pipeline("to include timer from different timezone in my app")

print("OUTPUT:")
print(output)
print("\nEVALUATION:")
print(evaluation)
print("\nSTEPS LOG:")
print(steps_log)
