from pathlib import Path


def render_html(title: str, briefing: str, position_rows: str, technical_summary: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <style>
      body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 24px; background: #f8f9fb; }}
      h1, h2 {{ color: #1f2937; }}
      section {{ background: white; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
      pre {{ white-space: pre-wrap; word-break: break-word; }}
      table {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
      th, td {{ border: 1px solid #d1d5db; padding: 10px; text-align: left; }}
      th {{ background: #eff6ff; }}
    </style>
  </head>
  <body>
    <h1>{title}</h1>
    <section>
      <h2>Natural Language Briefing</h2>
      <pre>{briefing}</pre>
    </section>
    <section>
      <h2>Open Positions</h2>
      {position_rows}
    </section>
    <section>
      <h2>Technical Summary</h2>
      <pre>{technical_summary}</pre>
    </section>
  </body>
</html>
"""


def write_dashboard(output_path: Path, title: str, briefing: str, position_rows: str, technical_summary: str):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    html = render_html(title, briefing, position_rows, technical_summary)
    output_path.write_text(html, encoding="utf-8")
