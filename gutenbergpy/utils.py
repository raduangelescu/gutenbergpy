import time
import sys
import os
import urllib
import tarfile

from gutenbergcachesettings import GutenbergCacheSettings



class Utils:
    @staticmethod
    def delete_tmp_files(delete_sqlite = False):
        if delete_sqlite:
            try:
                os.remove(GutenbergCacheSettings.CACHE_FILENAME)
            except OSError:
                pass
        try:
            os.remove(GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME)
        except OSError:
            pass
        try:
            for root, dirs, files in os.walk(GutenbergCacheSettings.CACHE_RDF_UNPACK_DIRECTORY, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        except OSError:
            pass

    @staticmethod
    def update_progress_bar(type,progress,total_progress): #used to update the progress bar display
        if total_progress % GutenbergCacheSettings.DOWNLOAD_NUM_DIVS == 0:
            dv = total_progress/GutenbergCacheSettings.DOWNLOAD_NUM_DIVS
            num_of_sharp = progress/dv
            num_of_space = (total_progress-progress)/dv

            sys.stdout.write("\r %s  %s: [%s%s]" % (type,GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME,'#'* num_of_sharp,' '*num_of_space))
            sys.stdout.flush()

    download_progress = 0
    @staticmethod
    def __report(block_no, block_size, file_size):  #callback called on download update
        Utils.download_progress += block_size
        type = 'Downloading %s'%(GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME)
        Utils.update_progress_bar(type,Utils.download_progress,file_size)

    @staticmethod
    def download_file(): #used to download the rdf tar file
        start = time.time()
        test_file = urllib.URLopener()
        test_file.retrieve(GutenbergCacheSettings.CACHE_RDF_DOWNLOAD_LINK,GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME,Utils.__report)
        print ('took %f' % (time.time()-start))
        Utils.download_progress = 0

    @staticmethod
    def unpack_tarbz2(): #used to unpack the rdf tar file
        start = time.time()
        tar   = tarfile.open(GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME)
        total_num = len(tar.getmembers())
        type = 'Extracting  %s' % (GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME)
        for idx,member in enumerate(tar.getmembers()):
            Utils.update_progress_bar(type,idx,total_num)
            tar.extract(member)
        tar.close()
        print('took %f'%(time.time()-start))
