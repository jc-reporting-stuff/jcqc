from django.conf import settings
from sequences.models import Worksheet

from sys import platform

import shutil
import os


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


def dropbox_folders():
    raw_folders = []
    # Walk the dropbox directory and keep track of what's found
    # Don't validate for duplicate folder names since the system should do that
    dropbox_folder = os.path.join(
        settings.FILES_BASE_DIR, settings.DROPBOX_DIR, '')
    for path, dirs, files in os.walk(dropbox_folder):
        name = path.replace(dropbox_folder, '')
        folder_object = {'name': name,
                         'ab1_files': 0, 'seq_files': 0, 'size': 0}
        for file in files:
            extension = file[-3:]
            if extension == 'ab1':
                folder_object['ab1_files'] += 1
            elif extension == 'seq':
                folder_object['seq_files'] += 1
            filename = os.path.join(path, file)
            folder_object['size'] += os.path.getsize(filename)

        # Make the size field human-readable
        if folder_object['size'] > 10**6:
            folder_object['size'] /= 10**6
            folder_object['size'] = str(
                round(folder_object['size'], 1)) + ' MB'
        else:
            folder_object['size'] /= 1000
            folder_object['size'] = str(
                round(folder_object['size'], 1)) + ' kB'
        raw_folders.append(folder_object)

    # remove the blank root-level directory
    folders = [folder for folder in raw_folders if len(folder['name']) > 0]
    return folders


# Check if the customer sequence folder exists.
# If the create flag is set to true, create the folder if it does not exist.
def check_customer_folder_exists(path, create=True):
    if not os.path.exists(path) and create:
        os.makedirs(os.path.join(
            settings.FILES_BASE_DIR, settings.CUSTOMER_SEQUENCES_DIR))
    return


class SuccessfulImport:
    def __init__(self, name, username, ab1=False, seq=False):
        self.name = name
        self.ab1 = ab1
        self.seq = seq
        self.username = username

    def make_true(self, extension):
        if extension == 'ab1':
            self.ab1 = True
        elif extension == 'seq':
            self.seq = True

    def __repr__(self):
        return f'{self.name}: ab1({self.ab1}), seq({self.seq})'
