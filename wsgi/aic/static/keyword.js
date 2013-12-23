$(function(){
  mentions = getKeywordMentions();
  plotStack(mentions);
  plotPie(mentions);
});

// mockdata
function getKeywordMentions() {
  var mentions = {positive: [], neutral: [], negative: []};

  var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  for (var i = 0; i <= months.length; i += 1) {
    mentions.positive.push([months[i], parseInt(Math.random() * 30)]);
    mentions.negative.push([months[i], parseInt(Math.random() * 30)]);
    mentions.neutral.push([months[i], parseInt(Math.random() * 30)]);
  }

  return mentions;
}

function plotStack(mentions) {
  var data = [mentions.positive, mentions.neutral, mentions.negative];

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
    colors: ['#C44D58', '#A8A890', '#14a085']
  };

  $.plot("#keyword-stack", data, options);
}

function plotPie(mentions) {
  var positive = 0;
  var negative = 0;
  var neutral = 0;

  for (i = 0; i < 12; i++) {
    positive += mentions.positive[i][1];
    negative += mentions.negative[i][1];
    neutral += mentions.neutral[i][1];
  }

  data = [{
    data: positive,
    color: '#C44D58'
  }, {
    data: neutral,
    color: '#A8A890'
  }, {
    data: negative,
    color: '#14a085'
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