"""Video generation commands."""

import click

from sora_cli.core.client import get_client
from sora_cli.core.exceptions import SoraError
from sora_cli.core.output import (
    DEFAULT_MODEL,
    SORA_MODELS,
    print_error,
    print_json,
    print_video_result,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(SORA_MODELS),
    default=DEFAULT_MODEL,
    help="Sora model version.",
)
@click.option(
    "--orientation",
    type=click.Choice(["landscape", "portrait"]),
    default="landscape",
    help="Video orientation.",
)
@click.option(
    "--duration",
    type=int,
    default=5,
    help="Duration in seconds.",
)
@click.option(
    "--size",
    type=click.Choice(["480p", "720p", "1080p"]),
    default="480p",
    help="Video resolution size.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    orientation: str,
    duration: int,
    size: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt.

    PROMPT is a detailed description of what to generate.

    Examples:

      sora generate "A cinematic scene of a sunset over the ocean"

      sora generate "A cat playing with yarn" -m sora-2
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "prompt": prompt,
            "model": model,
            "callback_url": callback_url,
            "orientation": orientation,
            "duration": duration,
            "size": size,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except SoraError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("image-to-video")
@click.argument("prompt")
@click.option(
    "-i",
    "--image-url",
    "image_urls",
    required=True,
    multiple=True,
    help="Image URL(s) for reference. Can be specified multiple times.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(SORA_MODELS),
    default=DEFAULT_MODEL,
    help="Sora model version.",
)
@click.option(
    "--orientation",
    type=click.Choice(["landscape", "portrait"]),
    default="landscape",
    help="Video orientation.",
)
@click.option(
    "--duration",
    type=int,
    default=5,
    help="Duration in seconds.",
)
@click.option(
    "--size",
    type=click.Choice(["480p", "720p", "1080p"]),
    default="480p",
    help="Video resolution size.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def image_to_video(
    ctx: click.Context,
    prompt: str,
    image_urls: tuple[str, ...],
    model: str,
    orientation: str,
    duration: int,
    size: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from reference image(s).

    PROMPT describes the desired video. Provide one or more image URLs as reference.

    Examples:

      sora image-to-video "Animate this scene" -i https://example.com/photo.jpg

      sora image-to-video "Bring to life" -i img1.jpg -i img2.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_video(
            prompt=prompt,
            image_urls=list(image_urls),
            model=model,
            orientation=orientation,
            duration=duration,
            size=size,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except SoraError as e:
        print_error(e.message)
        raise SystemExit(1) from e
