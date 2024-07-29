import pathlib

import click

from pegasus.templates import render_template_pack


def validate_name(ctx, param, value):
    if not value.isidentifier():
        raise click.BadParameter(
            f"'{value}' is not a valid app name. Please make sure it is a valid identifier."
        )
    return value


@click.command(name="startapp")
@click.argument("name", callback=validate_name)
@click.argument(
    "directory",
    envvar="APP_DIRECTORY",
    type=click.Path(file_okay=False, exists=True, resolve_path=True),
    default=".",
)
def startapp(name, directory):
    """Creates a Django app directory structure for the given app name in
    the current directory or optionally in the given directory.

    NAME is the name of the Django app
    DIRECTORY is the path of the directory to create the app in. Defaults to the current directory.
    """
    app_dir = pathlib.Path(directory) / name
    if not app_dir.exists():
        app_dir.mkdir()
    elif any(app_dir.iterdir()):
        raise click.ClickException(f"target directory must be empty: {app_dir}")

    context = {
        "app_name": name,
        "camel_case_app_name": "".join(x for x in name.title() if x != "_"),
    }
    render_template_pack("app_template", app_dir, context)
