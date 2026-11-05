#!/usr/bin/env python3
"""
Script d'extraction et de structuration documentaire pour le Chatbot Stop Dépôt Sauvage.
Sources gérées :
1. Modèles ODT officiels (backend/doc_maker/doc_templates/*.odt) -> Markdown
2. FAQ et Articles Blog (extraits de la prod Scalingo) -> Markdown nettoyé et structuré
"""

import json
import os
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "backend" / "chatbot" / "knowledge"
ODT_TEMPLATES_DIR = BASE_DIR / "backend" / "doc_maker" / "doc_templates"
RAW_DUMP_FILE = KNOWLEDGE_DIR / "raw" / "prod_dump_faq_blog.json"


def html_to_markdown(html_text: str) -> str:
    """Nettoie le HTML riche TipTap / Wagtail en Markdown lisible."""
    if not html_text:
        return ""
    text = html_text
    # Headers
    text = re.sub(r"<h1[^>]*>(.*?)</h1>", r"# \1\n\n", text, flags=re.DOTALL)
    text = re.sub(r"<h2[^>]*>(.*?)</h2>", r"## \1\n\n", text, flags=re.DOTALL)
    text = re.sub(r"<h3[^>]*>(.*?)</h3>", r"### \1\n\n", text, flags=re.DOTALL)
    text = re.sub(r"<h4[^>]*>(.*?)</h4>", r"#### \1\n\n", text, flags=re.DOTALL)
    # Lists
    text = re.sub(r"<li[^>]*><p>(.*?)</p></li>", r"- \1\n", text, flags=re.DOTALL)
    text = re.sub(r"<li[^>]*>(.*?)</li>", r"- \1\n", text, flags=re.DOTALL)
    text = re.sub(r"</?ul[^>]*>", "\n", text)
    text = re.sub(r"</?ol[^>]*>", "\n", text)
    # Paragraphs & line breaks
    text = re.sub(r"<p[^>]*>(.*?)</p>", r"\1\n\n", text, flags=re.DOTALL)
    text = re.sub(r"<br\s*/?>", "\n", text)
    # Formatting
    text = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", text, flags=re.DOTALL)
    text = re.sub(r"<em[^>]*>(.*?)</em>", r"*\1*", text, flags=re.DOTALL)
    # Links: [text](href)
    text = re.sub(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", text, flags=re.DOTALL)
    # Strip remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Decode basic entities
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    # Clean up excessive newlines & trailing spaces
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_odt_to_markdown(odt_path: Path, output_md_path: Path):
    """Extrait le contenu texte structuré d'un fichier .odt."""
    print(f"Extraction ODT: {odt_path.name} -> {output_md_path.name}")
    try:
        with zipfile.ZipFile(odt_path) as z:
            content_xml = z.read("content.xml")
            tree = ET.fromstring(content_xml)
            
            # Namespaces ODT
            ns = {
                "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
                "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
            }
            
            lines = []
            for elem in tree.iter():
                tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
                if tag in ("p", "h"):
                    full_text = "".join(elem.itertext()).strip()
                    if full_text:
                        # Si c'est un header
                        if tag == "h":
                            lines.append(f"\n## {full_text}\n")
                        else:
                            lines.append(full_text)
            
            full_content = "\n\n".join(lines)
            # Nettoyer les espaces multiples
            full_content = re.sub(r"[ \t]+", " ", full_content)
            full_content = re.sub(r"\n{3,}", "\n\n", full_content)
            
            header = f"# Modèle officiel : {odt_path.stem.upper()}\n"
            header += f"> Source : `{odt_path.name}` (modèle de document généré par Stop Dépôt Sauvage)\n\n"
            
            output_md_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_md_path, "w", encoding="utf-8") as f:
                f.write(header + full_content + "\n")
    except Exception as e:
        print(f"Erreur lors de l'extraction de {odt_path}: {e}")


