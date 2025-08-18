from wxconv import WXC

def wx_to_devanagari(word):
    wxc = WXC(source='wx', target='utf')
    return wxc.convert(word)

print(wx_to_devanagari('bAla'))
