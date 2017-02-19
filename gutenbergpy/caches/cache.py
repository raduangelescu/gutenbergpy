##
# Base class for any kind of cache
class Cache():
    def create_cache(self):
        raise NotImplementedError( "Please implement the create_cache function" )
    def query(self,**kwargs):
        raise NotImplementedError("Please implement the query function")
    def native_query(self,sql_query):
        raise NotImplementedError("Please implement the native_query function")