def process_dump_data():
    """Traite les FAQ et les articles de blog depuis le dump de prod."""
    if not RAW_DUMP_FILE.exists():
        print(f"Dump introuvable: {RAW_DUMP_FILE}")
        return

    with open(RAW_DUMP_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Traitement des FAQ
    faq_items = [d for d in data if d["model"] == "faq.faqitem"]
    categories = {item["pk"]: item["fields"]["title"] for item in faq_items if item["fields"].get("is_top_level")}
    
    faq_by_category = {}
    for item in faq_items:
        fields = item["fields"]
        if fields.get("is_top_level"):
            continue
        parent_id = fields.get("parent")
        category_title = categories.get(parent_id, "Questions Générales")
        # Nettoyage catégorie pour nom de fichier
        cat_slug = re.sub(r"[^\w\-]", "_", category_title).strip("_").lower()
        cat_slug = re.sub(r"_+", "_", cat_slug)
        
        question = fields.get("title", "")
        content_blocks = fields.get("content", [])
        answer_parts = []
        for block in content_blocks:
            if isinstance(block, dict) and block.get("type") == "rich_text":
                answer_parts.append(html_to_markdown(block.get("value", "")))
            elif isinstance(block, str):
                answer_parts.append(html_to_markdown(block))
        answer = "\n\n".join(answer_parts).strip()
        
        if not answer:
            continue
            
        if cat_slug not in faq_by_category:
            faq_by_category[cat_slug] = {
                "title": category_title,
                "items": []
            }
        faq_by_category[cat_slug]["items"].append({
            "question": question,
            "answer": answer,
            "slug": fields.get("slug", "")
        })

    faq_dir = KNOWLEDGE_DIR / "faq"
    faq_dir.mkdir(parents=True, exist_ok=True)
    for cat_slug, cat_data in faq_by_category.items():
        file_path = faq_dir / f"{cat_slug}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# FAQ - {cat_data['title']}\n\n")
            for item in cat_data["items"]:
                f.write(f"## {item['question']}\n\n")
                f.write(f"{item['answer']}\n\n---\n\n")
        print(f"Généré FAQ: {file_path.name} ({len(cat_data['items'])} Q/R)")

    # 2. Traitement des articles de blog
    blog_dir = KNOWLEDGE_DIR / "blog"
    blog_dir.mkdir(parents=True, exist_ok=True)
    blog_articles = [d for d in data if d["model"] == "blog.blogarticle"]
    for article in blog_articles:
        fields = article["fields"]
        title = fields.get("title", "Article")
        slug = fields.get("slug", "article")
        summary = fields.get("summary", "")
        content_blocks = fields.get("content", [])
        
        body_parts = []
        for block in content_blocks:
            if isinstance(block, dict) and block.get("type") == "rich_text":
                body_parts.append(html_to_markdown(block.get("value", "")))
        
        body = "\n\n".join(body_parts).strip()
        file_path = blog_dir / f"{slug}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            if summary:
                f.write(f"> **Résumé** : {summary}\n\n")
            f.write(body + "\n")
    print(f"Généré {len(blog_articles)} articles de blog dans {blog_dir}")


def main():
    print(f"Extraction des connaissances dans: {KNOWLEDGE_DIR}")
    
    # 1. Modèles ODT
    modeles_dir = KNOWLEDGE_DIR / "modeles"
    for odt_file in ODT_TEMPLATES_DIR.glob("*.odt"):
        extract_odt_to_markdown(odt_file, modeles_dir / f"{odt_file.stem}.md")
        
    # 2. FAQ et Blog
    process_dump_data()
    
    # 3. Custom README
    custom_dir = KNOWLEDGE_DIR / "custom"
    custom_dir.mkdir(parents=True, exist_ok=True)
    custom_readme = custom_dir / "README.md"
    if not custom_readme.exists():
        with open(custom_readme, "w", encoding="utf-8") as f:
            f.write(
                "# Documents et Procédures Complémentaires\n\n"
                "Déposez ici vos fichiers texte ou Markdown (.md ou .txt) contenant vos guides PDF "
                "ou modèles spécifiques. Ils seront automatiquement indexés et pris en compte par le Chatbot.\n"
            )
            
    print("Extraction et structuration terminées avec succès !")


if __name__ == "__main__":
    main()
