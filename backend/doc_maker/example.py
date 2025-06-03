from .odt import ODTProcessor


def generate_test_document():
    processor = ODTProcessor()

    # Test context
    context = {"administration": "test bal"}

    return processor.process_template(
        template_name="template-doc-constat.odt", context=context, output_filename="pv1.odt"
    )
