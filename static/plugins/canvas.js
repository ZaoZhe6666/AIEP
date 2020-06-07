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

function sensitivity_canvas(data, label){
	var config = {
      // The type of chart we want to create
      type: "line",
      // The data for our dataset
      data: {
        labels: label,
        datasets: [
          {
            label: "Vanilla",
            backgroundColor: "transparent",
            borderColor: "rgb(82, 136, 255)",
            data: data["data"]["Vanilla"][0],
            lineTension: 0,
            pointRadius: 5,
            pointBackgroundColor: "rgba(255,255,255,1)",
            pointHoverBackgroundColor: "rgba(255,255,255,1)",
            pointBorderWidth: 2,
            pointHoverRadius: 7,
            pointHoverBorderWidth: 1
          },
          {
            label: "PAT",
            backgroundColor: "transparent",
            borderColor: "rgb(255, 199, 15)",
            data: data["data"]["PAT"][0],
            lineTension: 0,
            borderDash: [10, 5],
            borderWidth: 1,
            pointRadius: 5,
            pointBackgroundColor: "rgba(255,255,255,1)",
            pointHoverBackgroundColor: "rgba(255,255,255,1)",
            pointBorderWidth: 2,
            pointHoverRadius: 7,
            pointHoverBorderWidth: 1
          }
        ]
      },
      // Configuration options go here
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
                // callback: function(tick, index, array) {
                //   return (index % 2) ? "" : tick;
                // }
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
    };
    return config;
}

function line_name_append(data){
	var html = ""
	for (var key in data){
		html += "<li class='nav-item'><a class='nav-link pb-md-0' data-toggle='tab' href='#"
		html += "' role='tab' aria-controls='' aria-selected='false'><h4 class='type-name'>"
		html += data[key]
		html += "</h4></a></li>"
	}
	return html
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
      ret += "<div><img data-u='image' src='";
      ret += DIR + "/" + picname;
      ret += "'></div>"
    }
    else{
      ret += "<div style='display: none;'><img data-u='image' src='";
      ret += DIR + "/" + picname;
      ret += "'></div>"
    }
  }
  return ret;
}

function pic_in_pair(id, ori_path, attack_path, style){
	var html = "";
	html += "<div data-p='150.00' "
  html += style;
  html += " id='"
	html += id
	html += "' class='beer-slider' data-beer-label='before'><img data-u='image' src='"
	html += ori_path
	html += "'><div class='beer-reveal' data-beer-label='after'><img data-u='image' src='"
	html += attack_path
	html += "' style='width: 720px; height: 480px;'></div></div>"
	return html;
}

function read_table_list(data){
  console.log(data)
  var html = "<thead><tr align='center'><td rowspan='2'>" + data["TITLE"][0] + "</td>"
  html += "<td rowspan='2'>CLEAN</td>"
  block_num = data["TITLE"][3].length;
  html += "<td colspan='" + block_num + "'>" + data["TITLE"][2] + "</td></tr><tr align='center'>"
  for(var param in data["TITLE"][3]){
    html += "<td>" + data["TITLE"][3][param] + "</td>"
  }
  html += "</tr></thead><tbody>";
  // 添加具体表格内容，一个内容一行
  for(var key in data){
    if(key == "TITLE") continue;
    html += "<tr align='center'>";
    for(var param in data[key]){
      html += "<td>" + data[key][param] + "</td>";
    }
    html += "</tr>";
  }
  html += "</tbody>"
  return html;
}

function read_table(table){
  var html = "<thead>";
  for(var row_key in table){
    console.log("row_key = " + table[row_key])
    html += "<tr>"
    for(var key2 in table[row_key]){
      console.log("tmp =" + table[row_key][key2])
      html += "<td"
      if(table[row][tmp].length == 1){
        if(row == "TITLE"){
          html += " rowspan='2'";
        }
        html += ">" + table[row][tmp]
      }
      else{
        html += ">";
        for(var level3 in table[row][tmp]){
          console.log(table[row][tmp][level3])
          html += "<td>" + table[row][tmp][level3] + "</td>";
        }
        html += "</tr></tbody>"
      }
      html += "</td>"
    }
    html += "</tr>"
    if(row == "TITLE"){
      html += "</thead><tbody>"
    }
  }
  return html
}

function cam_pic_path(DIR, num){
  var html = "";
  var path = "/static/upload/Results/" + DIR + "/CamResult/"
  html += "<img src='";
  html += path + "OriginSample_orig_" + num;
  html += ".jpg' alt='' class='img-fluid'>"
  html += "<img src='";
  html += path + "AttackSample_orig_" + num;
  html += ".jpg' alt='' class='img-fluid'>"
  html += "<img src='";
  html += path + "OriginSample_cam_" + num;
  html += ".jpg' alt='' class='img-fluid'>"
  html += "<img src='";
  html += path + "AttackSample_cam_" + num;
  html += ".jpg' alt='' class='img-fluid'>"
  return html;
}

function cam_rolling(num){
  var html = "";
  for(var i = 0; i < num; i++){
    if(i == 0){
      html += "<li data-target='#carouselTestimonial' data-slide-to='0' class='active'></li>"
    }
    else{
      html += "<li data-target='#carouselTestimonial' data-slide-to='" + i + "' class=''></li>"
    }
  }
  return html;
}

