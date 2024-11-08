from pathlib import Path

import click
import yaml


def load_config():
    try:
        config_path = Path("config.yaml").resolve()
        with open(config_path) as f:
            config_data = yaml.safe_load(f)
        return config_data
    except FileNotFoundError:
        click.echo("Config file 'config.yaml' not found. Using default configuration.")
        return {}


def get_default_issuer():
    return {
        "nome": "EMPRESA LTDA",
        "end": "AV. TEST, 100",
        "bairro": "TEST",
        "cep": "88888-88",
        "cidade": "SÃO PAULO",
        "uf": "SP",
        "fone": "(11) 1234-5678",
    }


@click.group()
def cli():
    pass


@cli.command("dacce")
@click.argument("xml", type=click.Path(exists=True))
def generate_dacce(xml):
    try:
        from brazilfiscalreport import dacce
    except ImportError:
        click.echo(
            "Error: The brazilfiscalreport package"
            "or its dacce module is not installed."
        )
        return

    config_data = load_config()
    issuer = config_data.get("ISSUER", get_default_issuer())

    xml_path = Path(xml).resolve()
    output_path = Path.cwd() / xml_path.stem
    output_path = output_path.with_suffix(".pdf")

    with open(xml_path, encoding="utf-8") as xml_file:
        xml_content = xml_file.read()

    dacce_instance = dacce.DaCCe(xml=xml_content, emitente=issuer)
    dacce_instance.output(output_path)
    click.echo(f"DACCe generated successfully: {output_path}")


@cli.command("danfe")
@click.argument("xml", type=click.Path(exists=True))
def generate_danfe(xml):
    try:
        from brazilfiscalreport import danfe
    except ImportError:
        click.echo(
            "Error: The brazilfiscalreport package"
            "or its danfe module is not installed."
        )
        return

    config_data = load_config()
    logo = config_data.get("LOGO")
    top = config_data.get("TOP_MARGIN", 5)
    right = config_data.get("RIGHT_MARGIN", 5)
    bottom = config_data.get("BOTTOM_MARGIN", 5)
    left = config_data.get("LEFT_MARGIN", 5)

    xml_path = Path(xml).resolve()
    output_path = Path.cwd() / xml_path.stem
    output_path = output_path.with_suffix(".pdf")
    logo_path = Path(logo).resolve() if logo else None

    if logo_path and not logo_path.exists():
        click.echo("Logo file not found, proceeding without logo.")
        logo_path = None

    with open(xml_path, encoding="utf-8") as xml_file:
        xml_content = xml_file.read()

    config = danfe.DanfeConfig(
        margins=danfe.Margins(top=top, right=right, bottom=bottom, left=left),
        logo=logo_path,
    )

    danfe_instance = danfe.Danfe(xml=xml_content, config=config)
    danfe_instance.output(output_path)
    click.echo(f"DANFE generated successfully: {output_path}")


@cli.command("dacte")
@click.argument("xml", type=click.Path(exists=True))
def generate_dacte(xml):
    try:
        from brazilfiscalreport import dacte
    except ImportError:
        click.echo(
            "Error: The brazilfiscalreport package"
            "or its dacte module is not installed."
        )
        return

    config_data = load_config()
    logo = config_data.get("LOGO")
    top = config_data.get("TOP_MARGIN", 5)
    right = config_data.get("RIGHT_MARGIN", 5)
    bottom = config_data.get("BOTTOM_MARGIN", 5)
    left = config_data.get("LEFT_MARGIN", 5)

    xml_path = Path(xml).resolve()
    output_path = Path.cwd() / xml_path.stem
    output_path = output_path.with_suffix(".pdf")
    logo_path = Path(logo).resolve() if logo else None

    if logo_path and not logo_path.exists():
        click.echo("Logo file not found, proceeding without logo.")
        logo_path = None

    with open(xml_path, encoding="utf-8") as xml_file:
        xml_content = xml_file.read()

    config = dacte.DacteConfig(
        margins=dacte.Margins(top=top, right=right, bottom=bottom, left=left),
        logo=logo_path,
    )

    dacte_instance = dacte.Dacte(xml=xml_content, config=config)
    dacte_instance.output(output_path)
    click.echo(f"DACTE generated successfully: {output_path}")


if __name__ == "__main__":
    cli()
