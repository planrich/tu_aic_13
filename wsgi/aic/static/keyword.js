$(function(){
  plotStack(mentions);
  plotPie(mentions);
});

function plotStack(mentions) {
  var data = [mentions.positive.data, mentions.neutral.data, mentions.negative.data]

  var options = {
    grid: {
       borderWidth: {top: 0, right: 0, bottom: 2,left: 0}
    },
    series: {
      stack: 0,
      lines: {
        show: false,
        fill: true,
        steps: false
      },
      bars: {
        show: true,
        barWidth: 0.6,
        align: "center",
        fill: 0.8
      }
    },
    xaxis: {
      tickLength: 0,
      mode: "categories"
    },
    colors: ['#14a085', '#A8A890', '#f0776c']
  };

  $.plot("#keyword-stack", data, options);
}

function plotPie(mentions) {
  data = [{
    data: mentions.positive.count,
    color: '#14a085'
  }, {
    data: mentions.neutral.count,
    color: '#A8A890'
  }, {
    data: mentions.negative.count,
    color: '#f0776c'
  }];

  var options = {
    series: {
      pie: {
        show: true,
        stroke: {
          width: 2
        }
      }
    }
  }

  $.plot("#keyword-pie", data, options);
}