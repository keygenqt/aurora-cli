import click

from aurora_cli.src.base.output import OutResultError, OutResult
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.prompt import TextPrompt


def model_select(
        models: [],
        select: bool,
        index: int | None
) -> OutResult:
    def has_index(i: int, arr: []) -> bool:
        return i < 0 or len(arr) <= i

    # At the same time index and select
    if select and index is not None:
        return OutResultError(TextError.index_and_select_at_the_same_time())
    # If empty
    if len(models) == 0:
        return OutResultError(TextError.validate_config_devices_not_found())
    # If select index
    if index is not None:
        if has_index(index - 1, models):
            return OutResultError(TextError.index_error())
        return OutResult(value=models[index - 1])
    # If not prompt select fist
    if not select:
        return OutResult(value=models[0])
    # Prompt
    index = click.prompt(TextPrompt.select_index(), type=int)
    # Check index
    if has_index(index - 1, models):
        return OutResultError(TextError.index_error())
    # Result
    return OutResult(value=models[index - 1])
