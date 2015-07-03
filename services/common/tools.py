import re
import json
from itertools import groupby

def parse_gff_block(block):
    """
    Parse a gff block where the first row is a gene feature record and
    each subsequent row is a subfeature of the gene
    """
    for feature in block:
        feature_fields = feature.split('\t')
        ftype = feature_fields[2]
        if ftype == 'gene':
            response = {
                'class': 'feature_property',
                'source_text_description': 'Araport11 feature',
                'location': feature_fields[0],
                'source': feature_fields[1],
                'type': ftype,
                'start': feature_fields[3],
                'end': feature_fields[4],
                'score': feature_fields[5],
                'strand': feature_fields[6],
                'phase': feature_fields[7],
                'id': extract_agi_identifier(feature_fields[8]),
                'description': extract_note(feature_fields[8]),
                'subfeatures': []
            }
        else:
            subfeature = {
                'location': feature_fields[0],
                'source': feature_fields[1],
                'type': ftype,
                'start': feature_fields[3],
                'end': feature_fields[4],
                'score': feature_fields[5],
                'strand': feature_fields[6],
                'phase': feature_fields[7],
                'id': extract_agi_identifier(feature_fields[8])
            }
            response['subfeatures'].append(subfeature)
    return response

def read_block(handle, signal):
    """
    Useful for reading block-like file formats, for example FASTA or OBO file,
    such file usually startswith some signal, and in-between the signals are a
    record
    """
    signal_len = len(signal)
    it = (x[1] for x in groupby(handle,
        key=lambda row: row.strip()[:signal_len] == signal))
    found_signal = False
    for header in it:
        header = header.next().strip()
        if header[:signal_len] != signal:
            continue
        found_signal = True
        seq = list(s.strip() for s in it.next())
        yield header, seq

    if not found_signal:
        handle.seek(0)
        seq = list(s.strip() for s in handle)
        yield None, seq

def extract_agi_identifier(line):
    p = re.compile(r'ID=(.*);')
    ident = ""
    m = p.search(line)
    if m:
        ident = m.group(1)
    return ident

def extract_note(line):
    p = re.compile(r'Note=(.*)')
    note = ""
    m = p.search(line)
    if m:
        note = m.group(1)
    return note

def is_valid_agi_identifier(ident):
    p = re.compile(r'AT[1-5MC]G[0-9]{5,5}\.[0-9]+', re.IGNORECASE)
    if not p.search(ident):
        return False
    return True

def send(data):
    """Display `data` in the format required by Adama.
    :type data: list
    """

    for elt in data:
        print json.dumps(elt)
        print '---'

def fail(message):
    # failure message for generic adapters
    return 'text/plaintext; charset=ISO-8859-1', message
