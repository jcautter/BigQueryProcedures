class ProcLog:
    def __init__(self):
        pass

    def __exec(self, title:str, query:str):
        print("{title} -- Begin".format(title=title))
        self.bq.execute_query(query, commit=True)
        print("{title} -- Finish".format(title=title))
