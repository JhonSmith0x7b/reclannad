#-*- coding:utf-8 -*-
from flask import current_app, url_for
import hashlib, time

class BaseLogic(object):
    def file_upload(self, f, upload_type, funcnum=0):
        mimetype_dic = {
            'image/gif': '.gif',
            'image/jpeg': '.jpg',
            'image/png': '.png'
        }
        if upload_type in ['article', 'modify_content']:
            mimetype = f.mimetype
            original_filename = f.filename
            md5 = hashlib.md5()
            md5.update(original_filename.encode())
            ext = mimetype_dic[mimetype] if mimetype in mimetype_dic.keys() else '.jpg'
            save_filename = '%.0f%s%s' % (time.time(), md5.hexdigest()[:13], ext)
            with open('%s/static/images/article/%s' % (current_app.root_path, save_filename), 'wb') as _f:
                _f.write(f.read())

            '''
            <html><body><script type="text/javascript">window.parent.CKEDITOR.tools.callFunction('.$GET('CKEditorFuncNum').', "'.圖片檔案連結.'","'.顯示處理結果的訊息.'");</script></body></html>
            '''
            if upload_type == 'article':
                return_data = '<script type="text/javascript">window.parent.CKEDITOR.tools.callFunction(%s, "%s", "%s");</script>' \
                                % (funcnum, url_for('static', filename='images/article/%s' % save_filename), '')
                
                return return_data
            elif upload_type == 'modify_content':
                return url_for('static', filename='images/article/%s' % save_filename)