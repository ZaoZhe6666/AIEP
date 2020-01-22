function cube_canvas(labels, datasets){
	var return_var = {
      	type: "bar",
      	data: {
	        labels: labels,
        datasets: [
          {
            label: "准确度",
            data: datasets,
            // data: [2, 3.2, 1.8, 2.1, 1.5, 3.5, 4, 2.3, 2.9, 4.5, 1.8, 3.4, 2.8],
            backgroundColor: "#4c84ff"
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        scales: {
          xAxes: [
            {
              gridLines: {
                drawBorder: true,
                display: false,
              },
              ticks: {
                fontColor: "#8a909d",
                fontFamily: "Roboto, sans-serif",
                display: false, // hide main x-axis line
                beginAtZero: true,
                callback: function(tick, index, array) {
                  return index % 2 ? "" : tick;
                }
              },
              barPercentage: 1.8,
              categoryPercentage: 0.2
            }
          ],
          yAxes: [
            {
              gridLines: {
                drawBorder: true,
                display: true,
                color: "#eee",
                zeroLineColor: "#eee"
              },
              ticks: {
                fontColor: "#8a909d",
                fontFamily: "Roboto, sans-serif",
                display: true,
                beginAtZero: true
              }
            }
          ]
        },

        tooltips: {
          mode: "index",
          titleFontColor: "#888",
          bodyFontColor: "#555",
          titleFontSize: 12,
          bodyFontSize: 15,
          backgroundColor: "rgba(256,256,256,0.95)",
          displayColors: true,
          xPadding: 10,
          yPadding: 7,
          borderColor: "rgba(220, 220, 220, 0.9)",
          borderWidth: 2,
          caretSize: 6,
          caretPadding: 5
        }
      }
    }
    return return_var;
}

function line_append(data){
	var html = ""
	for (var key in data){
		html += "<li class='nav-item'><a class='nav-link pb-md-0' data-toggle='tab' href='#"
		html += "' role='tab' aria-controls='' aria-selected='false'><h4 class='type-name'>"
		html += key
		html += "</h4></a></li>"
	}
	return html
}

function line_canvas(data){
	var config = {
		type: "line",
		data: {
			labels: data["label"],
			datasets: []
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			legend: {
				display: false
			},
			scales: {
				xAxes: [
					{
						gridLines: {
							display: false,
						},
						ticks: {
							fontColor: "#8a909d", // this here
						},
					}
				],
				yAxes: [
					{
						gridLines: {
							fontColor: "#8a909d",
							fontFamily: "Roboto, sans-serif",
							display: true,
							color: "#eee",
							zeroLineColor: "#eee"
						},
						ticks: {
							stepSize: 50,
							fontColor: "#8a909d",
							fontFamily: "Roboto, sans-serif"
						}
					}
				]
			},
			tooltips: {
				mode: "index",
				intersect: false,
				titleFontColor: "#888",
				bodyFontColor: "#555",
				titleFontSize: 12,
				bodyFontSize: 15,
				backgroundColor: "rgba(256,256,256,0.95)",
				displayColors: true,
				xPadding: 10,
				yPadding: 7,
				borderColor: "rgba(220, 220, 220, 0.9)",
				borderWidth: 2,
				caretSize: 6,
				caretPadding: 5
			}
		}
	}

	var key;
	for(key in data["data"]){
		break;
	}
	for(var i = 0; i < data["data"][key].length; i++){
		var datatmp = {
			label: "style_" + i,
			backgroundColor: "transparent",
			borderColor: "rgb(82, 136, 255)",
			data: data["data"][key][i],
			lineTension: 0,
			pointRadius: 5,
			pointBackgroundColor: "rgba(255,255,255,1)",
			pointHoverBackgroundColor: "rgba(255,255,255,1)",
			pointBorderWidth: 2,
			pointHoverRadius: 7,
			pointHoverBorderWidth: 1
		}
		config.data.datasets.push(datatmp)
	}
	return config
}

function getFileType(filePath){
	var startIndex = filePath.lastIndexOf(".");
	if(startIndex != -1)
		return filePath.substring(startIndex+1, filePath.length).toLowerCase();
	else return "";
}

function pic_read(data){
	var ret = "";
	var DIR = data['DIR'];
	for(var i in data["name"]){
		var picname = data["name"][i];
		var type = getFileType(DIR + "/" + picname);
		if(type != "png" && type != "jpg"){
			continue;
		}
		if(ret == ""){
			ret += "<div data-p='150.00'><img data-u='image' src='";
			ret += DIR + "/" + picname;
			ret += "' />img data-u='thumb' src='";
			ret += DIR + "/" + picname;
			ret += "' /></div>"
		}
		else{
			ret += "<div data-p='150.00' style='display: none;'><img data-u='image' src='";
			ret += DIR + "/" + picname;
			ret += "' />img data-u='thumb' src='";
			ret += DIR + "/" + picname;
			ret += "' /></div>"
		}
	}
	return ret;
}