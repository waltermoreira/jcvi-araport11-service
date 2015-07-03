import gzip
import json
import os.path as op
import services.common.tools as tools

ARAPORT11_GFF = op.join(op.dirname(__file__), 'data', 'Araport11_protein_coding_genes.gff3.gz')

def search(args):
    """
    args contains a dict with one or key:values

    locus is AGI identifier and is mandatory
    """
    search_locus = args['locus']

    """
    Parse the local Araport11 gff3 file to find the search locus
    """
    locus_record = None
    with gzip.open(ARAPORT11_GFF, 'r') as f:
        for header, data in tools.read_block(f, '###'):
            gene_fields = data[0].split('\t')
            locus =  tools.extract_agi_identifier(gene_fields[8])
            if search_locus == locus:
                locus_record = data
                break

    """
    Iterate through the results
    Foreach record from the remote service, build the response json
    Print this json to stdout followed by a record separator "---"
    ADAMA takes care of serializing these results
    """
    response = tools.parse_gff_block(locus_record)
    if response:
        return 'application/json', json.dumps(response)
    else:
        tools.fail('Failed to parse the gff file')

def list(args):
    """
    List all of the available loci from the Araport11 protein-coding gene set
    """

    response = []
    with gzip.open(ARAPORT11_GFF, 'r') as f:
        for header, data in tools.read_block(f, '###'):
            gene_fields = data[0].split('\t')
            locus = tools.extract_agi_identifier(gene_fields[8])

            record = {
                'locus': locus,
                'class': 'locus_property',
                'source_text_description': 'Araport11 locus'
            }
            response.append(record)

    if len(response) != 0:
        return 'application/json', json.dumps(response)
    else:
        tools.fail('Failed to parse the gff file')
