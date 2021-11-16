from sequences.models import Worksheet


def create_runfile(plate_id, block_num, analysis_module):
    items = Worksheet.objects.filter(plate_id=plate_id, block=block_num)

    headers = ['Container Name', 'Plate ID', 'Description', 'ContainerType',
               'AppType', 'Owner', 'Operator', 'PlateSealing', 'SchedulingPref']
    top_row = '\t'.join(headers) + '\n'

    meta = [items[0].plate.name, items[0].plate.name, ' ', '96-Well',
            'Regular', 'LSD', 'LSD', 'Septa', '1234']
    meta_row = '\t'.join(meta) + '\n'

    meta_row2 = 'AppServer\tAppInstance\n'
    meta_row3 = 'SequencingAnalysis\n'
    sample_headings = ['Well', 'Sample Name', 'Comment',
                       'Results Group 1', 'Instrument Protocol 1', 'Analysis Protocol 1']
    heading_row = '\t'.join(sample_headings)

    text = top_row + meta_row + meta_row2 + meta_row3 + heading_row

    for item in items:
        sample_name = f'{item.reaction.id}_{item.reaction.template.name}_{item.reaction.primer.name}'
        rxn_comment = item.reaction.comment[:
                                            15] if item.reaction.comment else ' '
        columns = [item.well, sample_name, rxn_comment, 'LSD_Service',
                   'LSD', analysis_module]
        text += '\n' + '\t'.join(columns) + '\t'
    return text
