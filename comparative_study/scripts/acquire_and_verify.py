from __future__ import annotations

import html
import io
import json
import re
import tarfile
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote
from xml.etree import ElementTree

import fitz
import requests


ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "metadata"
PAPERS = ROOT / "papers"
TEXT = ROOT / "paper_text"
PAGES = ROOT / "article_pages"
for directory in (META, PAPERS, TEXT, PAGES):
    directory.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "MenstrualHygieneComparativeStudy/1.0 (research use)"}
SEARCH_DATE = date.today().isoformat()
SEARCH_QUERIES = [
    'Pakistan adolescent girls menstrual hygiene maternal education',
    'Pakistan schoolgirls menstrual hygiene knowledge practice',
    'South Asia adolescent menstrual hygiene maternal education practice',
    'adolescent girls menstrual hygiene knowledge practice parental education',
]

PUBLISHER_PDFS = {
    "10.7189/jogh.12.04059": "https://jogh.org/wp-content/uploads/2022/08/jogh-12-04059.pdf",
    "10.1186/s12905-019-0874-3": "https://link.springer.com/content/pdf/10.1186/s12905-019-0874-3.pdf",
    "10.7759/cureus.73899": "https://www.cureus.com/articles/298309-awareness-and-practices-of-menstrual-hygiene-among-rural-adolescent-schoolgirls-in-lahore-pakistan-a-cross-sectional-study.pdf",
    "10.1186/s12905-015-0245-7": "https://link.springer.com/content/pdf/10.1186/s12905-015-0245-7.pdf",
}

STUDIES = [
    {
        "key": "wasan2022",
        "title": "Practices and predictors of menstrual hygiene management material use among adolescent and young women in rural Pakistan: a cross-sectional assessment",
        "doi": "10.7189/jogh.12.04059",
        "pmid": "35908217",
        "pmcid": "PMC9339234",
        "region": "Pakistan",
        "setting": "Matiari District, rural Sindh",
    },
    {
        "key": "aziz2024",
        "title": "A comparative study of the knowledge and practices related to menstrual hygiene among adolescent girls in urban and rural areas of Sindh, Pakistan: A cross-sectional study",
        "doi": "10.1177/17455057241231420",
        "pmid": "38385267",
        "pmcid": "PMC10893828",
        "region": "Pakistan",
        "setting": "Government girls' schools, Khairpur District, Sindh",
    },
    {
        "key": "shah2023",
        "title": "Knowledge, Attitudes, and Practices Regarding Menstrual Hygiene among Girls in Ghizer, Gilgit, Pakistan",
        "doi": "10.3390/ijerph20146424",
        "pmid": "37510656",
        "pmcid": "PMC10378792",
        "region": "Pakistan",
        "setting": "Government educational institutions, Ghizer District",
    },
    {
        "key": "michael2020",
        "title": "Knowledge and practice of adolescent females about menstruation and menstruation hygiene visiting a public healthcare institute of Quetta, Pakistan",
        "doi": "10.1186/s12905-019-0874-3",
        "pmid": "31906921",
        "pmcid": "PMC6945726",
        "region": "Pakistan",
        "setting": "Public hospital outpatient department, Quetta",
    },
    {
        "key": "afzaal2024",
        "title": "Awareness and Practices of Menstrual Hygiene Among Rural Adolescent Schoolgirls in Lahore, Pakistan: A Cross-Sectional Study",
        "doi": "10.7759/cureus.73899",
        "pmid": "39697906",
        "pmcid": "PMC11655083",
        "region": "Pakistan",
        "setting": "Rural schoolgirls, Lahore",
    },
    {
        "key": "dasgupta2008",
        "title": "Menstrual hygiene: how hygienic is the adolescent girl?",
        "doi": "10.4103/0970-0218.40872",
        "pmid": "19967028",
        "pmcid": "PMC2784630",
        "region": "India",
        "setting": "Rural secondary school, Singur, West Bengal",
    },
    {
        "key": "kansal2016",
        "title": "Menstrual Hygiene Practices in Context of Schooling: A Community Study Among Rural Adolescent Girls in Varanasi",
        "doi": "10.4103/0970-0218.170964",
        "pmid": "26917872",
        "pmcid": "PMC4746952",
        "region": "India",
        "setting": "Eight rural villages, Varanasi",
    },
    {
        "key": "yadav2018",
        "title": "Knowledge, Attitude, and Practice on Menstrual Hygiene Management among School Adolescents",
        "doi": "10.3126/jnhrc.v15i3.18842",
        "pmid": "29353891",
        "region": "Nepal",
        "setting": "Schools in Doti District",
        "pdf_url": "https://www.nepjol.info/index.php/JNHRC/article/download/18842/15403",
    },
    {
        "key": "bhusal2020",
        "title": "Practice of Menstrual Hygiene and Associated Factors among Adolescent School Girls in Dang District, Nepal",
        "doi": "10.1155/2020/1292070",
        "pmid": "32774926",
        "pmcid": "PMC7396122",
        "region": "Nepal",
        "setting": "Public and private schools, Dang District",
    },
    {
        "key": "haque2014",
        "title": "The effect of a school-based educational intervention on menstrual health: an intervention study among adolescent girls in Bangladesh",
        "doi": "10.1136/bmjopen-2013-004607",
        "pmid": "24993753",
        "pmcid": "PMC4091465",
        "region": "Bangladesh",
        "setting": "Three rural schools, Araihazar",
    },
    {
        "key": "alam2017",
        "title": "Menstrual hygiene management among Bangladeshi adolescent schoolgirls and risk factors affecting school absence: results from a cross-sectional survey",
        "doi": "10.1136/bmjopen-2016-015508",
        "pmid": "28694347",
        "pmcid": "PMC5541609",
        "region": "Bangladesh",
        "setting": "National survey of 700 schools",
    },
    {
        "key": "upashe2015",
        "title": "Assessment of knowledge and practice of menstrual hygiene among high school girls in Western Ethiopia",
        "doi": "10.1186/s12905-015-0245-7",
        "pmid": "26466992",
        "pmcid": "PMC4606849",
        "region": "Ethiopia (contextual)",
        "setting": "High schools, Nekemte",
    },
]


