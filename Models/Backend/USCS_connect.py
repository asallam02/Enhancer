import mysql.connector
import requests
import xml.etree.ElementTree as ET

def get_genes(chromosome, start, end):
    """Connects to the UCSC MySQL database to obtain genes within given coordinates.
    Assumes that integer end >= integer start. 
    """
    # Connect to the UCSC MySQL database
    connection = mysql.connector.connect(
        host="genome-mysql.cse.ucsc.edu",
        user="genome",
        password="",
        database="hg38"
    )

    cursor = connection.cursor(dictionary=True)

    # Query to retrieve genes within the specified region
    query = "SELECT name, name2, txStart, txEnd FROM refGene WHERE chrom = %s AND txStart >= %s AND txStart <= %s"
    cursor.execute(query, (chromosome, start, end))

    genes = []
    for row in cursor.fetchall():
        gene_name = row['name']
        gene_symbol = row['name2']
        gene_start = row['txStart']
        gene_end = row['txEnd']
        genes.append((gene_name, gene_symbol, gene_start, gene_end))

    cursor.close()
    connection.close()

    return genes


def get_fasta(chromosome, start, end, assembly="hg38"):
    """Connects to the USCS DAS files to get fasta sequence for hg38.
    Gets fasta sequence given chromosome str, and start and stop integer indexes. 
    assumes that coordinates are such that end >= start. 
    """
    url = f"https://genome.ucsc.edu/cgi-bin/das/{assembly}/dna?segment={chromosome}:{start},{end}"
    response = requests.get(url)
    if response.status_code == 200:
        XML_page = ET.fromstring(response.text)
        dna_tag = XML_page.find(".//DNA")
        return dna_tag.text.strip().replace("\n", "")
    else:
        print(f"Failed to retrieve sequence: {response.status_code}")
        return None
