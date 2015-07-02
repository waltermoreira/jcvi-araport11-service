import gzip
import json
import services.common.tools as tools

ARAPORT11_GFF = 'data/Araport11_protein_coding_genes.gff3.gz'

def search(args):
    """
    args contains a dict with one or key:values

    locus is AGI identifier and is mandatory
    """
    #locus = args['locus']

    """
    Parse the local Araport11 gff3 file
    """

    """
    Iterate through the results
    Foreach record from the remote service, build the response json
    Print this json to stdout followed by a record separator "---"
    ADAMA takes care of serializing these results
    """
    """
    for result in response['lines']:

        record = {
                'locus': locus,
                'class': 'locus_property',
                'source_text_description': 'Reporter_Image_data',
                'line_record': {
                        'line_id': result['line_id']
                }
            }
        print json.dumps(record, indent=2)
        print '---'
    """

def list():
    """
    List all of the available loci from the Araport11 protein-coding gene set
    """

    with gzip.open(ARAPORT11_GFF, 'r') as f:
        for header, data in tools.read_block(f, '###'):
            gene_fields = data[0].split('\t')
            locus =  tools.extract_agi_identifier(gene_fields[8])

            record = {
                'locus': locus,
                'class': 'locus_property',
                'source_text_description': 'Araport11 locus'
            }

            print json.dumps(record, indent=2)
            print '---'
