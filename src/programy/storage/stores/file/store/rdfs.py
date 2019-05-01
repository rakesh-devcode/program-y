"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger

from programy.storage.stores.file.store.filestore import FileStore

from programy.storage.entities.rdf import RDFStore

class FileRDFStore(FileStore, RDFStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _load_file_contents(self, rdf_collection, filename):
        YLogger.debug(self, "Loading rdf [%s]", filename)
        try:
            with open(filename, 'r', encoding='utf8') as my_file:
                for line in my_file:
                    if line:
                        splits = line.split(":")
                        if len(splits) > 2:
                            subj = splits[0].upper()
                            pred = splits[1].upper()
                            obj = (":".join(splits[2:])).strip()
                            
                            rdf_name = self.get_just_filename_from_filepath(filename)
                            
                            rdf_collection.add_entity(subj, pred, obj, rdf_name, filename)
                            
        except Exception as excep:
            YLogger.exception_nostack(self, "Failed to load rdf [%s]", excep, filename)

    def get_storage(self):
        return self.storage_engine.configuration.rdf_storage

    def reload(self, collection, rdf_name):
        filename = collection.storename(rdf_name)
        collection.empty()
        self._load_file_contents(collection, filename)
