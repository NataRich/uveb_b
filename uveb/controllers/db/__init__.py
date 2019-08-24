from contextlib import closing

from .. import Models


class ModuleNotFoundException(Exception):
    pass


class Init(Models):
    """Init MySQL Schema connection"""

    conn = None

    @classmethod
    def init(cls, connection):
        cls.conn = connection


class Fetchers(Init):
    handle = 'SELECT'


class Adders(Init):
    handle = 'INSERT'


class Updaters(Init):
    handle = 'UPDATE'


class Deleters(Init):
    handle = 'DELETE'


class AutoSQL(Init):
    @classmethod
    def get_columns(cls, table_name, args=None, tuplize=False, skip=()):
        """Get the columns of table_name from the map table

        :param table_name: the target table

        :param args: a tuple of strings which are names of columns

        :param tuplize: if true, tuplize the result; or stringify the result, otherwise

        :param skip: a tuple that specifies which columns to skip, usually which have
                    default settings

        :returns: 1. a string, "('col1', 'col2','col3', 'col4', ...)"
                  2. a tuple, ('col1', 'col2', 'col3', 'col4', ...)
        """

        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""SELECT * FROM map WHERE tableName='{table_name}'""")
            r = cur.fetchone()

        if not r:
            raise ModuleNotFoundException

        cols = tuple([col for col in r if col is not None and col not in skip][2:])

        if args:
            lst = [arg for col in cols for arg in args if arg == col]
            return tuple(lst) if tuplize else '(' + ', '.join(lst) + ')'

        else:
            lst = [col for col in cols]
            return tuple(lst) if tuplize else '(' + ', '.join(cols) + ')'

    @classmethod
    def gen_syntax(cls, table_name, vals, tuplize=False, AND=False, skip=()):
        """Generate a set of valid MySQL syntaxes

        :param table_name: the target table

        :param vals: a dictionary of values

        :param tuplize: if true, return a string-styled tuple of values, type sensitive

        :param AND: if true, use key word AND; or use ',', otherwise

        :param skip: a tuple that specifies which columns to skip

        :returns: 1. a string, "('val1', 'val2', val3, 'val4', ...)"
                  2. a string, "col1='val1', col2='val2', col3=val3, col4='val4', ..."
                  3. a string, "col1='val1' AND col2='val2' AND col3=val3 AND col4='val4' AND ...)"
                  (where val1, val2, val4 are strings, val3 is an integer)
        """

        cols = cls.get_columns(table_name, tuplize=True, skip=skip)

        if tuplize:
            lst = (f"{item[1]}" if type(item[1]) == int else f""" "{item[1]}" """ for col in cols
                   for item in vals.items() if item[0] == col and (item[1] or item[1] == 0))

            return '(' + ', '.join(lst) + ')'

        else:
            lst = [f"{item[0]}={item[1]}" if type(item[1]) == int else f"""{item[0]}="{item[1]}" """
                   for col in cols for item in vals.items() if item[0] == col and (item[1] or item[1] == 0)]

            return ' AND '.join(lst) if AND else ', '.join(lst)

    @staticmethod
    def gen_special(ids=(), title=None):
        """Generate a string of id keys

        :param ids: a tuple of ids, int

        :param title: a string

        :returns: 1. a string, 'id'
                  2. a string, 'id=1 OR id=2 OR id=3...'
        """

        if len(ids) == 0 and len(title) == 0:
            return 'id'

        lst = ['id=' + str(id) for id in ids]
        if len(title) == 0:

            return ' OR '.join(lst)

        elif len(ids) == 0:
            return f"title='{title}'"

        else:
            return ' OR '.join(lst) + f" AND title='{title}'"

    @staticmethod
    def add_suffix(limit=0, offset=0, asc=True, by_col='date'):
        if asc:
            return f" ORDER BY {by_col} ASC LIMIT {limit} OFFSET {offset} "
        return f" ORDER BY {by_col} DESC LIMIT {limit} OFFSET {offset} "