function cam_pic_show(cam_list){
  var html = "";
  var DIR = cam_list["DIR"];
  for(var key in cam_list){
    if(key == "DIR"){
      continue;
    }
    if(html == ""){
      html += "<div class='carousel-item active'><div class='card border-0 text-center'><div class='card-img-wrapper '>";
    }
    else{
      html += "<div class='carousel-item'><div class='card border-0 text-center'><div class='card-img-wrapper '>";
    }
    html += cam_pic_path(DIR, key);
    html += "</div><div class='card-body'><p>";
    html += "上方第一张图为原始图像，第二张图为攻击后图像，通过肉眼我们很难分别出两张图像的不同，但是通过热力图观察模型关注度我们可以发现，经过攻击后的图像与原始图像相比，关注区域发生了变化。"
    html += cam_list[key];
    html += "</p></div></div></div>";
  }
  return html;
}

function get_data_size(){
  var config = {
    data: {
      datasets: [
        {
          data: [80, 80, 50, 10],
          backgroundColor: [
            "rgba(41,204,151,0.5)",
            "rgba(254,88,101,0.5)",
            "rgba(254,196,0,0.5)",
            "rgba(76,132,255,0.5)"
          ],
          label: "" // for legend
        }
      ],
      labels: ["训练样本", "对抗攻击样本", "测试样本", "可解释性评估样本"]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        position: "right",
        display: false
      },
      layout: {
        padding: {
          top: 10,
          bottom: 10,
          right: 10,
          left: 10
        }
      },
      scale: {
        ticks: {
          beginAtZero: true,
          fontColor: "#1b223c",
          fontSize: 12,
          stepSize: 20,
          max: 100
        },
        reverse: false
      },
      animation: {
        animateRotate: false,
        animateScale: true
      },
      tooltips: {
        titleFontColor: "#888",
        bodyFontColor: "#555",
        titleFontSize: 12,
        bodyFontSize: 14,
        backgroundColor: "rgba(256,256,256,0.95)",
        displayColors: true,
        borderColor: "rgba(220, 220, 220, 0.9)",
        borderWidth: 2
      }
    }
  }
  return config;
}

function get_CE(data){
  var base_line = new Array(data["CE"].length);
  for(var i = 0; i < data["CE"].length; i++){
    base_line[i] = data["BASE_LINE"];
  }
  var config =  {
    type: "radar",
    data: {
      labels: data["STYLE"],
      datasets: [
        {
          label: "CE",
          backgroundColor: "rgba(76,132,255,0.2)",
          borderColor: "#4c84ff",
          pointBorderWidth: 2,
          pointRadius: 4,
          pointBorderColor: "rgba(76,132,255,1)",
          pointBackgroundColor: "#ffffff",
          data: data["CE"]
        },
        {
          label: "Related CE",
          backgroundColor: "rgba(41, 204, 151, 0.2)",
          borderColor: "#29cc97",
          pointBorderWidth: 2,
          pointRadius: 4,
          pointBorderColor: "#29cc97",
          pointBackgroundColor: "#ffffff",
          data: data["RCE"]
        },
        {
          label: "BASE LINE",
          backgroundColor: "rgba(105, 105, 105, 0.1)",
          borderColor: "#696969",
          pointBorderWidth: 1,
          pointRadius: 1,
          pointBorderColor: "#696969",
          pointBackgroundColor: "#ffffff",
          data: base_line
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      legend: {
        display: true
      },
      layout: {
        padding: {
          top: 10,
          bottom: 10,
          right: 10,
          left: 10
        }
      },
      scale: {
        ticks: {
          beginAtZero: true,
          fontColor: "#1b223c",
          fontSize: 12,
          stepSize: 40,
          max: 200
        }
      },
      tooltips: {
        titleFontColor: "#888",
        bodyFontColor: "#555",
        titleFontSize: 12,
        bodyFontSize: 14,
        backgroundColor: "rgba(256,256,256,0.95)",
        displayColors: true,
        borderColor: "rgba(220, 220, 220, 0.9)",
        borderWidth: 2
      }
    }
  };
  return config;
}

function get_color(num){
  var pre = ["rgb(82, 136, 255)", "rgb(255, 215, 0)", "rgb(255, 105, 180)",
             "rgb(0, 128, 0)", "rgb(255, 0, 0)", "rgb(139, 0, 139)", "rgb(0, 0, 0)"]
  if(num < pre.length) return pre[num];
  return "rgb(" + int(random() * 256) + ", " + int(random() * 256) + ", " + int(random() * 256) + ")";
}

function get_EENI(data){
  var datasets = []
  for(var key in data){
    if(key == "TITLE") continue;
    var data_tmp = {
      label: key,
      backgroundColor: "transparent",
      borderColor: get_color(datasets.length),
      data: data[key],
      lineTension: 0,
      pointRadius: 5,
      pointBackgroundColor: "rgba(255,255,255,1)",
      pointHoverBackgroundColor: "rgba(255,255,255,1)",
      pointBorderWidth: 2,
      pointHoverRadius: 7,
      pointHoverBorderWidth: 1
    }
    datasets.push(data_tmp);
  }
  console.log(datasets)
  var config = {
    type: "line",
    data: {
      labels: data["TITLE"],
      datasets: datasets
    },
    options: {
      responsive: false,
      maintainAspectRatio: false,
      legend: {
        display: true
      },
      scales: {
          xAxes: [
            {
              gridLines: {
                display: true
              },
              ticks: {
                display: true
              }
            }
          ]
      },
      tooltips: {
        mode: "index",
        intersect: true,
        titleFontColor: "#888",
        bodyFontColor: "#555",
        titleFontSize: 12,
        bodyFontSize: 15,
        backgroundColor: "rgba(256,256,256,0.95)",
        displayColors: true,
        xPadding: 5,
        yPadding: 7,
        borderColor: "rgba(220, 220, 220, 0.9)",
        borderWidth: 2,
        caretSize: 10,
        caretPadding: 5
      }
    }
  };
  return config;
}