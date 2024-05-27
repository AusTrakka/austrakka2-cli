import xlsxwriter

# Defined Excel formats
DEFAULT_FONT = 'Courier New'
DEFAULT_FONTSIZE = 12
BASE = {
    'font_name': DEFAULT_FONT,
    'font_size': DEFAULT_FONTSIZE,
}
BOLD = {'bold': True}
ISO_DATE = {'num_format': 'yyyy-mm-dd'}
BORDER = {'border': True}
BG_GREEN = {'bg_color': '#A9D08E'}
WHITE_ON_BLACK = {'font_color': 'white', 'bg_color': 'black'}
WRAPPED = {'text_wrap': True}

# Type descriptions in template
TYPE_DESCRIPTIONS = {
    'string': 'String',
    'number': 'Numeric (integer)',
    'double': 'Numeric (floating-point)',
    'categorical': 'Controlled string',
    'date': 'Date'
}

# Fields for which the template should list a type other than the database-specified type
# e.g. fields which are strings but are effectively controlled by some means other than valid values
SPECIAL_TYPES = {
    'Owner_group': 'Controlled string',
    'Shared_groups': 'Controlled semicolon-separated strings'
}

# pylint: disable=too-many-locals disable=too-many-statements disable=too-many-branches
def generate_template(
        filename, proforma, restricted_values, nndss_column, project, num_format_rows=21):
    fields = list(proforma['name'])
    
    allowed_values = {
        field['name']: (field['allowedValues'].split(';') 
            if field['type']=='categorical' else []) 
        for (i,field) in proforma.iterrows()}
        
    for field in restricted_values:
        if field not in allowed_values:
            raise ValueError(f"Restricted values for field {field} which is not in proforma")
        bad_restricted_values = set(restricted_values[field]) - set(allowed_values[field])
        if len(bad_restricted_values) > 0:
            raise ValueError(
                f"Restricted values for field {field} are not valid values: {bad_restricted_values}"
            )
        allowed_values[field] = restricted_values[field]
    
    # Required widths when populated with values, i.e. type dictionary tab
    required_widths = {field: max(len(v) for v in (allowed_values[field]+[field]))
                        for field in fields}
    
    workbook = xlsxwriter.Workbook(filename)
    workbook.set_size(1500, 800) # default size when first opened
    
    # Formats
    normal_format = workbook.add_format(BASE)
    green_header_format = workbook.add_format(BASE | BG_GREEN)
    black_header_format = workbook.add_format(BASE | WHITE_ON_BLACK | BOLD)
    border_format = workbook.add_format(BASE | BORDER)
    bold_border_format = workbook.add_format(BASE | BOLD | BORDER)
    wrapped_border_format = workbook.add_format(BASE | WRAPPED | BORDER)
    green_wrapped_border_format = workbook.add_format(BASE | BG_GREEN | WRAPPED | BORDER)
    iso_date_format = workbook.add_format(BASE | ISO_DATE)
    
    # Worksheets
    metadata_sheet = workbook.add_worksheet('Metadata submission')
    datadict_sheet = workbook.add_worksheet('Data dictionary')
    typedict_sheet = workbook.add_worksheet('Type dictionary')
    ownergroups_sheet = workbook.add_worksheet('Owner_groups')
    sharinggroups_sheet = workbook.add_worksheet('Groups for sharing')

    # Metadata worksheet
    for (col, field) in enumerate(fields):
        # Write header row and set column widths to fit field names
        metadata_sheet.write_string(0, col, field, green_header_format)
        metadata_sheet.set_column(col, col, max(10, len(field)*1.5//1))
        # Add categorical field validation
        if proforma.loc[field, 'type'] == 'categorical':
            metadata_sheet.data_validation(1, col, num_format_rows, col, 
                {
                    'validate':'list',
                    'input_title': 'See Type Dictionary tab',
                    'source': allowed_values[field]
                })
        # Set date field formats
        if proforma.loc[field, 'type'] == 'date':
            metadata_sheet.set_column(col, col, None, iso_date_format)
    
    # Data dictionary worksheet
    seq_id_length = 1.5*max([24]+[len(f) for f in fields])
    datadict_columns = [
        'AusTrakka metadata label',
        'NNDSS metadata label',
        'Metadata class',
        'Definition',
        'Value Type',
        'Example',
        'Guidance'
    ]        
    datadict_lengths = [seq_id_length, 26, 20, 45, 25, 30, 45]
    if not nndss_column:
        datadict_columns.pop(1)
        datadict_lengths.pop(1)
    # Header row and column widths
    for (col,(name,length)) in enumerate(zip(datadict_columns,datadict_lengths)):
        datadict_sheet.write_string(0, col, name, black_header_format)
        datadict_sheet.set_column(col, col, length)
    # Column values
    nndss_offset = 1 if nndss_column else 0
    for row,field in enumerate(fields,1):
        datadict_sheet.write_string(row, 0, field, border_format)
        if nndss_column:
            datadict_sheet.write_string(row, 1, 
                proforma.loc[field, 'nndssFieldLabel'],
                border_format)
        # class (minimum, etc) - we only know if strictly required; 
        # project team must specify if minimum/optional
        datadict_sheet.write_string(row, 1+nndss_offset, 
            "Minimum - can't be blank" if proforma.loc[field, 'isRequired'] else "",
            green_wrapped_border_format)
        datadict_sheet.write_string(row, 2+nndss_offset,
            proforma.loc[field, 'description'],
            wrapped_border_format)
        datadict_sheet.write_string(row, 3+nndss_offset,
                                    _describe_type(field, proforma), wrapped_border_format)
        datadict_sheet.write_string(row, 4+nndss_offset,
            _give_examples(field, allowed_values, proforma.loc[field, 'type']),
            wrapped_border_format)
        # guidance, wrapped - to be filled in by project leads
        datadict_sheet.write_string(row, 5+nndss_offset, '', wrapped_border_format)
    
    # Type dictionary worksheet
    for (col, field) in enumerate(fields):
        # Header row
        typedict_sheet.write_string(0, col, field, green_header_format)
        # Set from length of field header or data values, whichever is longer
        typedict_sheet.set_column(col, col, max(required_widths[field]*1.5//1, 10))
        # Allowed values, or format specifier for date fields
        if proforma.loc[field, 'type'] == 'date':
            typedict_sheet.write_string(1, col, 'YYYY-MM-DD')
        elif proforma.loc[field, 'type'] == 'categorical':
            for (row, value) in enumerate(allowed_values[field],1):
                typedict_sheet.write_string(row, col, value, normal_format)
    
    # Owner groups worksheet header only
    ownergroup_columns = ['Abbreviation', 'Owner_group value', 'Organisation name']
    ownergroup_widths = [15, 30, 40]
    for (col,(name,width)) in enumerate(zip(ownergroup_columns,ownergroup_widths)):
        ownergroups_sheet.write_string(0, col, name, bold_border_format)
        ownergroups_sheet.set_column(col, col, width)
    
    # Shared group recommendation, with a row filled in if project specified
    sharinggroup_columns = ['Abbreviation', 'Group description']
    sharinggroup_widths = [15, 40]
    for (col,(name,width)) in enumerate(zip(sharinggroup_columns,sharinggroup_widths)):
        sharinggroups_sheet.write_string(0, col, name, bold_border_format)
        sharinggroups_sheet.set_column(col, col, width)
    if project:
        sharinggroups_sheet.write_string(1, 0, project['abbreviation'], border_format)
        sharinggroups_sheet.write_string(1, 1, f"{project['name']} project", border_format)
    
    workbook.close()
   

def _describe_type(field, proforma):
    if field in SPECIAL_TYPES:
        return SPECIAL_TYPES[field]
    return TYPE_DESCRIPTIONS[proforma.loc[field, 'type']]

def _give_examples(field, allowed_values, field_type):
    if field_type != 'categorical':
        return ''
    values = allowed_values[field]
    if len(values) > 5:
        return ','.join(values[:4]+values[-1:])
    return ', '.join(values)
        