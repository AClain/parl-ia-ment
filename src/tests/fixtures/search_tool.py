import pytest
from typing import TypedDict
from bs4 import BeautifulSoup


class HtmlPageWithNextButtonHref(TypedDict):
    """
    Object associating an HTML containing a search tool Suivant
    button and its href property.
    """
    html: BeautifulSoup
    href: str


@pytest.fixture
def search_tool_next_html() -> HtmlPageWithNextButtonHref:
    """
    A parsed HTML page containing a next button (Suivant).

    Returns
    -------
    HtmlPageWithNextButtonHref
        A dictionary containing :
        - The parsed HTML page content
        - The link to the next result page
    """
    next_button_str = (
        "<html>"
        "<div class=\"random\">"
        "<a href=\"another_website/route/next\">"
        "Suivant"
        "</a>"
        "</div>"
        "<a href=\"/recherche/resultats_questions/13/"
        "(offset)/200/(query)"
        "eyJxIjoibGVnaXNsYXR1cmU6MTMgYW5kIHNzVHlw"
        "ZURvY3VtZW50OihxZSBPUiBxZyBPUiBxb3NkKSBhb"
        "mQgcnVicmlxdWU6XCJhZG1pbmlzdHJhdGlvblwiIiw"
        "icm93cyI6IjEwMCIsInNvcnQiOiJzc1R5cGVEb2N1b"
        "WVudCBhc2MsIG51bURvY3VtZW50IGRlc2MifQ==\" "
        "data-uri-suffix=\"/(offset)/200/(query)/"
        "eyJxIjoibGVnaXNsYXR1cmU6MTMgYW5kIHNzVHlwZU"
        "RvY3VtZW50OihxZSBPUiBxZyBPUiBxb3NkKSBhbmQg"
        "cnVicmlxdWU6XCJhZG1pbmlzdHJhdGlvblwiIiwicm"
        "93cyI6IjEwMCIsInNvcnQiOiJzc1R5cGVEb2N1bWVu"
        "dCBhc2MsIG51bURvY3VtZW50IGRlc2MifQ==\" "
        "data-uri-init=""><span class=\"text\">"
        "Suivant&nbsp;&raquo;</span></a>"
        "</html>"
    )

    next_html_page = BeautifulSoup(
        next_button_str,
        "html.parser"
    )

    next_href = (
        "https://www2.assemblee-nationale.fr"
        "/recherche/resultats_question"
        "/recherche/resultats_questions/13/"
        "(offset)/200/(query)"
        "eyJxIjoibGVnaXNsYXR1cmU6MTMgYW5kIHNzVHlw"
        "ZURvY3VtZW50OihxZSBPUiBxZyBPUiBxb3NkKSBhb"
        "mQgcnVicmlxdWU6XCJhZG1pbmlzdHJhdGlvblwiIiw"
        "icm93cyI6IjEwMCIsInNvcnQiOiJzc1R5cGVEb2N1b"
        "WVudCBhc2MsIG51bURvY3VtZW50IGRlc2MifQ=="
    )

    return {
        "html": next_html_page,
        "href": next_href
    }


@pytest.fixture
def search_tool_question_links_html() -> BeautifulSoup:
    """
    Parsed HTML page containing question links.

    Returns
    -------
    BeautifulSoup
        A parsed HTML page.
    """
    html = """
    <html>
    <table>\n
     \t\t\t\t\t\t\t<thead>\n
     \t\t\t\t\t\t\t\t<tr>\n
     \t\t\t\t\t\t\t\t\t<th>N°</th>\n
     \t\t\t\t\t\t\t\t\t<th>Intitulé</th>\n
     \t\t\t\t\t\t\t\t\t<th>Date</th>\n
     \t\t\t\t\t\t\t\t</tr>\n
     \t\t\t\t\t\t\t</thead>\n
     \t\t\t\t\t\t\t<tbody> \n
     \t\t\t\t\t\t\t \n
     \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\n
     \t\t\t\t\t\t\t\t\t<td class="nowrap"><a 
     href="https://questions.assemblee-nationale.fr/q15/15-45416QE.htm"><strong>15ème 
     législature - QE 45416</strong></a>\n
                                         \n
                                                                             \n
                                         </td>\n
     \t\t\t\t\t\t\t\t\t<td class="text-center">\n
     \t\t\t\t\t\t\t\t\t\t<strong>M. Hervé Saulignac</strong> (Socialistes et 
     apparentés) - Ardèche<br />\n
     \t\t\t\t\t\t\t\t\t\t\n
     \t\t\t\t\t\t\t\t\t\t \n
     \t\t\t\t\t\t\t\t\t\t\t<em>fonction publique territoriale - Autorisation 
     "spéciale dabsence (ASA)</em><br />\n"
     \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tMinistère :  <strong>Transformation 
     et fonction publiques</strong>\n
     \t\t\t\t\t\t\t\t\t</td>\n
     \t\t\t\t\t\t\t\t\t<td class="nowrap text-center">\n
     \t\t\t\t\t\t\t\t\t\tPubliée au JO le  <strong>03/05/2022</strong>\n
     \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n
     \n
     \t\t\t\t\t\t\t\t\t</td>\n
     \t\t\t\t\t\t\t\t</tr>\n
      \t\t\t\t\t\t\t\t\t<td class="nowrap"><a 
     href="https://questions.assemblee-nationale.fr/q15/15-45392QE.htm"><strong>15ème 
     législature - QE 45392</strong></a>\n
                                         \n
                                                                             \n
                                         </td>\n
     \t\t\t\t\t\t\t\t\t<td class="text-center">\n
     \t\t\t\t\t\t\t\t\t\t<strong>M. Fabrice Brun</strong> (Les Républicains) - 
     Ardèche<br />\n
     \t\t\t\t\t\t\t\t\t\t\n
     \t\t\t\t\t\t\t\t\t\t \n
     \t\t\t\t\t\t\t\t\t\t\t<em>transports routiers - Situation des entreprises du 
     transport routier et coût du carburant</em><br />\n
     \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tMinistère :  <strong>Économie, 
     finances, souveraineté industrielle et numérique</strong>\n
     \t\t\t\t\t\t\t\t\t</td>\n
     \t\t\t\t\t\t\t\t\t<td class="nowrap text-center">\n
     \t\t\t\t\t\t\t\t\t\tPubliée au JO le  <strong>26/04/2022</strong>\n
     \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n
     \n
     \t\t\t\t\t\t\t\t\t</td>\n
     \t\t\t\t\t\t\t\t</tr>\n
                                     \n
                                     \n
                                                                     \n
     \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\n
     \t\t\t\t\t\t</table>
     </html>
    """

    return BeautifulSoup(html, "html.parser")
