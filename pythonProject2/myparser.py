def findtill(data, start, end) :  # iterate through the string to find char
    index = data.find(start.encode('ascii'))
    index = index + len(start)
    ret = ""
    while (data[index] != end) :  # loop through until we find end char must be in ascii
        # print(chr(data[index]))
        ret += chr(data[index])
        index += 1
    return ret


def findbufferend(data, start, end) :  # i just used splice for this one, much easier

    if data.find(start) == -1:
        return
    index = data.find(start)
    index = index + len(start)
    ret = bytearray()
    first = data.find(start) + len(start)  # get the location of the end of 'start'
    data = data[first :]
    second = data.find(end)  # get location of the beginning of the 'end'
    data = data[:second]

    return data


def removeHTML(data) :
    ret = data.replace('&', "&amp;")  # remove all html characters
    ret = ret.replace('<', "&lt;")
    ret = ret.replace('>', "&gt;")
    return ret
