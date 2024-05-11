for i in range(1,10):
    print("<tr>")
    for j in range(1,10):
        s = ""
        if i % 3 == 1 and j %3 == 1:
            s=f"<td class=\"thick-top thick-left cell\"><p id=\"C{i}{j}\"></p></td>"
        elif i % 3 == 1:
            s=f"<td class=\"thick-top cell\"><p id=\"C{i}{j}\"></p></td>"
        elif j% 3 == 1:
            s=f"<td class=\"thick-left cell\"><p id=\"C{i}{j}\"></p></td>"
        else:
            s=f"<td class=\"cell\"><p id=\"C{i}{j}\"></p></td>"
        if i == 9:
            s = s.replace("class=\"", "class=\"thick-bottom ")
        if j == 9:
            s = s.replace("class=\"", "class=\"thick-right ")
        print(s)
    print("</tr>")