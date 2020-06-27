function drawTable() {
    var HTML = "<table border=1 width=1000>";
    HTML += "<tr>";
    HTML += "<td>구분</td>";
    HTML += "<td>전체 단어 수</td>";
    HTML += "<td>처리시간</td>";
    HTML += "<td>단어 분석</td>";
    HTML += "<td>유사도 분석</td>";
    HTML += "</tr>";

    //  for(i=0; i<rows; i++)   { 
    //     HTML += "<tr>";
    //     HTML += "<td>" + i+1 + "</td>";
    //     HTML += "<td>" + _data[i]["url"] + "</td>";
    //     HTML += "<td>" + _data[i]["time"] + "</td>";
    //     HTML += "<td>" + "<form method="POST" action="/words_func"><input type=submit value="단어 분석"></form>" + "</td>";
    //     HTML += "<td>" + "<form method="POST" action="/cosine_func"><input type=submit value="유사도 분석"></form>" + "</td>";
    //     HTML += "</tr>" ;
    // }
    
    for(var temp in _data)   { 
      HTML += "<tr>";
      HTML += "<td>" + i+1 + "</td>";
      HTML += "<td>" + _data[temp]["url"] + "</td>";
      HTML += "<td>" + _data[temp]["time"] + "</td>";
      HTML += "<td>" + "<form method="POST" action="/words_func"><input type=submit value="단어 분석"></form>" + "</td>";
      HTML += "<td>" + "<form method="POST" action="/cosine_func"><input type=submit value="유사도 분석"></form>" + "</td>";
      HTML += "</tr>" ;
  }
     HTML +=("</table>");
    document.getElementById("tablediv").innerHTML = HTML;

   } 
