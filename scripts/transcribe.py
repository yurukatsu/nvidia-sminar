import json
import os
from pathlib import Path

from mistralai.client import Mistral
from typer import Typer

api_key = os.environ["MISTRAL_API_KEY"]
model = "voxtral-mini-latest"

client = Mistral(api_key=api_key)

app = Typer()

@app.command()
def transcribe(
    input_file: Path,
    output_dir: Path = Path("./data/output"),
):
    with input_file.open("rb") as f:
        transcription_response = client.audio.transcriptions.complete(
            model=model,
            file={
                "content": f,
                "file_name": input_file.name
            },
            language="ja",
            diarize=True,
            timestamp_granularities=["segment"]
        )

    output_file = output_dir / input_file.with_suffix(".json").name
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w") as f:
        json.dump(transcription_response.model_dump(), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    app()
