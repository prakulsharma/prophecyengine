def filter_columns(method):

    def filter_df(*args, **kwargs):

        df = kwargs.get('df', None)
        if df is None:
            df = args[0]
        columns = kwargs.get('columns', None)
        if columns is None:
            if len(args) >= 2:
                columns = args[1]
        use_column_indices = kwargs.get('use_column_indices', None)
        if use_column_indices is None:
            if len(args) >= 3:
                use_column_indices = args[2]

        if columns is not None and type(columns) == list:
            if use_column_indices:
                df = df.iloc[:, columns]
            else:
                df = df[columns]

        if 'df' in kwargs:
            kwargs.pop('df')

        if len(args) > 1:
            return method(df, *args[1:], **kwargs)
        else:
            return method(df, **kwargs)

    return filter_df
