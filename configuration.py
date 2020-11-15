class configuration:
    def __init__(self,operation,number_of_rows,add_column_names,
                 column_types_config_file,populate_data_flag_fieldname,
                 datatype_fieldname,header_column,randomly_skip_not_null_columns,
                 output_file,delimiter):
        self.operation = operation
        self.number_of_rows = number_of_rows
        self.add_column_names = add_column_names
        self.column_types_config_file = column_types_config_file
        self.populate_data_flag_fieldname = populate_data_flag_fieldname
        self.datatype_fieldname = datatype_fieldname
        self.header_column = header_column
        self.randomly_skip_not_null_columns = randomly_skip_not_null_columns
        self.output_file = output_file
        self.delimiter = delimiter