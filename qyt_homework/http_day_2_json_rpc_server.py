from flask import Flask, request
import os
from http_day_2_system_cmd import system_cmd
import base64

server_file_dir = './'

node = Flask(__name__)

node.debug = True

@node.route('/cmd', methods=['POST'])
def cmd():
    # request.content_type = 'application/json'
    client_post_data = request.json
    if client_post_data:
        cmd_command = client_post_data.get('cmd')
        if cmd_command:
            cmd_result = system_cmd(cmd_command)
            if cmd_result[1]:
                return {'error': base64.b64encode(cmd_result[1].encode()).decode()}
            else:
                print(cmd_result[0])
                return  {'cmd': cmd_command, 'cmd_result': base64.b64encode(cmd_result[0].encode()).decode()}
        else:
            return {'error': base64.b64encode('no cmd in json'.encode()).decode()}
    else:
        return {'error': base64.b64encode('no json data'.encode()).decode()}

@node.route('/upload', methods=['POST'])
def upload():
    # request.content_type = 'application/json'
    client_post_data = request.json
    if client_post_data:
        upload_filename = client_post_data.get('upload_filename')
        file_bit = client_post_data.get('file_bit')
        if upload_filename and file_bit:
            with open(server_file_dir + upload_filename, 'wb') as f:
                f.write(base64.b64decode(file_bit.encode()))
            return {'message': 'Upload Success!', 'upload_file': upload_filename}
        else:
            return {'error': 'need upload_filename and file_bit'}
    else:
        return {'error': 'no json data'}

@node.route('/download', methods=['POST'])
def download():
    # request.content_type = 'application/json'
    client_post_data = request.json
    if client_post_data:
        download_filename = client_post_data.get('download_filename')
        if download_filename:
            print(download_filename)
            if os.path.exists(server_file_dir + download_filename):
                download_json = {'download_filename': download_filename}
                file_bit = base64.b64encode(open(server_file_dir + download_filename, 'rb').read()).decode()
                download_json['file_bit'] = file_bit
                return download_json
            else:
                return {'error': 'download file not exist'}
        else:
            return {'error': 'need download_filename'}
    else:
        return {'error': 'no json data'}

# @node.route('/emm', methods=['POST'])
# def router_control():
#     # request.content_type = 'application/json'
#     client_post_data = request.json
#     if client_post_data:
#         download_filename = client_post_data.get('download_filename')
#         if download_filename:
#             print(download_filename)
#             if os.path.exists(server_file_dir + download_filename):
#                 download_json = {'download_filename': download_filename}
#                 file_bit = base64.b64encode(open(server_file_dir + download_filename, 'rb').read()).decode()
#                 download_json['file_bit'] = file_bit
#                 return download_json
#             else:
#                 return {'error': 'download file not exist'}
#         else:
#             return {'error': 'need download_filename'}
#     else:
#         return {'error': 'no json data'}

if __name__ == "__main__":
    node.run(host='0.0.0.0', port=8000)