def norm(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", html.unescape(value or "").lower()).strip()


def get(url: str, timeout: int = 60) -> requests.Response:
    response = requests.get(url, timeout=timeout, headers=HEADERS, allow_redirects=True)
    response.raise_for_status()
    return response


def search_pubmed(query: str) -> dict:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    response = requests.get(
        url,
        params={"db": "pubmed", "term": query, "retmode": "json", "retmax": 200},
        headers=HEADERS,
        timeout=60,
    )
    response.raise_for_status()
    result = response.json()["esearchresult"]
    return {"database": "PubMed", "query": query, "count": int(result["count"]), "pmids": result["idlist"]}


def search_openalex(query: str) -> dict:
    response = requests.get(
        "https://api.openalex.org/works",
        params={"search": query, "per-page": 100, "select": "id,display_name,doi,publication_year,open_access"},
        headers=HEADERS,
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return {
        "database": "OpenAlex",
        "query": query,
        "count": payload["meta"]["count"],
        "results": payload["results"],
    }


def crossref(doi: str) -> dict:
    payload = get(f"https://api.crossref.org/works/{quote(doi, safe='')}").json()["message"]
    title = " ".join(payload.get("title") or [])
    published = ((payload.get("published") or {}).get("date-parts") or [[]])[0]
    authors = [
        " ".join(part for part in (author.get("given"), author.get("family")) if part)
        for author in payload.get("author") or []
    ]
    return {
        "title": title,
        "title_similarity": round(SequenceMatcher(None, norm(title), norm(doi_title(doi))).ratio(), 4),
        "authors": authors,
        "journal": " ".join(payload.get("container-title") or []),
        "published": published,
        "volume": payload.get("volume"),
        "issue": payload.get("issue"),
        "pages": payload.get("page") or payload.get("article-number"),
        "url": payload.get("URL"),
    }


def doi_title(doi: str) -> str:
    return next(study["title"] for study in STUDIES if study["doi"] == doi)


def verify_handle(doi: str) -> bool:
    payload = get(f"https://doi.org/api/handles/{quote(doi, safe='')}").json()
    return payload.get("responseCode") == 1


def save_pmc_sources(study: dict) -> dict:
    pmcid = study["pmcid"]
    xml_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    xml = get(xml_url, 90).content
    xml_path = PAGES / f"{study['key']}.xml"
    xml_path.write_bytes(xml)
    xml_root = ElementTree.fromstring(xml)
    blocks = []
    for element in xml_root.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        if tag not in {"title", "p", "th", "td"}:
            continue
        value = re.sub(r"\s+", " ", " ".join(element.itertext())).strip()
        if value and (not blocks or blocks[-1] != value):
            blocks.append(value)
    text = "\n".join(blocks)
    text_path = TEXT / f"{study['key']}.txt"
    text_path.write_text(text, encoding="utf-8")

    result = {
        "article_xml": xml_path.relative_to(ROOT).as_posix(),
        "text_path": text_path.relative_to(ROOT).as_posix(),
        "text_chars": len(text),
    }
    try:
        publisher_pdf = PUBLISHER_PDFS.get(study["doi"])
        if publisher_pdf:
            pdf = get(publisher_pdf, 180).content
            if not pdf.startswith(b"%PDF"):
                raise ValueError("Publisher response is not a PDF")
            pdf_path = PAPERS / f"{study['key']}.pdf"
            pdf_path.write_bytes(pdf)
            with fitz.open(pdf_path) as document:
                extracted = "\n".join(page.get_text() for page in document)
                result.update(
                    {
                        "pdf_url": publisher_pdf,
                        "pdf_path": pdf_path.relative_to(ROOT).as_posix(),
                        "pdf_pages": document.page_count,
                    }
                )
                result["pdf_text_chars"] = len(extracted)
            return result

        oa_xml = get(f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={pmcid}").content
        oa_root = ElementTree.fromstring(oa_xml)
        package_url = next(
            link.attrib["href"] for link in oa_root.findall(".//link") if link.attrib.get("format") == "tgz"
        ).replace("ftp://", "https://")
        package = get(package_url, 180).content
        with tarfile.open(fileobj=io.BytesIO(package), mode="r:gz") as archive:
            pdf_member = next(member for member in archive.getmembers() if member.isfile() and member.name.lower().endswith(".pdf"))
            pdf_stream = archive.extractfile(pdf_member)
            if pdf_stream is None:
                raise ValueError("PDF member could not be read from the NCBI package")
            pdf = pdf_stream.read()
        if not pdf.startswith(b"%PDF"):
            raise ValueError("NCBI package member is not a PDF")
        pdf_path = PAPERS / f"{study['key']}.pdf"
        pdf_path.write_bytes(pdf)
        with fitz.open(pdf_path) as document:
            extracted = "\n".join(page.get_text() for page in document)
            result.update(
                {
                    "pdf_url": package_url,
                    "pdf_path": pdf_path.relative_to(ROOT).as_posix(),
                    "pdf_pages": document.page_count,
                }
            )
            result["pdf_text_chars"] = len(extracted)
    except Exception as exc:  # noqa: BLE001
        result["pdf_error"] = str(exc)
    return result


def save_direct_pdf(study: dict) -> dict:
    try:
        pdf = get(study["pdf_url"], 120).content
        if not pdf.startswith(b"%PDF"):
            raise ValueError("Downloaded response is not a PDF")
        pdf_path = PAPERS / f"{study['key']}.pdf"
        pdf_path.write_bytes(pdf)
        with fitz.open(pdf_path) as document:
            text = "\n".join(page.get_text() for page in document)
            pages = document.page_count
        text_path = TEXT / f"{study['key']}.txt"
        text_path.write_text(text, encoding="utf-8")
        return {
            "pdf_url": study["pdf_url"],
            "pdf_path": pdf_path.relative_to(ROOT).as_posix(),
            "pdf_pages": pages,
            "text_path": text_path.relative_to(ROOT).as_posix(),
            "text_chars": len(text),
        }
    except Exception as pdf_error:  # noqa: BLE001
        page_url = f"https://www.nepjol.info/index.php/JNHRC/article/view/18842"
        response = get(page_url, 90)
        page_path = PAGES / f"{study['key']}.html"
        page_path.write_text(response.text, encoding="utf-8")
        abstract = re.search(r'<meta name="citation_abstract"[^>]+content="([^"]+)"', response.text)
        text = html.unescape(abstract.group(1)) if abstract else re.sub(r"<[^>]+>", " ", response.text)
        text_path = TEXT / f"{study['key']}.txt"
        text_path.write_text(re.sub(r"\s+", " ", text).strip(), encoding="utf-8")
        return {
            "pdf_url": study["pdf_url"],
            "pdf_error": str(pdf_error),
            "article_page": page_path.relative_to(ROOT).as_posix(),
            "text_path": text_path.relative_to(ROOT).as_posix(),
            "text_chars": len(text),
        }


def main() -> None:
    searches = []
    for query in SEARCH_QUERIES:
        for search in (search_pubmed, search_openalex):
            try:
                searches.append(search(query))
            except Exception as exc:  # noqa: BLE001
                searches.append({"database": search.__name__, "query": query, "error": str(exc)})
    (META / "search_results.json").write_text(json.dumps(searches, indent=2), encoding="utf-8")

    audited = []
    for study in STUDIES:
        record = dict(study)
        try:
            record["handle_valid"] = verify_handle(study["doi"])
            record["crossref"] = crossref(study["doi"])
            record["title_match"] = record["crossref"]["title_similarity"] >= 0.85
        except Exception as exc:  # noqa: BLE001
            record["metadata_error"] = str(exc)
            record["handle_valid"] = False
            record["title_match"] = False
        try:
            evidence = save_pmc_sources(study) if study.get("pmcid") else save_direct_pdf(study)
            record["evidence"] = evidence
            if evidence.get("pdf_path") or study.get("pmcid"):
                record["evidence_status"] = "full_text_checked" if evidence.get("text_chars", 0) > 5000 else "full_text_extraction_weak"
            else:
                record["evidence_status"] = "abstract_and_doi_checked"
        except Exception as exc:  # noqa: BLE001
            record["evidence_status"] = "retrieval_failed"
            record["evidence_error"] = str(exc)
        audited.append(record)

    (META / "included_studies.json").write_text(json.dumps(audited, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# Literature Acquisition and Verification Audit",
        "",
        f"Search and verification date: {SEARCH_DATE}",
        "",
        "## Search Sources",
        "",
        "PubMed and OpenAlex were searched with four prespecified queries. The complete machine-readable results are in `search_results.json`.",
        "",
        "## Included Studies",
        "",
    ]
    for index, item in enumerate(audited, 1):
        crossref_data = item.get("crossref") or {}
        evidence = item.get("evidence") or {}
        lines.extend(
            [
                f"### {index}. {item['title']}",
                "",
                f"- Region: {item['region']}",
                f"- Setting: {item['setting']}",
                f"- DOI: https://doi.org/{item['doi']}",
                f"- PMID: {item.get('pmid', 'Not available')}",
                f"- PMCID: {item.get('pmcid', 'Not available')}",
                f"- DOI Handle valid: {item.get('handle_valid')}",
                f"- Crossref title similarity: {crossref_data.get('title_similarity')}",
                f"- Crossref title match: {item.get('title_match')}",
                f"- Evidence status: {item.get('evidence_status')}",
                f"- Local full text: {evidence.get('text_path', item.get('evidence_error', 'Unavailable'))}",
                f"- Local PDF: {evidence.get('pdf_path', 'Unavailable')}",
                "",
            ]
        )
    failed = [item["key"] for item in audited if item.get("evidence_status") != "full_text_checked"]
    lines.extend(["## Retrieval Limitations", "", f"Studies without strong extracted full text: {', '.join(failed) if failed else 'None'}", ""])
    (META / "acquisition_audit.md").write_text("\n".join(lines), encoding="utf-8")

    verified = sum(bool(item.get("handle_valid") and item.get("title_match")) for item in audited)
    full_text = sum(item.get("evidence_status") == "full_text_checked" for item in audited)
    print(f"Search records: {len(searches)}")
    print(f"Verified DOI/title records: {verified}/{len(audited)}")
    print(f"Strong full-text extracts: {full_text}/{len(audited)}")


if __name__ == "__main__":
    main()
