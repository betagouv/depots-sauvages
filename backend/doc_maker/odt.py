from python_odt_template import ODTTemplate
from python_odt_template.jinja import get_odt_renderer

from backend.doc_maker import settings as doc_maker_settings


class ODTProcessor:
    """
    Process ODT templates
    """

    def __init__(self):
        self.renderer = get_odt_renderer(media_path=str(doc_maker_settings.TEMPLATE_DIR))
        self.ensure_dirs()

    def ensure_dirs(self):
        """Ensure directories exist"""
        doc_maker_settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def process_template(self, template_name, context, output_filename):
        """
        Process ODT template with given context
        """
        template_path = doc_maker_settings.TEMPLATE_DIR / template_name
        output_path = doc_maker_settings.OUTPUT_DIR / output_filename
        with ODTTemplate(template_path) as template:
            self.renderer.render(template, context=context)
            template.pack(output_path)
        return output_path
